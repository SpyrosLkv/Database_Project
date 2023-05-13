from flask import Flask, render_template, request, json
from flask_mysqldb import MySQL
import hashlib
import binascii
app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toyot2002'
app.config['MYSQL_DB'] = 'semester_project'


mysql = MySQL(app)

def HashPass(original_text):
    hash_password = hashlib.sha256(original_text.encode()).digest()
    answer = binascii.hexlify(hash_password).decode()
    return answer

@app.route("/")
def main():
    return render_template('index.html')


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
            conn = mysql.connection
            cursor = conn.cursor()

            query = "select username from Users where username = %s;"
            params = (username,)
            cursor.execute(query,params)
            data = cursor.fetchall()

            if len(data) == 0:
                query = "insert into Pending_Registrations (username,password_hashed,first_name,last_name,birth_date,email,user_role,library_id) values (%s,%s,%s,%s,%s,%s,%s,"+str(library_id)+");"
                params = (username,HashPass(_password),first_name,last_name,birth_date,_email,user_role)
                print(query,params)
                cursor.execute(query,params)
                print("now we're trying to commit")
                conn.commit()
                print("now we send back a message")
                return json.dumps({'message': 'User created successfully !'})
                print("this shouldve returned")
            else:
                print("len!=0")
                return 'hello'
            
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        print("the exception is:",str(e))
        return json.dumps({'error': str(e)})
    # except Exception as e: (Should really have a try: catch: here, will work on it..12/05)
    finally:
        print("finally")
        cursor.close()
        print("cursored")
        conn.close()
        print("connectioned")


if __name__ == "__main__":
    app.run()
