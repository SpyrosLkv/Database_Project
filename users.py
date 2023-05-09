## εδώ θα είναι ο χρήστης και όλες του οι σχέσεις
## δημιουργώ 3 αντμινς
## δημιουργω για κάθε βιβλιοθήκη τους χρήστες της
## κάνω appoint operators
import random
import hashlib
import sys
import binascii

filename = "dml_of_semester.sql"
dml = open(filename,"a",encoding="UTF-8")


first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "James", "Isabella", "Oliver", "Mia",
                "Benjamin", "Charlotte", "Elijah", "Amelia", "Lucas", "Harper", "Mason", "Evelyn", "Logan"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
               "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez",
                "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright",
                "Scott", "Green", "Baker", "Adams", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips",
                "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers"]

usernames = []

# 100 students
#  οι μαθητές είναι στην αρχή για να ξέρουμε σίγουρα κάποια id που είναι σε κάποια βιβλιοθήκη αναλογα με το id div 20
for lib in range(1,6):
    for i in range(20):
        first = random.choice(first_names)
        last = random.choice(last_names)
        username = first + last + str(random.randint(100,999))
        password = username
        if username in usernames:
            i-=1
            continue
        usernames.append(username)
        hash_password = hashlib.sha256(password.encode()).digest()
        readable_password = binascii.hexlify(hash_password).decode()
        birth_date = str(random.randint(2007,2009))+"-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
        email = username + "@gmail.com"
        role = "Student"
        status = "Active"
        library_id = lib
        # query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+role+"','"+status+"',"+str(library_id)+");\n"
        query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+status+"',"+str(library_id)+");\n"
        print(query)
        dml.write(query)



# 2 admins

for i in range(0,2):
    first = random.choice(first_names)
    last = random.choice(last_names)
    username = first + last + str(random.randint(100,999))
    password = username
    if username in usernames:
        i-=1
        continue
    usernames.append(username)
    hash_password = hashlib.sha256(password.encode()).digest()
    readable_password = binascii.hexlify(hash_password).decode()
    birth_date = str(random.randint(1980,1990))+"-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
    email = username + "@gmail.com"
    role = "Admin"
    status = "Active"
    library_id = random.randint(1,6)
    # query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+role+"','"+status+"',"+str(library_id)+");\n"    
    query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+status+"',"+str(library_id)+");\n"
    dml.write(query)



# operators

for i in range(1,6):
    first = random.choice(first_names)
    last = random.choice(last_names)
    username = first + last + str(random.randint(100,999))
    password = username
    if username in usernames:
        i-=1
        continue
    usernames.append(username)
    hash_password = hashlib.sha256(password.encode()).digest()
    readable_password = binascii.hexlify(hash_password).decode()
    birth_date = str(random.randint(1980,1990))+"-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
    email = username + "@gmail.com"
    role = "Operator"
    status = "Active"
    library_id = i
    # query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+role+"','"+status+"',"+str(library_id)+");\n"    
    query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+status+"',"+str(library_id)+");\n"
    dml.write(query)
# 20 teachers

for i in range(20):
    first = random.choice(first_names)
    last = random.choice(last_names)
    username = first + last + str(random.randint(100,999))
    password = username
    if username in usernames:
        i-=1
        continue
    usernames.append(username)
    hash_password = hashlib.sha256(password.encode()).digest()
    readable_password = binascii.hexlify(hash_password).decode()
    birth_date = str(random.randint(1980,1990))+"-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
    email = username + "@gmail.com"
    role = "Teacher"
    status = "Active"
    library_id = random.randint(1,6)
    # query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+role+"','"+status+"',"+str(library_id)+");\n"    
    query = "INSERT INTO semester_project.Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_status,users_library_id) VALUES ('"+username+"','"+readable_password+"','"+first+"','"+last+"','"+birth_date+"','"+email+"','"+status+"',"+str(library_id)+");\n"
    dml.write(query)



# create loans reservations manually

# create cards
for i in range(1,129):
    query = "INSERT INTO semester_project.Card (user_id,card_no,status) VALUES("+ str(i) +",1,'Active');\n"
    dml.write(query)

dml.close()