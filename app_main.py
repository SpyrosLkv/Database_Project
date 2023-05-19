from flask import Flask, render_template, request, json, redirect, session, jsonify
from flask_mysqldb import MySQL
import hashlib
import binascii
from datetime import datetime
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
        library_id = int(request.form['inputLibrary'])

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
                    query = "insert into Pending_Registrations (username,password_hashed,first_name,last_name,birth_date,email,user_role,library_id) values (%s,%s,%s,%s,%s,%s,%s,"+str(library_id)+");"
                    params = (username,HashPass(_password),first_name,last_name,birth_date,_email,user_role)
                    cursor.execute(query,params)
                    mysql.connection.commit()
                    # return redirect('/')
                    # return render_template('index.html')
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
                return json.dumps({'redirect_url': '/pending_registrations'})
            else:
                return json.dumps({'error': 'Something has gone wrong!'})
            
    except Exception as e:
        return json.dumps({'error': str(e)})
    
    

    #retrive data from the request
    response = 1

    return response;

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

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run()
