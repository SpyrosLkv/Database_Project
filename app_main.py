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
    return render_template('searchbar.html')
@app.route('/api/book_search', methods = ['POST'])
def bookSearch():
    try:
        _book = request.form['inputBook']
        if _book:
            with mysql.connection.cursor() as cursor:
                string1 = "'%"
                string2 = "%';"
                merged_string = string1 + str(_book) + string2
                query = "select title,publisher from Book where title LIKE %s"
                cursor.execute(query, merged_string)
                results = cursor.fetchall()
                if (len(results) == 0):
                    return json.dumps({'message' : 'No books found relative to the searched word'})
                else:
                    books = []
                    for row in results:
                        book = {
                            'title': row['title'],
                            'publisher': row['publisher']
                        }
                        books.append(book)
                    return jsonify({'results': books})
        else:
            return json.dumps({'html': '<span> Enter the required fields</span>'})

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

@app.route('/api/process_(de)activation')
def process_act():
    try:
        data = request.json()
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
                query = "UPDATE Users SET user_status = 'Inactive' where usernmae =%s;"
                params = (username,)
                cursor.execute(query, params)
                mysql.connection.commit()
                return jsonify({'message': 'Success2'})
            else :
                return jsonify({'message': 'Wrong action passed'})
    except Exception as e:
        return jsonify({'message': 'Error'})

@app.route('/show_myloans')
def show_myloans():
    return render_template('/show_myloans.html')

@app.route('/api/get_loans')
def get_loans():
    try:
        with mysql.connection.cursor() as cursor:
            query = "SELECT book_ISBN, return_date, status from Loan where user_id = %s and (status = 'Active' or status = 'Late Active');"
            user_id = str(session['user'])
            params = (user_id,)
            cursor.execute(query, params)
            mysql.connection.commit()
            data = cursor.fetchall()
            response = []

            for loans in data:
                response.append({
                    "isbn" : loans[0],
                    "return_date" : loans[1],
                    "status" : loans[2]
                })
            return jsonify(response)
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
    
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run()
