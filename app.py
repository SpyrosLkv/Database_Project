from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toyot2002'
app.config['MYSQL_DATABASE_DB'] = 'semester_project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signup')
def signup():

    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def signUp():
    # create user code will be here
    conn = None
    cursor = None
    try:
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        username = request.form['inputUserName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if first_name and last_name and _email and username and _password:
            conn = mysql.connect()  # connect Mysql if all good
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (first_name,last_name, username, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    # except Exception as e: (Should really have a try: catch: here, will work on it..12/05)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
