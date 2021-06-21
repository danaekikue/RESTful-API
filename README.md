# Δεύτερη Εργασία Πληροφοριακών Συστημάτων

## Table of contents

> * [Δεύτερη Εργασία Πληροφοριακών Συστημάτων](#title--repository-name)
>   * [Table of contents](#table-of-contents)
>   * [About / Synopsis](#about--synopsis)
>   * [Requirements](#requirements)
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
 
 ## Requirements

###### Εγκατάσταση dependencies

```
pip install -r requirements.txt
```

Προαπαραίτητη η ύπαρξη και η εγκατάσταση της [Python](https://www.python.org/downloads/)  .

## Setup
Τα απαρίτητα βήματα που πρέπει να γίνουν για την δημουργία του docker container και του image, με το students.json περασμένο.
Προαπαραίτητη η ύπαρξη και η εγκατάσταση του [Docker](https://hub.docker.com/).
Για την δυνατότητα ελέγχου της υλοποίησης της εφαρμογής, θα χρειαστεί πρώτα να γίνει η δημιουργία ενός Docker Container.

###### Δημιουργία Docker Container
Στο Powershell/Terminal γράφουμε τα παρακάτω:

```
docker pull mongo
docker run -d -p 27017:27017 --name mongodb mongo:4.0.4
docker exec -it mongodb mongo
```
Τώρα βρισκόμαστε στο περιβάλλον του Mongo Shell. Εδώ γράφουμε:
```
use InfoSys
```
Φεύγουμε από το περιβάλλον με CTR+C.
Μπαίνουμε μέσω του CMD στον φάκελο data. Εκεί τρέχουμε το παρακάτω:
```
docker cp students.json mongodb:/students.json
docker exec -it mongodb mongoimport --db=InfoSys --collection=Students --file=students.json
```
Ελέγχουμε εάν το docker container τρέχει. Εάν όχι το ξεκινάμε με:

```
docker start mongodb
```

###### Τρέξιμο εφαρμογής
Στον φάκελο που υπάρχει το app.py εκτελούμε:
```
python app.py
```
Και τώρα μέσω του [Postman](https://www.postman.com/) στην διεύθνση http://127.0.0.1:5000/<αντίστιχο link>, μπορούμε να κάνουμε δοκιμές.


## Tasks

- Δημιουργία νέου χρήστη. Πληροφορίες χρήστη:  username, password
- Login στο σύστημα με ένα username και passowrd που υπάρχουν στην βάση δεδομένων
- Αναζήτηση ύπαρξης φοιτητή βάσει email
- Αναζήτηση όλων των φοιτητών που είναι 30 χρονών 
- Αναζήτηση όλων των φοιτητών που είναι 30 ετών και άνω
- Αναζήτηση φοιτητή βάσει email και ο οποίος έχει δηλώσει κατοικία
- Διαγραφή φοιτητή
- Εισαγωγή μαθημάτων και βαθμών του σε φοιτητή βάσει email
- Αναζήτηση φοιτητή που έχει περασμένα μαθήματα ( Βαθμολογία άνω του 5 )



## Example Usage
Ο κώδικας είναι πλήρως σχολιασμένος για περισσότερες λεπτομέρειες του τρόπου υλοποίησης.
Σε κάθε ερώτημα αναφέρονται παραδείγματα από τρεξίματα του κώδικα για όλες τις περιπτώσεις.

**email** : Το email προς αναζήτηση. Όπου υπάρχει, αντικατάσταση με το email που θέλουμε να δοκιμάσουμε. Τα email αυτά, για να έχουμε σωστά αποτελέσματα, προέρχνται από το students.json

### Ερώτημα 1 /createUser
POST request URL: http://127.0.0.1:5000/createUser
<br/>Δέχεται στο body του request ενα json της μορφής:

```
{
    "username": "danai",
    "password": "12343"
}
```
Επιστρέφει: 
```
danai was added to the MongoDB
```

Αν υπάρχει ήδη ένας χρήστης με αυτό το όνομα τότε επιστρέφει: 
```
A user with the given username already exists
```

### Ερώτημα 2 /login
POST request URL: http://127.0.0.1:5000/login

Δέχεται στο body του request ενα json της μορφής:

```
{
    "username": "danai",
    "password": "12343"
}
```

Σε αυτήν την φάση δημιουργείται επίσης και ένα uuid για το session που βρίσκεται σε λειτουργία μέσω αυτού του ερωτήματος 

Επιστρέφει: 
```
Session initiated. 
Welcome danai. 
Data: {
    "uuid": "fe836f19-b666-11eb-8a85-2cf05d7962e8",
    "username": "danai"
}
```

Αν δεν υπάρχει αυτός χρήστης με τα παραπάνω στοιχεία, επιστρέφει: 
```
Wrong username or password.
```

### Ερώτημα 3 /getStudent/<string:email>
GET request URL: http://127.0.0.1:5000/getStudent/email

Δέχεται σαν argument το email του φοιτητή που αναζητούμε στο link

```
http://127.0.0.1:5000/getStudent/mortonfitzgerald@ontagene.com
```

Επίσης δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν υπάρχει session και υπάρχει ο φοιτητής με το email που δόθηκε, επιστρέφει τις πληροφορίες του:
```
Morton Fitzgerald's information: {
    "name": "Morton Fitzgerald",
    "email": "mortonfitzgerald@ontagene.com",
    "yearOfBirth": 1997,
    "address": [
        {
            "street": "Jardine Place",
            "city": "Lowgap",
            "postcode": 18330
        }
    ],
    "courses": [
        {
            "Information Systems": 10,
            "Statistics": 3,
            "Web Programming": 8
        }
    ]
}
```

Αν δεν υπάρχει φοιτητής με αυτό το email τότε επιστρέφει: 
```
There is no student associated with the email ffsdff@ontagene.com
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 4 /getStudents/thirties
GET request URL: http://127.0.0.1:5000/getStudents/thirties


Δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν έχει υπάρχει session και υπάρχουν φοιτητές που είναι 30 ετών, επιστρέφει τις πληροφορίες τους:
```
There are 2 students that are 30: [
    {
        "name": "Browning Rasmussen",
        "email": "browningrasmussen@ontagene.com",
        "yearOfBirth": 1991,
        "address": [
            {
                "street": "Doone Court",
                "city": "Cuylerville",
                "postcode": 17331
            }
        ]
    },
    {
        "name": "Bennett Baker",
        "email": "bennettbaker@ontagene.com",
        "yearOfBirth": 1991,
        "gender": "male"
    }
]
```

Αν δεν υπάρχουν φοιτητές που να είναι 30 ετών, τότε επιστρέφει: 
```
No students of the age of 30 exist
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 5 /getStudents/oldies
GET request URL: http://127.0.0.1:5000/getStudents/oldies

Δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν έχει υπάρχει session και υπάρχουν φοιτητές που είναι άνω των 30 ετών, επιστρέφει τις πληροφορίες τους:
```
There are 115 students that are over 30: [
    {
        "name": "Tanner Wilson",
        "email": "tannerwilson@ontagene.com",
        "yearOfBirth": 1962,
        "address": [
            {
                "street": "Halsey Street",
                "city": "Greenwich",
                "postcode": 13832
            }
        ],
        "courses": [
            {
                "Information Systems": 8,
                "Statistics": 9,
                "Web Programming": 10
            }
        ]
    },
    {
        "name": "Lavonne Leon",
        "email": "lavonneleon@ontagene.com",
        "yearOfBirth": 1967,
        "address": [
            {
                "street": "Chauncey Street",
                "city": "Chase",
                "postcode": 12663
            }
        ],
        "courses": [
            {
                "Information Systems": 4,
                "Statistics": 3,
                "Web Programming": 5
            }
        ]
    },
    ...
```

Αν δεν υπάρχουν φοιτητές που να είναι πάνω των 30 ετών, τότε επιστρέφει: 
```
No students over the age of 30 exist
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 6 /getStudentAddress/<string:email>
GET request URL: http://127.0.0.1:5000/getStudentAddress/email

Δέχεται σαν argument το email του φοιτητή που αναζητούμε στο link

```
http://127.0.0.1:5000/getStudentAddress/dorthycobb@ontagene.com
```

Επίσης δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν υπάρχει session, υπάρχει ο φοιτητής με το email που δόθηκε και έχει δηλώσει κατοικία, επιστρέφει τις πληροφορίες του:
```
Morton Fitzgerald's address information: {
    "name": "Morton Fitzgerald",
    "street": "Jardine Place",
    "postcode": 18330
}
```

Αν δεν υπάρχει φοιτητής με αυτό το email τότε επιστρέφει: 
```
There is no student associated with the email fg@ontagene.com
```

Αν δεν έχει δηλώσει κατοικία ο φοιτητής, τότε επιστρέφει: 
```
There is no address associated with Dorthy Cobb
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 7
DEL request URL: http://127.0.0.1:5000/deleteStudent/email

Δέχεται σαν argument το email του φοιτητή που αναζητούμε στο link

```
http://127.0.0.1:5000/getStudentAddress/dorthycobb@ontagene.com
```

Επίσης δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν υπάρχει session και υπάρχει ο φοιτητής με το email που δόθηκε, επιστρέφει μήνυμα επιτυχίας:
```
Schwartz Butler was deleted.
```

Αν δεν υπάρχει φοιτητής με αυτό το email τότε επιστρέφει: 
```
There is no student associated with the email ddffg@ontagene.com
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 8
PATCH request URL: http://127.0.0.1:5000/addCourses/email

Δέχεται σαν argument το email του φοιτητή που αναζητούμε στο link

```
http://127.0.0.1:5000/getStudentAddress/mortonfitzgerald@ontagene.com
```

Επίσης δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν υπάρχει session και υπάρχει ο φοιτητής με το email που δόθηκε, επιστρέφει μήνυμα επιτυχίας:
```
Lavonne Leon's information was updated: 
Information Systems: 8
Statistics: 9
Web Programming: 10
```

Αν δεν υπάρχει φοιτητής με αυτό το email τότε επιστρέφει: 
```
There is no student associated with the email ddffg@ontagene.com
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
```

### Ερώτημα 9
GET request URL: http://127.0.0.1:5000/getPassedCourses/email

Δέχεται σαν argument το email του φοιτητή που αναζητούμε στο link

```
http://127.0.0.1:5000/getStudentAddress/tannerwilson@ontagene.com
```

Επίσης δέχεται στον header το uuid του session που ξεκίνησε μέσω του ερωτήματος 2. Το uuid αυτό πρέπει να ανατεθεί σε ένα header με Key: Authorization kai Value: το uuid ( η διαδικασία αυτή έχει γίνει μέσω της χρήσης του Postman που παρέχει τέτοια δυνατότητα )

Αν υπάρχει session, υπάρχει ο φοιτητής με το email που δόθηκε και έχει μαθήματα που έχει περάσει, επιστρέφει:
```
Here are the grades for the subjects that Tanner Wilson passed: {
    "Information Systems": 8,
    "Statistics": 9,
    "Web Programming": 10
}
```

Αν δεν έχει έχει μαθήματα που έχει περάσει, τότε επιστρέφει: 
```
Lavonne Leon has not passed any subjects
```

Αν δεν έχει courses, τότε επιστρέφει: 
```
There are no courses associated with Mcgowan Robinson
```

Αν δεν υπάρχει φοιτητής με αυτό το email τότε επιστρέφει: 
```
There is no student associated with the email fg@ontagene.com
```

Αν δεν υπάρχει session που να τρέχει, τότε επιστρέφει: 
```
User does not exist. Unauthorized client error
