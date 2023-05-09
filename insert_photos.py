from PIL import Image
import os


filename = "all_the_isbn.txt"

file = open(filename,'r')

filename = "dml_for_photos.sql"

dml = open(filename,"w")
dml.truncate(0)

isbn_list = file.read().split("\n")
if isbn_list[-1] == "":
    isbn_list = isbn_list[:len(isbn_list)-2]

i = 0
for isbn in isbn_list:
    '''
    Εδώ πρέπει να γράψετε το path που έχουν οι φωτογραφίες στον υπολογιστή στον οποίο τρέχετε
    Αυτό δεν ξέρω κατα πόσο θα λειτουργήσει
    '''
    cwd = os.getcwd()
    cwd =cwd.replace("\\","/")

    img_path = cwd + "/images/image"+str(i)+".png"
    img_size = os.path.getsize(img_path)
    
    if img_size >= 262000:
        i+=1
        continue
    
    query = "UPDATE semester_project.Book SET image = LOAD_FILE('"+ img_path +"') WHERE ISBN ="+ isbn +";\n"
    dml.write(query)
    i+=1
