import mysql.connector
from mysql.connector import Error
import base64
import os

try:
    # Connect to the database
    cnx = mysql.connector.connect(
        user='root',
        password='toyot2002',
        host='localhost',
        database='semester_project'
    )
#  ΕΔΏ ΒΑΖΕΙΣ ΤΟ ΙΣΒΝ ΠΟΥ ΘΕΣ ΝΑ ΔΕΙΣ ΤΗΝ ΦΩΤΟΓΡΑΦΙΑ ΤΟΥ
    query = "SELECT image FROM Book WHERE ISBN ="+str(1234567890123)+";"
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if result is None:
        print("nothing")
    file_bytes = base64.b64decode(result)
    with open('test.png', 'wb') as f:
        f.write(file_bytes)

    cursor.close()
    cnx.close()
except Error as e:
    print(e)

temp_dir = 'temp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
filename = "cover.png"
temp_file_path = os.path.join(temp_dir, filename)
with open(temp_file_path, 'wb') as file:
    file.write(file_bytes)