# θα βάλουμε τυχαία κάθε βιβλίο να έχει από 0 μέχρι 10 reviews άσχετα από αν κάποιος το έχει πάρει ή όχι

import random

filename = "all_the_isbn.txt"
isbn_file = open(filename, "r")
isbn_list = isbn_file.read().split('\n')
if isbn_list[-1] == "":
    isbn_list = isbn_list[:len(isbn_list)-2]
filename = "dml_of_semester.sql"
dml = open(filename,"a")
filename = "random_review.txt"
reviews = open(filename,"r")
reviews_text = reviews.read()

for isbn in isbn_list:
    no_of_reviews = random.randint(0,10)
    users_rev = set()
    for number in range(no_of_reviews):
        while True:
            user = random.randint(1,127)
            if user not in users_rev:
                users_rev.add(user)
                break
        start = random.randint(0,len(reviews_text)-100)
        rev = reviews_text[start:start+30]
        rev = rev.replace("'","")
        rev = rev.replace("\n","")
        rev = rev.replace("\"","")

        rating = random.randint(1,5)
        query = "INSERT INTO semester_project.Reviews (book_ISBN,user_id,likert_rating,review) VALUES ("+isbn+","+str(user)+","+str(rating)+",'"+rev+"');\n"
        dml.write(query)

dml.close()
reviews.close()
isbn_file.close()
            