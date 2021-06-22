# Δεύτερη Εργασία Πληροφοριακών Συστημάτων

## Table of contents

> * [Δεύτερη Εργασία Πληροφοριακών Συστημάτων](#title--repository-name)
>   * [Table of contents](#table-of-contents)
>   * [About / Synopsis](#about--synopsis)
>   * [Setup](#setup)
>   * [Tasks](#tasks)
>   * [Example Usage](#example-usage)

## About / Synopsis

Εργασία πάνω στην υλοποίηση ενός RESTful API, για το μάθημα των Πληροφοριακών Συστημάτων του Πανεπιστημίου Πειραιώς.
 <br/>Φτιαγμένο με Python 3.9.2, Flask API και MongoDB.
 <br/>Flask : Python Based mini-Webframework
 <br/>MongoDB : Database Server
 <br/>Pymongo : Database Connector ( For creating connectiong between MongoDB and Flask )
 <br/>Yλοποιημένο σε Docker περιβάλλον.
 <br/>Για τον έλεγχο της υλοποίησης χρησιμοποιήθηκε το [Postman](https://www.postman.com/)  
 


Προαπαραίτητη η ύπαρξη και η εγκατάσταση της [Python](https://www.python.org/downloads/)  .

## Setup


###### Τρέξιμο εφαρμογής

1) Clone ή download το repository.
2) Στον φάκελο που υπάρχει το docker-compose.yml εκτελούμε:
```
docker-compose up
```
Και τώρα μέσω του [Postman](https://www.postman.com/) στην διεύθνση http://127.0.0.1:5000/<αντίστιχο link>, μπορούμε να κάνουμε δοκιμές. Για διευκόληνση, στον φάκελο Postman Collections, υπάρχουν τρία αρχεία που αποτελούν collection προς εισαγωγή στο postman workspace σας. 

- Ένα για τις κοινές ενέργειες, όπως θα δείτε παρακάτω
- Ένα για τις ενέργειες ενός απλού χρήστη 
- Ένα για τις ενέργειες ενός admin

Επίσης για την δοκιμή με την λειτουργία ενός admin, πρέπει μέσω MongoDb Compass, μετά την εισαγωγή ενός χρήστη, να γίνει η αλλαγή της κατηγορίας του από user σε admin.


## Tasks
Υπάρχουν δύο κατηγορίες χρηστών με διαφορετικές δυνατότητες και ενέργειες. Έχουμε τον απλό χρήστη και τον admin. Υπάρχουν όμως και δύο ενέργειες ανεξάρτητες του είδου χρήστη.

### Κοινές ενέργειες
- Δημιουργία νέου χρήστη. Πληροφορίες χρήστη:  username, password, category
- Login στο σύστημα με username και passowrd που υπάρχουν στην βάση δεδομένων

### Απλός χρήστης
- Διαγραφή λογαριασμού ενός απλού χρήστη
- Αναζήτηση προϊόντων με βάση: 
  a) Ονομα
  b) Κατηγορία
  c) Μοναδικό ID
- Προσθήκη προϊόντος στο καλάθι αγορών
- Εμφάνιση των περιεχομένων του καλαθιού αγορών
- Αφαίρεση προϊότνος από το καλάθι αγορών
- Αγορά προϊόντων καλαθιού
- Εμφάνιση ιστορικού παραγγελιών

### Admin
- Προσθήκη προϊόντος στο σύστημα
- Διαγραφή προϊόντος από το σύστημα
- Ανανέωση πληροφοριών κάποιου προϊόντος στο σύστημα


## Example Usage
Ο κώδικας είναι πλήρως σχολιασμένος για περισσότερες λεπτομέρειες του τρόπου υλοποίησης.
Σε κάθε ερώτημα αναφέρονται παραδείγματα από τρεξίματα του κώδικα για όλες τις περιπτώσεις.

### /createUser
POST request URL: http://127.0.0.1:5000/createUser
<br/>Δέχεται στο body του request ενα json της μορφής:

```
{
    "name": "Jane Doe",
    "email": "janedoe@dsmarket.com",
    "password": "securePassword"
}
```
Επιστρέφει: 
```
Jane Doe, you have successfully signed up.
```

Αν υπάρχει ήδη ένας χρήστης με αυτό το όνομα τότε επιστρέφει: 
```
A user with the given username already exists
```

### /login
POST request URL: http://127.0.0.1:5000/login

Δέχεται στο body του request ενα json της μορφής:

```
{
    "email": "janedoe@dsmarket.com",
    "password": "securePassword"
}
```

Σε αυτήν την φάση δημιουργείται επίσης και ένα uuid για το session που βρίσκεται σε λειτουργία μέσω αυτού του ερωτήματος 

Επιστρέφει: 
```
Session initiated. 
Welcome to DSMarket Jane Doe 
Data: {
    "uuid": "bc6dab44-d35a-11eb-b616-001a7dda7115",
    "email": "janedoe@dsmarket.com"
}
```

Αν δεν υπάρχει ο χρήστης με τα παραπάνω στοιχεία, επιστρέφει: 
```
Wrong username or password.
```

*Για όλα τα υπόλοιπα endpoints εάν δεν έχει γίνει η σύνδεση ενός χρήστη στο σύστημα ( είτε απλού χρήστη είτε admin ), τότε θα βγάλει αντίστοιχο μήνυμα λάθους. Το μήνυμα αυτό είναι το παρακάτω:*

```
Unauthorized client error. No session initiated.
```

*Επίσης για τα endpoints ενός απλού χρήστη, εάν ένας admin επιχειρήσει να εκτελέσει κάποια λειτουργία, θα του εμφανιστεί το παρακάτω μήνυμα:*
```
You are logged in with your admin account. Please switch to a normal user account.
```

*Αντίστοιχα για τα endpoints ενός admin, εάν ένας απλός χρήστης επιχειρήσει να εκτελέσει κάποια λειτουργία, θα του εμφανιστεί το παρακάτω μήνυμα:*
```
Action not allowed, user does not have admin privileges!
```

## Απλός χρήστης


### /delete_account
GET request URL: http://127.0.0.1:5000/deleteAccount



Αν υπάρχει session και ο χρήστης ανοίκει στην κατηγορία του user, τότε διαγράφεται επιτυχώς ο λογαριασμός του. Επιστρέφεται μήνυμα

```
The account associated with the email test@dsmarket.com was successfully deleted.
```

Στο συγκεκριμένο endpoint, το email παίρνεται από τα δεδομένα του χρήστη ( uuid και email ) που έχουν αποθηκευτεί για το τρέχων session.
Με βάση αυτό το email γίνεται η διαγραφή του από την βάση, καθώς και η εκαθάριση του user_sessions, για να μην υπάρχει πλέον πρόσβαση στο σύστημα. 


Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /findProduct/name/<string:name>
GET request URL: http://127.0.0.1:5000/findProduct/name/<string:name>

**<string:name>** : Το όνομα του προϊόντος προς αναζήτηση. Όπου υπάρχει, αντικατάσταση με το όνομα που θέλουμε να αναζητήσουμε.

Μέσω του usser_sessions που αποθηκεύει το uuid και το email του τρέχων χρήστη, παίρνουμε και ελέγχουμε το uuid του session.

Αν έχει υπάρχει session και υπάρχουν προϊόντα με το όνομα που έχουμε δώσει, επιστρέφει τις πληροφορίες τους:
```
Products matching 'Milk' : [
    {
        "_id": "60cb78a56ff56e024d7a8cde",
        "name": "Milk",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 44
    },
    {
        "_id": "60cb7a406ff56e024d7a8ce0",
        "name": "Milk 2%",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 98
    },
    {
        "_id": "60cb7b8fa27c91e90e53505f",
        "name": "Delta Milk",
        "price": 2.5,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 101
    }
]
```

Αν δεν υπάρχουν προϊόντα, τότε επιστρέφει: 
```
There is no Product associated with the name Cherry
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /findProduct/category/<string:category>
GET request URL: /findProduct/category/<string:category>

**<string:category>** : H κατηγορία του προϊόντος προς αναζήτηση. Όπου υπάρχει, αντικατάσταση με την κατηγορία που θέλουμε να αναζητήσουμε.

Μέσω του usser_sessions που αποθηκεύει το uuid και το email του τρέχων χρήστη, παίρνουμε και ελέγχουμε το uuid του session.

Αν έχει υπάρχει session και υπάρχουν προϊόντα με την κατηγορία που έχουμε δώσει, επιστρέφει τις πληροφορίες τους:
```
Products matching 'dairy' : [
    {
        "_id": "60ccbe048febbc431ca1a3be",
        "name": "Eggs 6",
        "price": 0.8,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 216
    },
    {
        "_id": "60ccbdf38febbc431ca1a3bd",
        "name": "Yogurt",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 89
    },
    {
        "_id": "60ccbde28febbc431ca1a3bc",
        "name": "Greek Yogurt",
        "price": 1.8,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 19
    },
    {
        "_id": "60cb78a56ff56e024d7a8cde",
        "name": "Milk",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 44
    },
    {
        "_id": "60cb7a406ff56e024d7a8ce0",
        "name": "Milk 2%",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 98
    },
    {
        "_id": "60cb7b8fa27c91e90e53505f",
        "name": "Delta Milk",
        "price": 2.5,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 101
    }
]
```

Αν δεν υπάρχουν προϊόντα, τότε επιστρέφει: 
```
There is no Product associated with the category dairy.
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /findProduct/ID/<string:id>
GET request URL: http://127.0.0.1:5000/findProduct/ID/<string:id>

**<string:id>** : Το id του προϊόντος προς αναζήτηση. Όπου υπάρχει, αντικατάσταση με  το id που θέλουμε να αναζητήσουμε.

Μέσω του usser_sessions που αποθηκεύει το uuid και το email του τρέχων χρήστη, παίρνουμε και ελέγχουμε το uuid του session.

Αν έχει υπάρχει session και υπάρχει προϊόν με το id που έχουμε δώσει, επιστρέφει τις πληροφορίες τους:
```
The product with the ID '60cb7b8fa27c91e90e53505f' is the following: {
    "name": "Delta Milk",
    "price": 2.5,
    "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
    "category": "dairy",
    "stock": 101
}
```

Αν δεν υπάρχουν προϊόντα, τότε επιστρέφει: 
```
There is no Product associated with the id ddffghhgf.
```

Αν το ID δεν έχει την σωστή μορφή, βγάζει μήνυμα λάθους.
```
The ID you provided is not correct. Please try again.
```


Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /addToCart/<string:id>/<int:quantity>
GET request URL: http://127.0.0.1:5000/<string:id>/<int:quantity>

Δέχεται σαν argument το id που θέλει να αγοράσει ο χρήστης, καθώς και την ποσότητα που θέλει.

```
http://127.0.0.1:5000/addToCart/60cb7b8fa27c91e90e53505f/2
```

Αν υπάρχει session γίνεται η προσθήκη στο καλάθι του προϊόντος με βάση το ID. Στο καλάθι υπάρχει και το συνολικό κόστος, το οποίο ανανεώνεται κάθε φορά που προστίθεται ένα προϊόν. Επιτυχές αποτέλεσμα:
```
Cart was updated with 2 items of Delta Milk. 
 Your cart now includes: [
    {
        "_id": "60cb7b8fa27c91e90e53505f",
        "name": "Delta Milk",
        "price": 2.5,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 101,
        "quantity": 2
    }
]
 Total cost is: 5.00€
```

Αν το απόθεμα είναι λιγότερο από την ποσότητα που ζητήθηκε,εμφανίζεται μήνυμα λάθους.
```
We are sorry but the quantity you are asking for is greater than our stock of this product.
Current stock of Delta Milk is: 101
```

Αν το ID δεν έχει την σωστή μορφή, βγάζει μήνυμα λάθους.
```
The ID you provided is not correct. Please try again.
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /showCart
GET request URL: http://127.0.0.1:5000/showCart


Αν υπάρχει session, επιστρέφει τα περιεχόμενα του καλαθιού και το κόστος όλων των προϊόντων
```
Your cart includes: [
    {
        "_id": "60cb7b8fa27c91e90e53505f",
        "name": "Delta Milk",
        "price": 2.5,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 101,
        "quantity": 2
    },
    {
        "_id": "60ccbdf38febbc431ca1a3bd",
        "name": "Yogurt",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 89,
        "quantity": 2
    }
]
 Total cost is: 7.40€
```

Αν το καλάθι είναι άδειο: 
```
The cart is empty.
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /removeFromCart/<string:id>
GET request URL: http://127.0.0.1:5000//removeFromCart/<string:id>

Δέχεται σαν argument το id του προϊόντος προς διαγραφή που αναζητούμε στο link

```
http://127.0.0.1:5000/removeFromCart/60cb7b8fa27c91e90e53505f
```


Αν υπάρχει session, επιστρέφει το ανανεώμενο περιεχόμενο του καλαθιού και το κόστος όλων των προϊόντων
```
Your cart includes: [
    {
        "_id": "60ccbdf38febbc431ca1a3bd",
        "name": "Yogurt",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 89,
        "quantity": 2
    }
]
 Total cost is: 2.40€
```

Γίνεται και η διαδοχική διαγραφή προϊόντων. Όταν πια το καλάθι είναι άδειο, εμφανίζεται αντίστοιχο μήνυμα:

```
The cart doens't have any more items to remove
```

Αν δεν έχει εξαρχής προϊόντα:
```
The cart is empty
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /checkOut/<int:card_num>

GET request URL: http://127.0.0.1:5000/checkOut/<int:card_num>

Δέχεται σαν argument τον αριθμό κάρτας για την πληρωμή των προϊόντων.

```
http://127.0.0.1:5000/checkOut/1234567891234567
```


Αν υπάρχει session και ο αριθμός της κάρτας είναι 16 ψηφία, επιστρέφει την απόδειξη της πληρωμής:
```
Thank you for your purchase. 
Receipt for purchase:
 Total Cost: 8.00€
 Products bought: [
    {
        "_id": "60ccbdf38febbc431ca1a3bd",
        "name": "Yogurt",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 87,
        "quantity": 2
    },
    {
        "_id": "60d05cdf910377f7d7732a77",
        "name": "Bananas",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "fruit",
        "stock": 150,
        "quantity": 3
    },
    {
        "_id": "60cb78a56ff56e024d7a8cde",
        "name": "Milk",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 44,
        "quantity": 1
    },
    {
        "cost": "8.00"
    }
]
```

Αν ο αριθμός της κάρτας δεν είναι 16 ψηφία: 

```
The input of your card number is not 16 digits long. Please try again.
```

Αν δεν έχει το καλάθι εξαρχής προϊόντα:
```
The cart is empty
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```


### /viewHistory

GET request URL: http://127.0.0.1:5000/viewHistory


Αν υπάρχει session και ο συγκεκριμένος χρήστης έχει ιστορικό παραγγελιών, εμφανίζεται το ιστορικό του:
```
Thank you for your purchase. 
Receipt for purchase:
 Total Cost: 8.00€
 Products bought: [
    {
        "_id": "60ccbdf38febbc431ca1a3bd",
        "name": "Yogurt",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "dairy",
        "stock": 87,
        "quantity": 2
    },
    {
        "_id": "60d05cdf910377f7d7732a77",
        "name": "Bananas",
        "price": 1.2,
        "description": "gfdgsdjkhjkgfgsdfgdsg",
        "category": "fruit",
        "stock": 150,
        "quantity": 3
    },
    {
        "_id": "60cb78a56ff56e024d7a8cde",
        "name": "Milk",
        "price": 2.0,
        "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
        "category": "dairy",
        "stock": 44,
        "quantity": 1
    },
    {
        "cost": "8.00"
    }
]
```

Αν ο δεν έχει κάνει καμία παραγγελία και δεν υπάρχει ιστορικό, του εμφανίζεται αντίστοιχο μήνυμα:

```
You haven't made any orders yet.
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```



## Admin

### /addProduct

GET request URL: http://127.0.0.1:5000/addProduct

Δέχεται στο body του request ενα json της μορφής:

```
{
    "name": "Apple", 
    "price": 4.50, 
    "description": "Delicious biological fruit",
    "category": "fruit", 
    "stock": 150
}
```

Αν υπάρχει session και δεν υπάρχει ήδη προϊόν με το όνομα που δίνεται, εμφανίζεται το παρακάτω μήνυμα: 
```
The product with the name 'Apple' was added: {
    "name": "Apple",
    "price": 4.5,
    "description": "Delicious biological fruit",
    "category": "fruit",
    "stock": 150
}
```

Αν ήδη υπάρχει τέτοιο προϊόν:

```
The product with the name 'Apple' already exists
```


Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /deleteProduct/<string:id>

GET request URL: http://127.0.0.1:5000/deleteProduct/60d210c965e5759937b32487


Αν υπάρχει session και υπάρχει ήδη προϊόν με το όνομα που δίνεται, εμφανίζεται το παρακάτω μήνυμα: 
```
Apple was deleted.
```

Αν δεν υπάρχει τέτοιο προϊόν:

```
There is no such product to delete.
```


Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```





Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```

### /updateProduct/<string:id>

GET request URL: http://127.0.0.1:5000/updateProduct/60cb78a56ff56e024d7a8cde


Αν υπάρχει session και υπάρχει ήδη προϊόν με το ID που δίνεται, εμφανίζεται το παρακάτω μήνυμα: 
```
Milk's information was updated: {
    "name": "Milk",
    "price": "3",
    "description": "Produced with care from our 700 producers throughout Greece, from cows fed cows fed on clover, corn, barley and other plant feeds, with interactive packaging through Shazam and Augmented Reality, 7-day shelf life",
    "category": "dairy",
    "stock": 43
}
```

Αν δεν υπάρχει τέτοιο προϊόν:

```
There is no such product.
```


Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
Unauthorized client error. No session initiated.
```


