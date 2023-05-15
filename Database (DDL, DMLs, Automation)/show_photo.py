import mysql.connector
from mysql.connector import Error

try:
    # Connect to the database
    cnx = mysql.connector.connect(
        user='root',
        password='toyot2002',
        host='localhost',
        database='semester_project'
    )

    query = "SELECT image FROM Book WHERE ISBN ="+str(9789603322092)+";"
    cursor = cnx.cursor()
    cursor.execute(query)
    photo_data = cursor.fetchone()[0]

    with open('test.png', 'wb') as f:
        f.write(photo_data)

    cursor.close()
    cnx.close()
except Error as e:
    print(e)