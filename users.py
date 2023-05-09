## εδώ θα είναι ο χρήστης και όλες του οι σχέσεις
## δημιουργώ 3 αντμινς
## δημιουργω για κάθε βιβλιοθήκη τους χρήστες της
## κάνω appoint operators
import random
import secrets

filename = "dml_of_semester.sql"
dml = open(filename,"a",encoding="UTF-8")


first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "James", "Isabella", "Oliver", "Mia",
                "Benjamin", "Charlotte", "Elijah", "Amelia", "Lucas", "Harper", "Mason", "Evelyn", "Logan"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
               "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez",
                "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright",
                "Scott", "Green", "Baker", "Adams", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips",
                "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers"]

for i in range(1,6):
    first = random.choice(first_names)
    last = random.choice(last_names)
    username = first + last
