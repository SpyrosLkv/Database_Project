## εδω θα δημιουργήσω τις βιβλιοθήκες και τα βιβλία που τους ανήκουν (5 βιβλιοθήκες)
## θα πάρω το σύνολο των isbn και θα τα βάλω σε κάθε βιβλιοθήκη με πιθανόητα 70%
## θα δημιουργήσω τις σχέσεις Lib owns book
## θα αποθηκεύσω τα ISBN που έχει κάθε βιβλιοθήκη

## να βάλω και τηλέφωνα ή δεν ξέρω και εγώ τι

filename = ""

file = open(filename, "r")
ISBN_list = file.read();
ISBN_list = ISBN_list.split("\n")

names = ["St Johns Catholic School", "Hogwarts", "Xavier's School for Gifted Children", "1ο Γελ Παλλήνης", "Βιβλιοθήκη Ήμμυ"]
addresses = ["285 Fulton St","241 Baker's Street","300 E St", "Λεωφ. Μαραθώνος, 153 51", "Κτίρια Ηλεκτρολόγων, ΕΜΠ"]
town = ["New York","London","Washington","Αθήνα","Αθήνα"]
emails
for index in range(5):
    