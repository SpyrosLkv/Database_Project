from flask import Flask, render_template, request, json, redirect, session
from flask_mysqldb import MySQL
import hashlib
import binascii
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
                if role == "Student":
                    return json.dumps({'message': 'Credentials Correct!', 'redirect_url': '/Studenthome'})
                if role == "Teacher":
                    return json.dumps({'message': 'Credentials Correct!', 'redirect_url': '/Teacherhome'})
                if role == "Operator":
                    return json.dumps({'message': 'Credentials Correct!', 'redirect_url': '/Operatorhome'})
                if role == "Admin":
                    return json.dumps({'message': 'Credentials Correct!', 'redirect_url': '/Adminhome'})
                
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
def StudentHome():
    if session.get('user'):
        return render_template('Teacherhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')
    

@app.route('/Operatorhome')
def StudentHome():
    if session.get('user'):
        return render_template('Operatorhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')
    
@app.route('/Adminhome')
def StudentHome():
    if session.get('user'):
        return render_template('Adminhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/userhome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
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

    

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run()
