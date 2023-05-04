## εδω θα δημιουργήσω τις βιβλιοθήκες και τα βιβλία που τους ανήκουν (5 βιβλιοθήκες)
## θα πάρω το σύνολο των isbn και θα τα βάλω σε κάθε βιβλιοθήκη με πιθανόητα 70%
## θα δημιουργήσω τις σχέσεις Lib owns book
## θα αποθηκεύσω τα ISBN που έχει κάθε βιβλιοθήκη

## να βάλω και τηλέφωνα ή δεν ξέρω και εγώ τι
import random
filename = ""

file = open(filename, "r")
ISBN_list = file.read();
ISBN_list = ISBN_list.split("\n")

filename = "dml_of_semester.sql"
dml = open(filename,"a", encoding="UTF-8")

names = ["St Johns Catholic School", "Hogwarts", "Xavier's School for Gifted Children", "1ο Γελ Παλλήνης", "Βιβλιοθήκη Ήμμυ"]
addresses = ["285 Fulton St","241 Baker's Street","300 E St", "Λεωφ. Μαραθώνος, 153 51", "Κτίρια Ηλεκτρολόγων, ΕΜΠ"]
town = ["New York","London","Washington","Αθήνα","Αθήνα"]
emails = ["StJohns@gmail.com","LevioSA@hotmai.com","Mutant101@yahoo.com","1oGELPALLINIS@gmail.com","DonteEstaLaBibliotexa@gmail.com"]
for index in range(5):
    query = "INSERT INTO semester_project.School_Library (name, address, town, email) VALUES (\"" + names[index] + "\",\"" + addresses[index] +"\",\"" + town[index] +"\",\""+ emails[index] +"\");\n"
    dml.write(query)

for index in range(1,6):
    for ISBN in ISBN_list:
        rand_num = random.random()
        total = random.randint(2,10);
        avail = total
        if rand_num < 0.7:
            query = "INSERT ON semester_project.Lib_Owns_Book (book_ISBN,library_id,total_copies,available_copies) VALUES (" + str(ISBN) + "," + str(index) + "," + total + "," + avail + ");\n"
            dml.write(query)

phone_nos = ["6954363464","2103753456","6923459878","2133859677","2180267385","6996454323","2220009998","2068433987","6920347958","2103890545"];

i = 0
for school in range(1,6):
    no_of_phones = random.choice([1,2])
    for j in range(no_of_phones):
        query = "INSERT ON semester_project.School_Phone_No (phone_no,library_id) VALUES (" + phone_nos[i] + "," + str(school) +");\n"
        dml.write(query)
        i+=1
