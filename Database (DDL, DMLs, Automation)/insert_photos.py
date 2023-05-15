import mysql.connector
import os


cnx = mysql.connector.connect(
    user='root',
    password ='toyot2002',
    host='localhost',
    database='semester_project'
)



filename = "all_the_isbn.txt"
isbn_file = open(filename, "r")
isbn_list = isbn_file.read().split("\n")
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
    
    with open(img_path, 'rb') as file:
        image_data = file.read()

    cursor = cnx.cursor()
    insert_query = "UPDATE Book SET image =%s WHERE ISBN ="+str(isbn)+";"
    image_data_blob = mysql.connector.Binary(image_data)
    insert_data = (image_data_blob,)
    cursor.execute(insert_query,insert_data)
    cnx.commit()

    cursor.close()
    i+=1
cnx.close()
