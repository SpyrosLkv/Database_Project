from flask import Flask, render_template, request, json, redirect, session, jsonify
from flask_mysqldb import MySQL
import hashlib
import binascii
from datetime import datetime, timedelta
import os
import mimetypes
import base64

app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toyot2002'
app.config['MYSQL_DB'] = 'semester_project'
app.config['MYSQL_CONNECT_TIMEOUT'] = 300

app.secret_key = 'VideoTapes'

mysql = MySQL(app)

''' Κώδικας για το Hashing  του password '''
def HashPass(original_text):
    hash_password = hashlib.sha256(original_text.encode()).digest()
    answer = binascii.hexlify(hash_password).decode()
    return answer

Home_for_role = {'Student': '/Studenthome',
                 'Teacher': '/Teacherhome',
                 'Operator': '/Operatorhome',
                 'Admin': '/Adminhome'}
Html_for_role = {'Student': 'Studenthome.html',
                 'Teacher': 'Teacherhome.html',
                 'Operator': 'Operatorhome.html',
                 'Admin': 'Adminhome.html'}   




''' main '''
@app.route("/")
def main():
    return render_template('index.html')

''' κώδικας για την εγγραφή '''
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def signUp():
    # create user code will be here
    try:
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        username = request.form['inputUserName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        birth_date = request.form['inputBirth_Date']
        user_role = request.form['inputUser_Role']
        # library_id = int(request.form['inputLibrary'])
        library_name = request.form.get("dropdown")

        if first_name and last_name and _email and username and _password:
            with mysql.connection.cursor() as cursor:
                query = "select username from Users where username = %s;"
                params = (username,)
                cursor.execute(query,params)
                data = cursor.fetchall()
                query = "select username from Pending_Registrations where username = %s;"
                cursor.execute(query,params)
                data2 = cursor.fetchall()

                if len(data) == 0 and len(data2) == 0:
                    query = "select * from School_Library where name = %s;"
                    params = (library_name,)
                    cursor.execute(query,params)
                    data = cursor.fetchall()
                    library_id = int(data[0][0])
                    query = "insert into Pending_Registrations (username,password_hashed,first_name,last_name,birth_date,email,user_role,library_id) values (%s,%s,%s,%s,%s,%s,%s,"+str(library_id)+");"
                    params = (username,HashPass(_password),first_name,last_name,birth_date,_email,user_role)
                    cursor.execute(query,params)
                    mysql.connection.commit()

                    return json.dumps({'message': 'User created successfully !', 'redirect_url': '/'})
                else:
                    return json.dumps({'error': "the username already exists"})
            
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

    # except Exception as e: (Should really have a try: catch: here, will work on it..12/05)

''' κώδικας για το Login '''
@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/api/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputUserName']
        _password = request.form['inputPassword']
        if _username and _password:
            with mysql.connection.cursor() as cursor:
                hashed = HashPass(_password)
                query = "select * from Users where username = %s and Password_Hashed = %s;"
                params = (_username,hashed)
                cursor.execute(query,params)
                data = cursor.fetchall()
                if len(data) == 0:
                    return json.dumps({'error': "wrong credentials"})
                role = data[0][8]
                session['user']= data[0][0]
                session['role']= data[0][8]
                return json.dumps({'message': 'Credentials Correct!', 'redirect_url': Home_for_role[session['role']]})
                
                
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/Studenthome')
def StudentHome():
    if session.get('user'):
        return render_template('Studenthome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/Teacherhome')
def TeacherHome():
    if session.get('user'):
        return render_template('Teacherhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')
    
@app.route('/Operatorhome')
def OperatorHome():
    if session.get('user'):
        return render_template('Operatorhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')
    
@app.route('/Adminhome')
def AdminHome():
    if session.get('user'):
        return render_template('Adminhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/userhome')
def userHome():
    if session.get('user'):
        return render_template(Html_for_role[session['role']])
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/api/get_data')
def get_user_data():
    user_id = int(session['user'])
    try:
        with mysql.connection.cursor() as cursor:
            query = "select * from Users where user_id = "+str(user_id)+";"
            cursor.execute(query)
            data = cursor.fetchall()
            data = data[0]
            return json.dumps({'username': str(data[1]), 'first_name' : str(data[3]), 'last_name' : str(data[4]), 'birth_date' : str(data[5]), 'email' : str(data[6])}) 
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/change_password')
def password_page():
    return render_template('ChangePassword.html')

@app.route('/api/changePass', methods=['POST'])
def change_password():
    try:
        oldPassword = request.form['inputOldPassword']
        newPassword1 = request.form['inputNewPassword1']
        newPassword2 = request.form['inputNewPassword2']
        print(oldPassword, newPassword1, newPassword2)
        if oldPassword and newPassword1 and newPassword2:
            with mysql.connection.cursor() as cursor:
                oldHashed = HashPass(oldPassword)
                query = "select Password_Hashed from Users where user_id ="+str(session['user'])+";"
                cursor.execute(query);
                data = cursor.fetchall()
                if oldHashed != data[0][0]:
                    print("wrong old password:", oldPassword)
                    return json.dumps({'error': "Wrong Old Password"})
                if newPassword1 != newPassword2:
                    return json.dumps({'error': "New Passwords don't match"})
                newHashed = HashPass(newPassword1)
                query = "UPDATE Users SET Password_Hashed = %s WHERE user_id = "+str(session['user'])+';'
                params = (newHashed,)
                cursor.execute(query,params)
                mysql.connection.commit()

                return json.dumps({'message': 'Password Changed!', 'redirect_url': Home_for_role[session['role']]})

        else:
            return json.dumps({'html': '<span> Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/change_attributes')
def attributes_page():
    return render_template('change_attributes.html')

@app.route('/api/change_attributes', methods=['POST'])
def change_attr():
    try:
        firstname = request.form["inputFirstName"]
        lastname = request.form["inputLastName"]
        birthdate = request.form["inputBirthDate"]
        email = request.form["inputEmail"]
        if firstname and lastname and birthdate and email:
            with mysql.connection.cursor() as cursor:
                query = "update Users set first_name = %s,last_name = %s, birth_date = %s, email = %s where user_id = "+str(session['user'])+";"
                params = (firstname,lastname,birthdate,email,)
                cursor.execute(query,params)
                mysql.connection.commit()

                return json.dumps({'message': 'attributes updated', 'redirect_url': Home_for_role[session['role']]})
        else:
            return json.dumps({'error': 'Not all required fields were filled'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/pending_registrations')
def load_reg():
    return render_template('manageregistrations.html')

@app.route('/api/getregistrations', methods=['GET'])
def get_pending_registrations():
    try:
        with mysql.connection.cursor() as cursor:
            query = 'select users_library_id from Users where user_id='+str(session['user'])+";"
            cursor.execute(query)
            library = cursor.fetchall()
            library = int(library[0][0])
            query = 'select * from Pending_Registrations where library_id='+str(library)+" and (user_role = 'Teacher' or user_role = 'Student');"
            cursor.execute(query)
            data = cursor.fetchall()
            response = []

            

            for row in data:

                registration_dict = {
                    'username': row[0],
                    'first_name': row[2],
                    'last_name': row[3],
                    'birth_date': str(row[4]),
                    'email': row[5],
                    'role': row[6]
                }
                response.append(registration_dict)
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/api/process_registration', methods=['POST'])
def process_registration():
    try:
        data = request.get_json()
        action = data['action']
        username = data['username']
        print(username, action)
        with mysql.connection.cursor() as cursor:
            if action == "deny":
                query = "DELETE FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_registrations'})
            elif action == "accept":
                query = "SELECT * FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                data = cursor.fetchall()
                data = data[0]
                library_id = int(data[7])
                query = "DELETE FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                mysql.connection.commit()
                query = "INSERT INTO Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES (%s,%s,%s,%s,%s,%s,%s,'Active',"+str(library_id)+");"
                params = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],)
                print(query, params)
                cursor.execute(query,params)
                mysql.connection.commit()
                ''' 
                Create User's first Card
                '''
                query = "SELECT user_id from Users where username = %s;"
                params = (username,)
                cursor.execute(query,params)
                user_id = int(cursor.fetchall()[0][0])

                query = "INSERT INTO Card (user_id,card_no,status) VALUES ("+str(user_id)+",1,'Active');"
                cursor.ececute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_registrations'})
            else:
                return json.dumps({'error': 'Something has gone wrong!'})
            
    except Exception as e:
        return json.dumps({'error': str(e)})
    

@app.route('/book_search')
def showSearchbar():
    return render_template('SearchBar.html')

@app.route('/api/book_search', methods = ['POST'])
def bookSearch():
    try:
        _book = request.form['inputTitle']
        if _book:
            with mysql.connection.cursor() as cursor:
                query = "SELECT users_library_id FROM Users WHERE user_id = "+str(session['user'])+";"
                cursor.execute(query)
                library_id = int(cursor.fetchall()[0][0])

                string1 = "'%"
                string2 = "%'"
                merged_string = string1 + str(_book) + string2
                query = "SELECT b.ISBN, b.title, b.publisher, b.no_of_pages, b.summary, b.image, b.language FROM Book b INNER JOIN Lib_Owns_Book lb ON b.ISBN = lb.book_ISBN WHERE b.title LIKE {} AND lb.library_id=".format(merged_string)  +str(library_id)+";"
                # query = "select * from Book where title LIKE {}".format(merged_string)
                cursor.execute(query)
                results = cursor.fetchall()
                if (len(results) == 0):
                    return json.dumps({'message' : 'No books found relative to the searched word'})
                else:
                    books = []
                    for row in results:
                        image_data = None
                        if row[5] is not None:  # Check if photo is not NULL
                            image_bytes = base64.b64decode(row[5])
                            image_data = base64.b64encode(image_bytes).decode('utf-8')
                        book = {
                            'isbn': row[0],
                            'title': row[1],
                            'publisher': row[2],
                            'no_of_pages': row[3],
                            'language': row[6],
                            'image_data': image_data
                        }
                        books.append(book)
                    return jsonify({'results': books})
        else:
            return json.dumps({'html': '<span> Enter the required fields</span>'})

    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/api/book_search_keyword', methods = ['POST'])
def bookSearchkey():
    try:
        keyword = request.form['inputKey']
        if keyword:
            with mysql.connection.cursor() as cursor:
                query = "SELECT users_library_id FROM Users WHERE user_id = "+str(session['user'])+";"
                cursor.execute(query)
                library_id = int(cursor.fetchall()[0][0])
                query = "SELECT b.ISBN, b.title, b.publisher, b.no_of_pages, b.summary, b.image, b.language FROM Keywords k INNER JOIN Keywords_in_book kb ON k.keyword_id = kb.keyword_id INNER JOIN Book b ON kb.book_ISBN = b.ISBN INNER JOIN Lib_Owns_Book lb ON b.ISBN = lb.book_ISBN WHERE k.keyword= %s AND lb.library_id="+str(library_id)+";"
                params = (keyword,)
                cursor.execute(query,params)
                results = cursor.fetchall()
                if (len(results) == 0):
                    return json.dumps({'message' : 'No books found relative to the searched word'})
                else:
                    books = []
                    for row in results:
                        image_data = None
                        if row[5] is not None:  # Check if photo is not NULL
                            image_bytes = base64.b64decode(row[5])
                            image_data = base64.b64encode(image_bytes).decode('utf-8')
                        book = {
                            'isbn': row[0],
                            'title': row[1],
                            'publisher': row[2],
                            'no_of_pages': row[3],
                            'language': row[6],
                            'image_data': image_data
                            
                        }
                        books.append(book)

                    return jsonify({'results': books})
        else:
            return json.dumps({'html': '<span> Enter the required fields</span>'})

    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/api/requestbook', methods=['POST'])
def requestbook():
    try:
        data = request.get_json()
        print(data)
        book_isbn = int(data['book_isbn'])
        user_id = int(session['user'])
        print(book_isbn)
        with mysql.connection.cursor() as cursor:
            # getting the role of the user from the user_id provided
            query = "SELECT user_role from Users where user_id = "+str(user_id)+"; "
            cursor.execute(query)
            data = cursor.fetchall()

            # getting how many Late Returns has the user made
            query2 = "SELECT COUNT(*) from Loan where user_id = "+str(user_id)+" AND status = 'Late Returned';"
            cursor.execute(query2)
            data2 = cursor.fetchall()

            #getting how many active Loans the user has
            query3 = "SELECT COUNT(*) from Loan WHERE user_id = "+str(user_id)+" AND loan_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);"
            cursor.execute(query3)
            data3  = cursor.fetchall()

            query4 = "SELECT COUNT(*) FROM Reservation WHERE user_id = "+str(user_id)+" AND reservation_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);"
            cursor.execute(query4)
            data4  = cursor.fetchall()
            #checking every limit of the request

    
            #late returns
            if (data2[0][0] != 0) :
                return json.dumps({'message' : "Late returns" })
            
            #if teach, only 1 book per week
            if ((data[0][0] == 'Teacher') and (data3[0][0] == 1) and data4[0][0] == 1) :
                return json.dumps({'message' : "Too many books for the week"})
    
            #if student, only 2 books per week
            if ((data[0][0] == 'Student') and (data3[0][0] == 2 and data4[0][0] == 1)) :
                return json.dumps({'message' : "Too many books for the week"})

            #if operator, only 1 book per week like the teacher
            if ((data[0][0] == 'Operator') and (data3[0][0] == 1 and data4[0][0] == 1)) :
                return json.dumps({'message' : "Too many books for the week"})


            query = "INSERT INTO Request (book_ISBN,user_id) VALUES ("+str(book_isbn)+","+str(user_id)+")"
            cursor.execute(query)
            mysql.connection.commit()

            return json.dumps({'redirect_url': '/userhome'})
    except Exception as e:
        return render_template('error.html', error = str(e))
                               


@app.route('/pending_operator_registrations')
def pending_operators():
    return render_template('OperatorRegistrations.html')

@app.route('/api/get_operator_registrations', methods=['GET'])
def get_operator_registrations():
    try:
        with mysql.connection.cursor() as cursor:
            
            query = "select * from Pending_Registrations where user_role = 'Operator' or user_role = 'Admin';"
            cursor.execute(query)
            data = cursor.fetchall()
            response = []

            ''' 
            Εδώ θα κάνουμε το query για να πάρουμε τα ονόματα των βιβλιοθηκών σε σχέση με τα id
            '''

            query = "select library_id, name from School_Library;"
            cursor.execute(query)
            libraries = cursor.fetchall()
            libs = {}
            for library in libraries:
                libs[library[0]] = library[1]
            

            for row in data:

                registration_dict = {
                    'username': row[0],
                    'first_name': row[2],
                    'last_name': row[3],
                    'birth_date': str(row[4]),
                    'email': row[5],
                    'role': row[6],
                    'school': libs[row[7]]
                }
                response.append(registration_dict)
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/api/process_operator', methods=['POST'])
def process_operator():
    try:
        data = request.get_json()
        action = data['action']
        username = data['username']
        print(username, action)
        with mysql.connection.cursor() as cursor:
            if action == "deny":
                query = "DELETE FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_registrations'})
            elif action == "accept":
                query = "SELECT * FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                data = cursor.fetchall()
                data = data[0]
                library_id = int(data[7])
                query = "DELETE FROM Pending_Registrations WHERE username = '"+username+"';"
                cursor.execute(query)
                mysql.connection.commit()
                query = "INSERT INTO Users (username,Password_Hashed,first_name,last_name,birth_date,email,user_role,user_status,users_library_id) VALUES (%s,%s,%s,%s,%s,%s,%s,'Active',"+str(library_id)+");"
                params = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],)
                print(query, params)
                cursor.execute(query,params)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_operator_registrations'})
            else:
                return json.dumps({'error': 'Something has gone wrong!'})
            
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/manip_lib')
def manip_lib():
    return render_template('Library_hub.html')

@app.route('/create_lib')
def create_lib():
    return render_template('Create_Library.html')

@app.route('/api/createlib', methods=['POST'])
def library_creation_form_process():
    try:
        name = request.form["inputName"]
        address = request.form["inputAddress"]
        city = request.form["inputCity"]
        email = request.form["inputEmail"]
        if name and address and city and email:
            with mysql.connection.cursor() as cursor:
                query = "select name from School_Library where name = %s;"
                params = (name,)
                cursor.execute(query,params)
                data = cursor.fetchall()
                if len(data) !=0:
                    return json.dumps({'error': "School of this name already exists"})
                print(name,address,city,email);
                query = "INSERT INTO School_Library (name, address, town, email) VALUES (%s,%s,%s,%s);"
                params = (name,address,city,email,)
                cursor.execute(query,params)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/manip_lib'})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/change_lib')
def change_lib():
    return render_template('Change_Lib.html')

@app.route('/api/changelib', methods=['POST'])
def change_library():
    try:
        old_name = request.form.get("dropdown")
        new_name = request.form["inputNewName"]
        new_address = request.form["inputNewAddress"]
        new_city = request.form["inputNewCity"]
        new_email = request.form["inputNewEmail"]
        if old_name and new_address and new_city and new_email and new_name:
            with mysql.connection.cursor() as cursor:
                query = "update School_Library set name = %s, address = %s, town = %s, email = %s where name = %s;"
                params = (new_name,new_address,new_city,new_email,old_name,)
                cursor.execute(query,params)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/manip_lib'})
        else:
            return json.dumps({'error': 'Not all required fields were filled'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    

@app.route('/api/getschools', methods=['GET'])
def return_lib_names():
    try:
        with mysql.connection.cursor() as cursor:
            query = 'select name from School_Library;'
            cursor.execute(query)
            data = cursor.fetchall()
            response = []
            for row in data:
                lib = {'name': row}
                response.append(lib)
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/newbook')
def newbookpage():
    return render_template('NewBook.html')

@app.route('/api/newbook', methods=['POST'])
def newbookinsert():
    try:
        ISBN = int(request.form['inputISBN'])
        title = request.form['inputTitle']
        publisher = request.form['inputPublisher']
        pages = int(request.form['inputPages'])
        summary = request.form['inputSummary']
        image = request.files['inputImage']
        language = request.form['inputLanguage']
        keywords = request.form['inputKeywords']
        authors = request.form['inputAuthors']
        categories = request.form['inputThematic']
    
        if ISBN and title and publisher and pages and summary and image and language and keywords and authors and categories:

            file_type, _ = mimetypes.guess_type(image.filename)
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if file_type not in allowed_types:
                return json.dumps({'errorshow': 'Invalid file type. Only JPEG, JPG, and PNG files are allowed'})

            max_size = 250 * 1024 
            if len(image.read()) > max_size:
                return json.dumps({'errorshow': 'File too large'})

            image.seek(0)

            file_bytes = image.read()

            keywords = keywords.split(",")
            authors = authors.split(",")
            categories = categories.split(",")
            with mysql.connection.cursor() as cursor:
                query = "INSERT INTO Book (ISBN,title,publisher,no_of_pages,summary,image,language) VALUES ("+str(ISBN)+",%s,%s,"+str(pages)+",%s,%s,%s);"
                params = (title,publisher,summary,base64.b64encode(file_bytes),language)
                cursor.execute(query, params)
                mysql.connection.commit()
                for keyword in keywords:
                    query = "select keyword_id from Keywords where keyword = %s;"
                    params = (keyword,)
                    cursor.execute(query,params)
                    data = cursor.fetchall()
                    if len(data) == 0:
                        query = "INSERT INTO Keywords (keyword) VALUES (%s);"
                        params = (keyword,)
                        cursor.execute(query,params)
                        mysql.connection.commit()
                        query = "select keyword_id from Keywords where keyword = %s;"
                        cursor.execute(query,params)
                        data = cursor.fetchall()
                        keyword_id = int(data[0][0])
                        query = "INSERT INTO Keywords_in_book (keyword_id,book_ISBN) VALUES ("+str(keyword_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                    else:
                        keyword_id = int(data[0][0])
                        query = "INSERT INTO Keywords_in_book (keyword_id,book_ISBN) VALUES ("+str(keyword_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                for author in authors:
                    first_name = author.split(" ")[0]
                    last_name = author.split(" ")[1]
                    query = "select author_id from Authors where first_name = %s and last_name = %s;"
                    params = (first_name,last_name,)
                    cursor.execute(query,params)
                    data = cursor.fetchall()
                    if len(data) == 0:
                        query = "INSERT INTO Authors (first_name,last_name) VALUES (%s,%s);"
                        params = (first_name,last_name,)
                        cursor.execute(query,params)
                        mysql.connection.commit()
                        query = "select author_id from Authors where first_name = %s and last_name = %s;"
                        cursor.execute(query,params)
                        data = cursor.fetchall()
                        author_id = int(data[0][0])
                        query = "INSERT INTO Wrote (author_id,book_ISBN) VALUES ("+str(author_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                    else:
                        author_id = int(data[0][0])
                        query = "INSERT INTO Wrote (author_id,book_ISBN) VALUES ("+str(author_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                for category in categories:
                    query = "select category_id from Thematic_Category where category = %s;"
                    params = (category,)
                    cursor.execute(query,params)
                    data = cursor.fetchall()
                    if len(data) == 0:
                        query = "INSERT INTO Thematic_Category (category) VALUES (%s);"
                        params = (category,)
                        cursor.execute(query,params)
                        mysql.connection.commit()
                        query = "select category_id from Thematic_Category where category = %s;"
                        cursor.execute(query,params)
                        data = cursor.fetchall()
                        category_id = int(data[0][0])
                        query = "INSERT INTO Belongs_in (category_id,book_ISBN) VALUES ("+str(category_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                    else:
                        category_id = int(data[0][0])
                        query = "INSERT INTO Belongs_in (category_id,book_ISBN) VALUES ("+str(category_id)+","+str(ISBN)+");"
                        cursor.execute(query)
                        mysql.connection.commit()
                return json.dumps({'redirect_url': '/userhome'})


        else:
            return json.dumps({'errorshow': 'Not all required fields were filled'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/get_phones')
def getphones():
    return render_template('get_phones.html')

@app.route('/api/get_phones', methods=['GET'])
def get_phones():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT number from User_Phone_No where user_id = " + str(session['user'])
            cursor.execute(query)
            data = cursor.fetchall() 
            counter = 0
            response = []

            for phones in data:
                counter += 1
                response.append({
                    "id": counter,
                    "number": phones[0]
                })
            return jsonify(response)
            
    except Exception as e:
        return json.dumps({'error': str(e)})
    
@app.route('/change_phones')
def change_phones():
    return render_template('ChangePhone.html')

@app.route('/api/add_phone', methods = ['POST'])
def add_phone():
    data = request.get_json()
    username = str(session['user'])
    number = data['number']

    #test
    if not isinstance(number,str) or len(number) == 0:
        return jsonify({'message' : 'Error', 'error': 'Invalid number'})
    try:
        with mysql.connection.cursor() as cursor:
            query = "INSERT INTO User_Phone_No (number, user_id) VALUES (%s, %s);"
            params = (number, username)
            cursor.execute(query,params)
            mysql.connection.commit()
            return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})
    
@app.route('/api/delete_phone', methods = ['POST'])
def delete_phone():
    data = request.get_json()
    number = data['number']

    #test
    if not isinstance(number,str) or len(number) == 0:
        return jsonify({'message' : 'Error', 'error': 'Invalid number'})
    try:
        with mysql.connection.cursor() as cursor:
            query = "DELETE FROM User_Phone_No WHERE number = %s;"
            params =(number,)
            cursor.execute(query, params)
            mysql.connection.commit()
            response_data = {'message': 'Success'}
            return json.dumps(response_data)
    except Exception as e:
        response_data = {'message': 'Error'}
        return json.dumps(response_data)
    
@app.route('/card_condition')
def show_card_status():
    try:
        card_no = 0
        card_status = 'Inactive'
        user_id = int(session['user'])
        with mysql.connection.cursor() as cursor:
            query = "SELECT max(card_no) from Card where user_id = "+str(user_id)+";"
            cursor.execute(query)
            card_no = int(cursor.fetchall()[0][0])
            query = "SELECT status from Card where user_id = "+str(user_id)+" and card_no="+str(card_no)+";"
            cursor.execute(query)
            card_status = cursor.fetchall()[0][0]
        return render_template("CardStatus.html", card_no = card_no, status = card_status)
    except Exception as e:
        return redirect('/logout')
    

@app.route('/api/lostcard', methods=['POST'])
def lost_card():
    try:
        user_id = int(session['user'])
        password = request.form['inputPassword']
        if password:
            with mysql.connection.cursor() as cursor:

                query = "SELECT Password_Hashed FROM Users where user_id = "+ str(user_id)+";"
                cursor.execute(query)
                if HashPass(password) != cursor.fetchall()[0][0]:
                    json.dumps({'errorshow': 'Wrong Password'})
                
                query = "SELECT card_no FROM Card where user_id ="+str(user_id)+" and status = 'Active';"
                cursor.execute(query)
                cardno = int(cursor.fetchall()[0][0])
                query = "UPDATE Card SET status = 'Missing' WHERE user_id="+str(user_id)+" and card_no="+str(cardno)+";"
                cursor.execute(query)
                mysql.connection.commit()
                query = "INSERT INTO Card (user_id,card_no,status) VALUES ("+str(user_id)+","+str(cardno + 1)+",'Pending');"
                cursor.execute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/userhome'})
        else:
            return json.dumps({'errorshow': 'Not all required fields were filled'})

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/pending_cards')
def show_pending_card_page():
    return render_template('pendingcards.html')



@app.route('/api/getcards', methods=['GET'])
def get_pending_cards():
    try:
        with mysql.connection.cursor() as cursor:
            query = 'select users_library_id from Users where user_id='+str(session['user'])+";"
            cursor.execute(query)
            library = cursor.fetchall()
            library = int(library[0][0])
            query = "SELECT u.username, u.first_name, u.last_name, u.email, u.user_role, c.card_no FROM Card c JOIN Users u ON c.user_id = u.user_id WHERE c.status = 'Pending' AND u.users_library_id = "+str(library)+";"
            cursor.execute(query)
            data = cursor.fetchall()
            response = []

            

            for row in data:

                registration_dict = {
                    'username': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'role': row[4],
                    'card_no': row[5]
                }
                response.append(registration_dict)
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/api/process_card', methods=['POST'])
def process_card():
    try:
        data = request.get_json()
        action = data['action']
        username = data['username']
        card_no = int(data['card_no'])
        print(username, action)
        with mysql.connection.cursor() as cursor:
            query = "SELECT user_id FROM Users WHERE username = %s;"
            params = (username,)
            cursor.execute(query,params)
            user_id = int(cursor.fetchall()[0][0])
            if action == "deny":
                query = "UPDATE Card SET status = 'Inactive' where user_id = "+str(user_id)+" AND card_no = "+str(card_no)+";"
                cursor.execute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_cards'})
            elif action == "accept":
                query = "UPDATE Card SET status = 'Active' where user_id = "+str(user_id)+" AND card_no = "+str(card_no)+";"
                cursor.execute(query)
                mysql.connection.commit()
                return json.dumps({'redirect_url': '/pending_cards'})
            else:
                return json.dumps({'error': 'Something has gone wrong!'})
            
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/manage_users')
def manage_users():
    return render_template('/manageusers.html')

@app.route('/api/search_user', methods=['POST'])
def return_users():
    try:
        last_name = request.form['inputLastName']
        print(last_name)
        if last_name:
            with mysql.connection.cursor() as cursor:
                query = "SELECT * FROM Users WHERE last_name = %s;"
                params = (last_name,)
                cursor.execute(query,params)
                results = cursor.fetchall()
                if (len(results) == 0):
                    return json.dumps({'message' : 'No users with this last name'})
                else:
                    users = []
                    for row in results:
                        user = {
                            'id': row[0],
                            'username': row[1],
                            'first_name': row[3],
                            'last_name': row[4],
                            'birth_date': str(row[5]),
                            'email': row[6],
                            'user_role': row[8],
                            'user_status': row[9]
                        }
                        users.append(user)
                    return jsonify({'results': users})
        else:
            return json.dumps({'errorshow': 'Not all required fields were filled'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/api/process_(de)activation', methods=['POST'])
def process_act():
    try:
        data = request.json
        action = data['action']
        username = data['username']
        with mysql.connection.cursor() as cursor:
            if (action == 'activate') :
                query = "UPDATE Users SET user_status = 'Active' where username = %s;"
                params = (username,)
                cursor.execute(query, params)
                mysql.connection.commit()
                return jsonify({'message': 'Success'})
            elif (action == 'deactivate') :
                query = "UPDATE Users SET user_status = 'Inactive' where username =%s;"
                params = (username,)
                cursor.execute(query, params)
                mysql.connection.commit()
                return jsonify({'message': 'Success2'})
            else :
                return jsonify({'message': 'Wrong action passed'})
    except Exception as e:
        return jsonify({'message': str(e)})

@app.route('/api/process_deletion_of_user', methods=['POST'])
def delete_user():
    try:
        data = request.json
        username = data['username']
        with mysql.connection.cursor() as cursor:
            query = "SELECT user_id FROM Users where username = %s;"
            params = (username,)
            cursor.execute(query,params)
            user_id = int(cursor.fetchall()[0][0])

            query = "DELETE FROM Loan WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Card WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Request WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Reservation WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Reviews WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM User_Phone_No WHERE user_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Operator_Appointment WHERE operator_id ="+str(user_id)+" OR administrator_id ="+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "UPDATE School_Library SET principals_id = NULL WHERE principals_id = "+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            query = "DELETE FROM Users Where user_id = "+str(user_id)+";"
            cursor.execute(query)
            mysql.connection.commit()

            return jsonify({'message': 'Success'})



    except Exception as e:
        return jsonify({'message': str(e)})

@app.route('/show_myloans_reg')
def show_myloans():
    return render_template('/show_myloans_reg.html')

@app.route('/api/get_loans_reg')
def get_loans():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT book_ISBN, return_date, status from Loan where user_id = %s and (status = 'Active' or status = 'Late Active');"
            user_id = str(session['user'])
            params = (user_id,)
            cursor.execute(query, params)
            mysql.connection.commit()
            data = cursor.fetchall()

            query2 = "SELECT book_ISBN, expiration_date, status from Reservation where user_id = %s and status = 'Active';"
            cursor.execute(query2, params)
            mysql.connection.commit()
            data2 = cursor.fetchall()
            response1 = []
            response2 = []

            for loans in data:
                response1.append({
                    "isbn" : loans[0],
                    "return_date" : loans[1],
                    "status" : loans[2]
                })

            for regestrations in data2:
                response2.append({
                    "isbn2" : regestrations[0],
                    "expiration_date" : regestrations[1],
                    "status2" : regestrations[2]
                })

            return jsonify({
                "loans" : response1,
                "registrations" : response2
            })
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
@app.route('/late_returns')
def late_returns():
    return render_template('late_loans.html')

@app.route('/api/get_lateloans')
def get_lateloans():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT l.book_ISBN, l.user_id, u.username FROM Loan l JOIN Users u ON  l.user_id = u.user_id WHERE l.status = 'Late Returned';"
            cursor.execute(query)
            mysql.connection.commit()
            data = cursor.fetchall()
            response = []

            for loans in data:
                response.append({
                    "isbn" : loans[0],
                    "userid" : loans[1],
                    "username" : loans[2]
                })
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
@app.route('/past_loans')
def past_loans_reg():
    return render_template('past_loans_reg.html')

@app.route('/api/past_loans_reg')
def get_loans_reg():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT book_ISBN, return_date, status from Loan where user_id = %s and (status = 'Returned' or status = 'Late Returned');"
            user_id = str(session['user'])
            params = (user_id,)
            cursor.execute(query, params)
            mysql.connection.commit()
            data = cursor.fetchall()

            second_query = "SELECT book_ISBN, expiration_date, status from Reservation where user_id = %s and (status = 'Expired' or status = 'Honoured');"
            cursor.execute(second_query, params)
            mysql.connection.commit()
            second_data = cursor.fetchall()

            response = []

            for loans in data:
                response.append({
                    "isbn" : loans[0],
                    "return_date" : loans[1],
                    "status" : loans[2]
                })
            
            for reg in second_data:
                response.append({
                    "isbn2" : reg[0],
                    "expiration_date" : reg[1],
                    "status2" : reg[2]
                })
            
            return jsonify(response)
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
@app.route('/forced_loans')
def force_reg():
    return render_template('force_loans.html')

@app.route('/api/instant_loans', methods =['POST'])
def instant_loans():
    try:
        bookISBN = request.form.get('inputISBN')
        user_id = request.form.get('inputUserId')

        if bookISBN and user_id:
            with mysql.connection.cursor() as cursor:
                #getting the role of the user from the user_id provided
                query = "SELECT user_role from Users where user_id = %s; "
                params = (user_id,)
                cursor.execute(query, params)
                mysql.connection.commit()
                data = cursor.fetchall()


                #getting how many Late Returns has the user made
                query2 = "SELECT COUNT(*) from Loan where user_id = %s AND status = 'Late Returned';"
                cursor.execute(query2, params)
                mysql.connection.commit()
                data2 = cursor.fetchall()

                #getting how many active Loans the user has
                query3 = "SELECT COUNT(*) from Loan WHERE user_id = %s AND (status = 'Active' OR status = 'Late Active');"
                cursor.execute(query3, params)
                mysql.connection.commit()
                data3  = cursor.fetchall()

                #checking every limit of the instant loan

                #late returns
                if (data2[0][0] != 0) :
                    return json.dumps({'message' : "Late returns" })
                
                #if teach, only 1 book per week
                if ((data[0][0] == 'Teacher') and (data3[0][0] == 1)) :
                    return json.dumps({'message' : "Too many books for the week"})
        
                #if student, only 2 books per week
                if ((data[0][0] == 'Student') and (data3[0][0] == 2)) :
                    return json.dumps({'message' : "Too many books for the week"})

                #if operator, only 1 book per week like the teacher
                if ((data[0][0] == 'Operator') and (data3[0][0] == 1)) :
                    return json.dumps({'message' : "Too many books for the week"})        

                #if admin, we don't have to check anything
                #he can get as many books as he wants

                #if we reach this point, the user satisfies all the limits
                #so we can perform the query for the loan if there are available copies

                #first we get the library id that user belongs to 
                query4 = "SELECT users_library_id from Users where user_id = %s;"
                cursor.execute(query4, params)
                mysql.connection.commit()
                data4 = cursor.fetchall()

                #then we find the available copies
                #if the returned object has length 0 it means book is not in the library
                query5 = "SELECT available_copies FROM Lib_Owns_Book WHERE book_ISBN = %s AND library_id = %s;"
                params2 = (bookISBN, data4[0][0],)
                cursor.execute(query5, params2)
                mysql.connection.commit()
                data5 = cursor.fetchall()

                if (len(data5) == 0) :
                    return json.dumps({'message' : "Book not in library"})
                
                if (data5[0][0] == 0) :
                    return json.dumps({'message' : "Not enough copies"})
                
                #we have to get the current date and add 1 week to set the return date
                current_date = datetime.now().date()
                new_date = current_date + timedelta(weeks=1)
                formatted_date = new_date.strftime('%Y-%m-%d')

                #if we reach, all set and we can finally input the loan to the database
                query6 = "INSERT INTO Loan (book_ISBN, user_id, return_date, status) VALUES (%s, %s, %s, 'Active');"
                params3 = (bookISBN, user_id, formatted_date,)
                cursor.execute(query6, params3)
                mysql.connection.commit()

                #we reduce the available copies of the books by 1
                new_available_copies = data5[0][0] - 1
                query7 = "UPDATE Lib_Owns_Book SET available_copies = %s WHERE book_ISBN = %s AND library_id = %s;"
                params4 = (new_available_copies, bookISBN, data4[0][0])
                cursor.execute(query7, params4)
                mysql.connection.commit()

                return json.dumps({'message' : "Loan was registered successfully"})
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
@app.route('/get_myrequests')
def get_myrequests():
    return render_template('get_requests.html')

@app.route('/api/get_requests', methods = ['GET'])
def get_requests():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT book_ISBN from Request where user_id = %s;"
            params = (str(session['user']),)
            cursor.execute(query, params)
            data = cursor.fetchall()
            counter = 0
            response = []

            for requests in data:
                counter += 1
                response.append({
                    "id" : counter,
                    "isbn" : requests[0]
                })
            return jsonify(response)
        
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
 @app.route('/satisfy_reservations')
def satisfy_res():
    return render_template('satisfy_reservations.html')

@app.route('/api/get_available_reservations')
def get_reserv():
    try:
        with mysql.connection.cursor() as cursor:
            #first we need to know at which library the operator works
            query = "SELECT users_library_id FROM Users WHERE user_id = %s;"
            params = (str(session['user']),)
            cursor.execute(query, params)
            data = cursor.fetchall()

            query2 = "SELECT r.book_ISBN, u.username, u.first_name, u.last_name, r.expiration_date FROM Reservation r INNER JOIN Users u ON r.user_id = u.user_id INNER JOIN Lib_Owns_Book l ON l.book_ISBN = r.book_ISBN WHERE u.users_library_id = %s AND r.status = 'Active' AND l.available_copies >= 1;"
            params2 = (data[0][0],)
            cursor.execute(query2, params2)
            data2 = cursor.fetchall()

            response = []

            for results in data2:
                response.append({
                    "isbn" : results[0],
                    "username" : results[1],
                    "first_name" : results[2],
                    "last_name" : results[3],
                    "expiration_date" : results[4],
                })

            return jsonify(response)

    except Exception as e:
        return json.dumps({'error' : str(e)})
    
@app.route('/api/proccess_reservations', methods = ['POST'])
def satisfy_reservations():
    try:
        result = request.get_json()
        action = result['action']
        username = result['username']
        book_ISBN = result['book_ISBN']
        with mysql.connection.cursor() as cursor:
            if action == "honour":
                #make the status honoured for the reservation
                query = "UPDATE Reservation SET status = 'Honoured' WHERE book_ISBN = %s AND user_id = (SELECT user_id FROM Users WHERE username = %s);"
                params = (book_ISBN, username,)
                cursor.execute(query, params)
                mysql.connection.commit()

                #make a loan for the user
                query2 = "SELECT user_id from Users WHERE username = %s;"
                params2 = (username,)
                cursor.execute(query2, params2)
                data = cursor.fetchall()
                user_id = data[0][0]

                current_date = datetime.now().date()
                new_date = current_date + timedelta(weeks=1)
                formatted_date = new_date.strftime('%Y-%m-%d')

                query3 = "INSERT INTO Loan (book_ISBN, user_id, return_date, status) VALUES (%s, %s, %s, 'Active');"
                params3 = (book_ISBN, user_id, formatted_date,)
                cursor.execute(query3, params3)
                mysql.connection.commit()

                #reduce the available copies of the book by 1
                query4 = "SELECT users_library_id from Users WHERE username = %s;"
                cursor.execute(query4, params2)
                data2 = cursor.fetchall()
                library_id = data2[0][0]

                query5 = "SELECT available_copies FROM Lib_Owns_Book WHERE book_ISBN = %s AND library_id = %s;"
                params4 = (book_ISBN, library_id)
                cursor.execute(query5, params4)
                data3 = cursor.fetchall()
                available_copies = data3[0][0]

                query6 = "UPDATE Lib_Owns_Book SET available_copies = %s WHERE book_ISBN = %s AND library_id = %s;"
                params5 = (available_copies, book_ISBN, library_id,)
                cursor.execute(query6, params5)
                mysql.connection.commit()

                return json.dumps({'redirect_url': '/satisfy_reservations'})
            
            elif action == 'move_to_expired' :
                #we just need to update this thing only
                query7 = "SELECT user_id from Users WHERE username = %s;"
                params6 = (username,)
                cursor.execute(query7, params6)
                data4 = cursor.fetchall()
                user_id = data4[0][0]
                
                query8 = "UPDATE Reservation SET status = 'Expired' WHERE book_ISBN = %s AND user_id = %s;"
                params7 = (book_ISBN, user_id,)
                cursor.execute(query8, params7)
                mysql.connection.commit()

                return json.dumps({'redirect_url': '/satisfy_reservations'})
            
            else :
                return json.dumps({'error' : 'Something went wrong'})


    
    except Exception as e:
        return json.dumps({'error' : str(e)})

# implementing specified queries for each role (12 in total). Each role's homepage redirects to own queries.

# query1
@app.route('/library_stats', methods=['GET'])
def library_stats():
    if session.get('role') == 'Admin':
        return render_template('library_stats.html')
    else:
        return "Unauthorized", 401


@app.route('/api/library_stats', methods=['GET'])
def get_library_stats():
    if session.get('role') == 'Admin':
        year = request.args.get('year')
        month = request.args.get('month')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT School_Library.name, library_id, COUNT(*) AS TotalLoans
                FROM Loan
                INNER JOIN Users ON Loan.user_id = Users.user_id
                INNER JOIN School_Library ON Users.users_library_id = School_Library.library_id
                WHERE YEAR(Loan.loan_date) = %s
                    AND MONTHNAME(Loan.loan_date) = %s
                GROUP BY library_id;
            """
            params = (year, month)
            cursor.execute(query, params)
            result = cursor.fetchall()

        # Process the query result and return as JSON
        stats = []
        for row in result:
            stats.append({
                'name': row[0],
                'library_id': row[1],
                'TotalLoans': row[2]
            })

        return jsonify(stats)
    else:
        return "Unauthorized", 401

# query2
# fix this


@app.route('/authors_stats', methods=['GET'])
def authors_stats():
    if session.get('role') == 'Admin':
        return render_template('authors_stats.html')
    else:
        return "Unauthorized", 401


@app.route('/api/authors_stats', methods=['GET'])
def get_authors_stats():
    if session.get('role') == 'Admin':
        category = request.args.get('category')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT DISTINCT CONCAT(Authors.first_name, ' ', Authors.last_name) AS author_name
                FROM Authors
                INNER JOIN Wrote ON Authors.author_id = Wrote.author_id
                INNER JOIN Book ON Wrote.Book_ISBN = Book.ISBN
                INNER JOIN Belongs_in ON Book.ISBN = Belongs_in.Book_ISBN
                INNER JOIN Thematic_Category ON Belongs_in.category_id = Thematic_Category.category_id
                WHERE Thematic_Category.category = %s;
            """
            cursor.execute(query, (category,))
            result = cursor.fetchall()

        # Process the query result and return as JSON
        authors = []
        for row in result:
            authors.append({
                'author_name': row[0]
            })

        return jsonify(authors)
    else:
        return "Unauthorized", 401

# query3
#find young teachers who have borrowed the most books and the number of books
@app.route('/teachers_stats', methods=['GET'])
def teachers_stats():
    if session.get('role') == 'Admin':
        return render_template('teachers_stats.html')
    else:
        return "Unauthorized", 401


@app.route('/api/teachers_stats', methods=['GET'])
def get_teachers_stats():
    if session.get('role') == 'Admin':
        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Users.user_id, Users.first_name, Users.last_name, COUNT(*) AS num_books_borrowed
                FROM Users
                INNER JOIN Loan ON Users.user_id = Loan.user_id
                WHERE Users.user_role = 'Teacher'
                  AND TIMESTAMPDIFF(YEAR, Users.birth_date, CURDATE()) < 40
                GROUP BY Users.user_id, Users.first_name, Users.last_name
                ORDER BY num_books_borrowed DESC
                LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()

        # Process the query result and return as JSON
        if result:
            user_id, first_name, last_name, num_books_borrowed = result
            teacher_stats = {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'num_books_borrowed': num_books_borrowed
            }
            return jsonify(teacher_stats)
        else:
            return jsonify({}), 404  # No results found
    else:
        return "Unauthorized", 401

#query4
#Find authors whose books have not been borrowed
@app.route('/authors_not_borrowed', methods=['GET'])
def authors_not_borrowed():
    if session.get('role') == 'Admin':
        return render_template('authors_not_borrowed.html')
    else:
        return "Unauthorized", 401


@app.route('/api/authors_not_borrowed', methods=['GET'])
def get_authors_not_borrowed():
    if session.get('role') == 'Admin':
        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Authors.author_id, Authors.first_name, Authors.last_name
                FROM Authors
                WHERE Authors.author_id NOT IN (
                    SELECT Wrote.author_id
                    FROM Wrote
                    INNER JOIN Loan ON Loan.book_ISBN = Wrote.book_ISBN
                );
            """
            cursor.execute(query)
            result = cursor.fetchall()

        # Process the query result and return as JSON
        authors = []
        for row in result:
            author_id, first_name, last_name = row
            authors.append({
                'author_id': author_id,
                'first_name': first_name,
                'last_name': last_name
            })

        return jsonify(authors)
    else:
        return "Unauthorized", 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

#query5
@app.route('/operators_loan_count', methods=['GET'])
def operators_loan_count():
    if session.get('role') == 'Admin':
        return render_template('operators_loan_count.html')
    else:
        return "Unauthorized", 401


@app.route('/api/operators_loan_count', methods=['GET'])
def get_operators_loan_count():
    if session.get('role') == 'Admin':
        year = request.args.get('year')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Users.user_id, Users.first_name, Users.last_name
                FROM Loan
                INNER JOIN Users ON Loan.user_id = Users.user_id
                WHERE Users.user_role = 'operator' AND YEAR(Loan.loan_date) = %s
                GROUP BY Users.user_id
                HAVING COUNT(*) > 20;
            """
            cursor.execute(query, (year,))
            result = cursor.fetchall()

        # Process the query result and return as JSON
        operators = []
        for row in result:
            user_id, first_name, last_name = row
            operators.append({
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name
            })

        return jsonify(operators)
    else:
        return "Unauthorized", 401

#query6


#query7
#select all the authors which have written more than 5 books less tan the first author 
@app.route('/authors_less_books', methods=['GET'])
def authors_less_books():
    if session.get('role') == 'Admin':
        return render_template('authors_less_books.html')
    else:
        return "Unauthorized", 401


@app.route('/api/authors_less_books', methods=['GET'])
def get_authors_less_books():
    if session.get('role') == 'Admin':
        with mysql.connection.cursor() as cursor:
            query = """
                SELECT A.author_id, A.first_name, A.last_name
                FROM Authors A
                WHERE (SELECT COUNT(*) FROM Wrote W WHERE W.author_id = A.author_id) <
                      (SELECT COUNT(*) - 5 FROM Wrote GROUP BY author_id ORDER BY COUNT(*) DESC LIMIT 1);
            """
            cursor.execute(query)
            result = cursor.fetchall()

        # Process the query result and return as JSON
        authors = []
        for row in result:
            authors.append({
                'author_id': row[0],
                'first_name': row[1],
                'last_name': row[2]
            })

        return jsonify(authors)
    else:
        return "Unauthorized", 401
###Implementing all the user_role = 'Operator' queries.

#query8
#this is a parametric query and appends lines to the query with 'AND' based on how many fields the search is based on

@app.route('/book_search_operator', methods=['GET'])
def book_search_operator():
    if session.get('role') == 'Operator':
        return render_template('book_search_operator.html')
    else:
        return "Unauthorized", 401


@app.route('/api/book_search_operator', methods=['GET'])
def get_book_search_operator():
    if session.get('role') == 'Operator':
        title = request.args.get('title')
        category = request.args.get('category')
        name = request.args.get('name')
        copies = request.args.get('copies')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Book.title, Authors.first_name, Authors.last_name, Thematic_Category.category, LOB.total_copies
                FROM Book 
                INNER JOIN Wrote ON Book.ISBN = Wrote.book_ISBN
                INNER JOIN Authors ON Wrote.author_id = Authors.author_id
                INNER JOIN Belongs_in ON Book.ISBN = Belongs_in.book_ISBN
                INNER JOIN Thematic_Category ON Belongs_in.category_id = Thematic_Category.category_id
                INNER JOIN Lib_Owns_Book LOB ON Book.ISBN = LOB.book_ISBN
                WHERE 1=1
            """
            params = []

            if title:
                query += "AND Book.title LIKE %s "
                params.append(f"%{title}%")

            if category:
                query += "AND Thematic_Category.category LIKE %s "
                params.append(f"%{category}%")

            if name:
                query += "AND CONCAT(Authors.first_name, ' ', Authors.last_name) LIKE %s "
                params.append(f"%{name}%")

            if copies:
                query += "AND LOB.total_copies >= %s "
                params.append(copies)

            cursor.execute(query, params)
            result = cursor.fetchall()

        # Process the query result and return as JSON
        books = []
        for row in result:
            books.append({
                'title': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'category': row[3],
                'total_copies': row[4]
            })

        return jsonify(books)
    else:
        return "Unauthorized", 401

#query9
@app.route('/delayed_loan_search', methods=['GET'])
def delayed_loan_search():
    if session.get('role') == 'Operator':
        return render_template('delayed_loan_search.html')
    else:
        return "Unauthorized", 401

@app.route('/api/delayed_loan_search', methods=['GET'])
def get_dealayed_loan_search():
    if session.get('role') == 'Operator':
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        delay_days = request.args.get('delay_days')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Users.first_name, Users.last_name, DATEDIFF(CURDATE(), Loan.return_date) AS delay_days
                FROM Users
                INNER JOIN Loan ON Users.user_id = Loan.user_id
                WHERE Loan.return_date IS NOT NULL
                AND Loan.status = 'Active' OR 'Late ACTIVE'
                AND DATEDIFF(CURDATE(), Loan.return_date) > 0
                AND (Users.first_name LIKE %s OR %s = '')
                AND (Users.last_name LIKE %s OR %s = '')
            """
            params = (f"%{first_name}%", first_name, f"%{last_name}%", last_name)

            if delay_days:
                query += " AND (DATEDIFF(CURDATE(), Loan.return_date) > %s OR %s = '')"
                params += (delay_days, delay_days)

            cursor.execute(query, params)
            result = cursor.fetchall()

        # Process the query result and return as JSON
        loans = []
        for row in result:
            loans.append({
                'first_name': row[0],
                'last_name': row[1],
                'delay_days': row[2]
            })

        return jsonify(loans)

    else :
            return "Unauhtorized", 401
    
#query10
@app.route('/loan_rating_search', methods=['GET'])
def loan_rating_search():
    if session.get('role') == 'Operator':
        return render_template('loan_rating_search.html')
    else:
        return "Unauthorized", 401


@app.route('/api/loan_rating_search', methods=['GET'])
def get_loan_rating_search():
    if session.get('role') == 'Operator':
        user_id = request.args.get('user_id')
        category = request.args.get('category')

        with mysql.connection.cursor() as cursor:
            query = """
                SELECT Users.user_id, Thematic_Category.category, AVG(Reviews.likert_rating) AS average_rating
                FROM Users
                INNER JOIN Loan ON Users.user_id = Loan.user_id
                INNER JOIN Belongs_in ON Loan.book_ISBN = Belongs_in.book_ISBN
                INNER JOIN Thematic_Category ON Belongs_in.category_id = Thematic_Category.category_id
                INNER JOIN Reviews ON Reviews.book_ISBN = Loan.book_ISBN
                WHERE(Users.user_id = %s OR %s = '')
                AND (Thematic_Category.category = %s OR %s = ' ')
                GROUP BY Users.user_id, Thematic_Category.category;
            """
            cursor.execute(query, (user_id, user_id, category, category))
            result = cursor.fetchall()

        # Process the query result and return as JSON
        ratings = []
        for row in result:
            ratings.append({
                'user_id': row[0],
                'category': row[1],
                'average_rating': float(row[2])
            })

        return jsonify(ratings)
    else :
        return "Unauthorized", 401    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run()
