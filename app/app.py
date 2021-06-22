from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response, session, make_response, render_template
import json, bson
import uuid
import time


# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSMarkets']

# Choose collections
users = db['Users']
products = db['Products']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}
cart=[]


def create_session(email, category):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (email, category, time.time())
    return user_uuid


def is_session_valid(user_uuid):
    return user_uuid in users_sessions

def calculate_total():
    total=0
    for i in range(0, len(cart)):
        total += cart[i]['price'] * cart[i]['quantity']
    return total

def get_current_user_email():
    # Retrieve email from ussers_sessions for current user
    if users_sessions:
        current_user = list(users_sessions.items())[-1]
        for item in current_user:
            email = item[0]
        return email

def get_current_user_category():
    # Retrieve email from ussers_sessions for current user
    if users_sessions:
        current_user = list(users_sessions.items())[-1]
        for item in current_user:
            category = item[1]
        return category

def get_current_user_uuid():
    # Retrieve uuid from ussers_sessions for current user
    if users_sessions:
        current_user = list(users_sessions.items())[-1]
        uuid=current_user[0]
        return uuid

# Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    # Έλεγχος δεδομένων email / password
    # Αν δεν υπάρχει user με το email που έχει δοθεί
    if users.find({"email": data['email']}).count() == 0:
        user = {"name": data['name'], "email": data['email'], "password": data['password'], "category": "user"}
        # Add user to the 'Users' collection
        users.insert_one(user)
        # Μήνυμα επιτυχίας
        return Response(data['name'] + ", you have successfully signed up.", status=200, mimetype='application/json')
    else:
        # Μήνυμα λάθους (Υπάρχει ήδη κάποιος χρήστης με αυτό το email)
        return Response("A user with the given email already exists", status=400, mimetype='application/json')

#============ User actions ============#

# Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    # Έλεγχος δεδομένων email / password
    # Αν η αυθεντικοποίηση είναι επιτυχής.
    result = users.find_one({"email": data['email'], "password":data['password']})
    if result!=None:
        cart.clear()
        #Δημιουργία ενός session για τον χρήστη
        user_uuid = create_session(data['email'], result['category'])

        #Αποθήκευση πληροφοριών uuid και email σε ένα dictionary
        res = {"uuid": user_uuid, "email": data['email']}
        #Μήνυμα επιτυχίας
        return Response("Session initiated. \nWelcome to DSMarket "+ result['name'] +" \nData:\n "+ json.dumps(res),status=200, mimetype='application/json')  # ΠΡΟΣΘΗΚΗ STATUS

    # Διαφορετικά, αν η αυθεντικοποίηση είναι ανεπιτυχής.
    else:
        # Μήνυμα λάθους (Λάθος email ή password)
        return Response("Wrong username or password.", status=400, mimetype='application/json')  # ΠΡΟΣΘΗΚΗ STATUS

# Διαγραφή Λογαριασμού
@app.route('/deleteAccount/', methods=['DELETE'])
def delete_account():
    # Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        if get_current_user_category() == 'user':
            email = get_current_user_email()
            #Query για την εύρεση
            user = users.find_one({"email": email})
            # Αν υπάρχει χρήστης με το συγκεκριμένο email
            if user != None:
                # Διαγραφή του
                users.delete_one({"email": email})

                if users_sessions:
                    for item in list(users_sessions):
                        del users_sessions[item]
                # Μήνυμα επιτυχούς διαγραφής
                return Response( "The account associated with the email '" + email + "' was successfully deleted.", status=200, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.",
                            status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Αναζήτηση προϊόντος βάση ονόματος
@app.route('/findProduct/name/<string:name>', methods=['GET'])
def get_product_by_name(name):
    #Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    #Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        if get_current_user_category() == 'user':
            #Query για την εύρεση προϊόντος με συγκεκριμένο όνομα
            result = products.find({"name": {"$regex": name, "$options":"i"}})
            # δημιουργία λίστας
            products_list = []
            #Αν υπάρχει προϊόν
            if result.count()>0:
                # Κράτα τα σε μια λίστα
                for item in result:
                    item['_id'] = str(item['_id'])
                    products_list.append(item)
                # Μήνυμα επιτυχούς αναζήτησης προϊόντων (δηλ. υπάρχουν προϊόντα με αυτό το όνομα).
                return Response("Products matching '"+ name+ "' : \n" + json.dumps(products_list), status=200, mimetype='application/json')
            else:
                # Μήνυμα αποτυχίας
                return Response("There are no productd associated with the name " + name, status=400, mimetype="application/json")
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.", status=400,
                            mimetype='application/json')
    else:
        # Μήνυμα αποτυχίας ( Δεν υπάρχει session με το id που δώθηκε )
        return Response("Unauthorized client error. No session initiated." , status=401, mimetype="application/json")

# Αναζήτηση προϊόντος βάση κατηγορίας
@app.route('/findProduct/category/<string:category>', methods=['GET'])
def get_product_by_category(category):
    # Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')

    uuid = get_current_user_uuid()
    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        if get_current_user_category() == 'user':
            # Query για την εύρεση προϊόντος με συγκεκριμένη κατηγορία
            result = products.find({'category': category}).sort("price")
            # δημιουργία λίστας
            products_list = []
            # Αν υπάρχει προϊόν
            if result != None:
                # Κράτα τα σε μια λίστα
                for item in result:
                    item['_id'] = str(item['_id'])
                    products_list.append(item)
                print(products_list)
                # Μήνυμα επιτυχούς αναζήτησης προϊόντων (δηλ. υπάρχουν προϊόντα στην κατηγορία).
                return Response("Products matching '" + category + "' : \n" + json.dumps(products_list), status=200,
                                mimetype='application/json')
            else:
                # Μήνυμα λάθους
                return Response("There is no Product associated with the category '" + category + "'", status=400,
                                mimetype="application/json")
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.",
                            status=400, mimetype='application/json')

    else:
        # Μήνυμα λάθους ( Δεν υπάρχει session με το id που δώθηκε )
        return Response("Unauthorized client error. No session initiated.", status=401, mimetype="application/json")

# Αναζήτηση προϊόντος βάση κατηγορίας
@app.route('/findProduct/ID/<string:id>', methods=['GET'])
def get_product_by_id(id):

    #Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()
    #Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        #Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            #έλεγχος για σωστό τύπο του ID που δίνεται
            if bson.objectid.ObjectId.is_valid(id):

                #Query για την εύρεση προϊόντων με συγκεκριμένο ID
                result = products.find_one({"_id": ObjectId(id)},{"_id":0})
                # δημιουργία λίστας
                products_list = {}
                #Αν υπάρχει προϊόν
                if result!=None:
                    # Κράτα τα σε μια λίστα
                    for item in result:
                        products_list[item] = result[item]
                    # Μήνυμα επιτυχούς αναζήτησης προϊόντων (δηλ. υπάρχει προϊόν με αυτό το ID).
                    return Response("The product with the ID '"+ id + "' is the following: \n" + json.dumps(products_list), status=200, mimetype='application/json')
                else:
                    # Μήνυμα λάθους
                    return Response("There is no Product associated with the id " + id, status=400, mimetype="application/json")
            else:
                # Μήνυμα λάθους
                return Response("The ID you provided is not correct. Please try again.", status=400, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account." ,status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους ( Δεν υπάρχει session με το id που δώθηκε )
        return Response("Unauthorized client error. No session initiated." , status=401, mimetype="application/json")

# Προσθήκη σε καλάθι
@app.route('/addToCart/<string:id>/<int:quantity>', methods=['GET'])
def add_to_cart(id, quantity):
    # Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            # έλεγχος για σωστό τύπο του ID που δίνεται
            if bson.objectid.ObjectId.is_valid(id):

                # Query για την εύρεση με βάση το id
                result = products.find_one({"_id": ObjectId(id)})

                #ανανέωση του id με srting id για την αποφυγή λάθους κατά το response
                result['_id']=id
                # προσθήκη του quantity για την προσθήκη του στο cart
                result['quantity']= quantity

                # Αν υπάρχει το προϊόν
                if result != None:
                    #Αν το υπάρχει διαθέσιμο stock μεγαλύτερο από την ποσότητα που ζητείται, προχώρα παρακάτω
                    if result['stock']>quantity:
                        #προσθήκη προϊόντος στο καλάθι
                        cart.append(result)
                        #τροποποίηση του κόστους για να έχει μέχρι 2 δεκαδικά ψηφία
                        cost = "{:.2f}".format(calculate_total())

                        # Μήνυμα επιτυχούς προσθήκης στο καλάθι
                        return Response("Cart was updated with " + str(quantity) + " items of " + result['name'] + ". \n Your cart now includes: "
                                        + json.dumps(cart)
                                        + "\n Total cost is: " + str(cost) + "€" , status=200, mimetype='application/json')
                    else:
                        #Μύνημα λάθους
                        return Response("We are sorry but the quantity you are asking for is greater than our stock of this product. \n Current stock of " + result['name'] + " is: " + str(result['stock']) )
                else:
                    # Μήνυμα λάθους
                    return Response("There is no such product available.", status=200, mimetype='application/json')
            else:
                # Μήνυμα λάθους
                return Response("The ID you provided is not correct. Please try again.", status=400, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Εμφάνιση καλαθιού
@app.route('/showCart', methods=['GET'])
def show_cart():
    # Ελεγχος ύπαρξης session
    # uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            # Αν το καλάθι έχει στοιχεία μέσα
            if cart:
                # τροποποίηση του κόστους για να έχει μέχρι 2 δεκαδικά ψηφία
                cost = "{:.2f}".format(calculate_total())

                # Μήνυμα επιτυχούς εμφάνισης καλαθιού
                return Response("Your cart includes: " + json.dumps(cart) + "\n Total cost is: " + str(cost) +"€"  , status=200, mimetype='application/json')
            else:
                print("The cart doens't have any items")
                # Μήνυμα λάθους
                return Response("The cart is empty.", status=200, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Αφαίρεση από το καλάθι ενός προϊόντος
@app.route('/removeFromCart/<string:id>', methods=['GET'])
def remove_from_cart(id):
    # Ελεγχος ύπαρξης session
    # uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            # έλεγχος για σωστό τύπο του ID που δίνεται
            if bson.objectid.ObjectId.is_valid(id):
                # Αν το καλάθι έχει στοιχεία μέσα
                if cart:
                    #Βες την θέση του προϊόντος πρπς αφαίρεση από το καλάθι
                    position=0
                    for i in range(0, len(cart)):
                        if cart[i]['_id']==id:
                            position = i

                    #και αφαίρεσέ το από την θέση αυτή
                    del cart[position]
                    # τροποποίηση του κόστους για να έχει μέχρι 2 δεκαδικά ψηφία
                    cost = "{:.2f}".format(calculate_total())

                    # Επανέλεγχος για το εάν το καλάθι έχει στοιχέια μέσα. Έτσι όταν αφαιρεθούν όλα, να βγάλει κατάλληλο μήνυμα λάθους
                    if cart:
                        return Response("Your cart includes: " + json.dumps(cart) + "\n Total cost is: " + str(cost) +"€",
                                        status=200, mimetype='application/json')
                    else:
                        # Μήνυμα λάθους
                        return Response("The cart doens't have any more items to remove")
                else:

                    print("The cart doens't have any items")
                    # Μήνυμα λάθους
                    return Response("The cart is empty.", status=200, mimetype='application/json')
            else:
                # Μήνυμα λάθους
                return Response("The ID you provided is not correct. Please try again.", status=400,
                                mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.",
                            status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Αγορά προϊόντος
@app.route('/checkOut/<int:card_num>', methods=['GET'])
def buy_products(card_num):
    # uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            # Αν το καλάθι έχει στοιχεία μέσα
            if cart:
                #Μετατροπή της κάρτας σε string
                str(card_num)
                #Αν τα ψηφία της κάρτας είναι 16
                if len(str(card_num))==16:
                    #Ανανέσε για κάθε προϊόν του καλαθιού το stock στην βάση
                    for item in cart:
                        new_stock = item['stock']-item['quantity']
                        query = {"_id": ObjectId(item['_id'])}
                        updated_stock = {"$set": {"stock": new_stock}}
                        # Update του document
                        products.update_one(query, updated_stock)
                    #Πάρε το email του χρήστη που είναι συνδεδεμένος
                    email = get_current_user_email()

                    query = {"email": email}

                    #βρες το κόστος του καλαθιού
                    cost = calculate_total()
                    #πρόσθεσέ το στο cart για να υπάρχει ξεχωριστά το συνολικό κόστος
                    cart.append({"cost":"{:.2f}".format(cost)})

                    #ανανέωσε το orderHistory με το cart
                    orderHistory_update = {"$push": {"orderHistory": cart}}
                    # Update του document
                    users.update_one(query, orderHistory_update)
                    user = users.find_one(query)
                    #άσειασμα του καλαθιού
                    cart.clear()
                    # Μήνυμα επιτυχίας
                    return Response("Thank you for your purchase. \nReceipt for purchase:" +"\n Total Cost: " + str(user['orderHistory'][-1][-1]['cost']) + "€" + "\n Products bought: " +json.dumps(user['orderHistory'][-1]) , status=200, mimetype='application/json')
                else:
                    return Response("The input of your card number is not 16 digits long. Please try again.", status=200, mimetype='application/json')
            else:
                print("The cart doens't have any items")
                # Μήνυμα αποτυχίας
                return Response("The cart is empty.", status=200, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Εμφάνιση ιστορικού πωλήσεων
@app.route('/viewHistory', methods=['GET'])
def view_history():
    # uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης δν είναι admin
        if get_current_user_category() == 'user':
            #Βρες το email του χρήστη που είναι συνδεδεμένος
            email = get_current_user_email()
            #ψάξε τα στοιχεία του στην βάση και δες εάν έχει ιστορικό παραγγελιών
            result = users.find_one({"email": email, "orderHistory":{"$exists": True}})

            #Αν έχει
            if result!=None:
                # Μήνυμα επιτυχίας
                    return Response("Your order history is the following: \n" + json.dumps(result['orderHistory']), status=200, mimetype='application/json')
            else:
                # Μήνυμα αποτυχίας
                return Response("You haven't made any orders yet.", status=400, mimetype="application/json")
        else:
            # Μήνυμα λάθους
            return Response("You are logged in with your admin account. Please switch to a normal user account.", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

#============ Admin actions ============#

# Εισαγωγή νέου product
@app.route('/addProduct', methods=['POST'])
def add_product():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" or not "price" or not "description" or not "category" or not "stock" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    # Ελεγχος ύπαρξης session
    # uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης είναι admin
        if get_current_user_category() == 'admin':
            #Αναζήτηση ύπαρξης προιϊόντος
            result = products.find_one({"name": data["name"]})
            #Αν δεν υπάρχει, να γίνει η προσθήκη στην βάση
            if result==None:
                insert_product = {"name": data['name'], "price": data['price'], "description": data['description'], "category": data['category']
                , "stock": data['stock']}

                product = {"name": data['name'], "price": data['price'], "description": data['description'],
                           "category": data['category']
                    , "stock": data['stock']}
                # Add product to the 'Products' collection
                products.insert_one(insert_product)
                # Μήνυμα επιτυχίας
                return Response("The product with the name '" + data['name'] + "' was added: " + json.dumps(product), status=200, mimetype='application/json')
            else:
                # Μήνυμα λάθους
                return Response("The product with the name '" + data['name'] + "' already exists", status=200,
                                mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("Action not allowed, user does not have admin privileges!", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Διαγραφή product βάση ID
@app.route('/deleteProduct/<string:id>', methods=['DELETE'])
def delete_product(id):
    # Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης είναι admin
        if get_current_user_category() == 'admin':
            # Query για την εύρεση
            product = products.find_one({"_id": ObjectId(id)})
            # Αν υπάρχει το προϊόν
            if product != None:
                # Διαγραφή του
                products.delete_one({"_id": ObjectId(id)})
                # Μήνυμα επιτυχούς διαγραφής
                return Response(product['name'] + " was deleted.", status=200, mimetype='application/json')
            else:
                # Μήνυμα λάθους
                return Response("There is no such product to delete.", status=200, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("Action not allowed, user does not have admin privileges!", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

# Ανανέωση στοιχείων product βάση ID
@app.route('/updateProduct/<string:id>', methods=['POST'])
def update_product(id):
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')

    # Ελεγχος ύπαρξης session
    #uuid = request.headers.get('Authorization')
    uuid = get_current_user_uuid()

    # Αν υπάρχει κάποιο session
    if is_session_valid(uuid):
        # Αν ο χρήστης είναι admin
        if get_current_user_category() == 'admin':
            # Query για την εύρεση
            product = products.find_one({"_id": ObjectId(id)})
            # Αν υπάρχει το προϊόν, γίνεται η ανανέωση των στοιχείων του
            if product != None:
                # Πρώτη παράμετρος που δέχεται η find_one
                query = {"_id": ObjectId(id)}

                updated_information = {}
                for i in data:
                    updated_information[i] = data[i]

                new_values = {"$set": updated_information}

                # Update του document
                products.update_one(query, new_values)
                # Αναζήτηση ξανά του document για την σωστή εκτύπωση των στοιχείων
                product = products.find_one({"_id": ObjectId(id)},{"_id":0})
                # Μήνυμα επιτυχούς ανανέωσης στοιχείων φοιτητή
                msg = data['name'] + "'s information was updated: \n"+ json.dumps(product)
                return Response(msg, status=200, mimetype='application/json')
            else:
                # Μήνυμα αποτυχίας
                return Response("There is no such product", status=200, mimetype='application/json')
        else:
            # Μήνυμα λάθους
            return Response("Action not allowed, user does not have admin privileges!", status=400, mimetype='application/json')
    else:
        # Μήνυμα λάθους
        return Response("Unauthorized client error. No session initiated.", status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run()
