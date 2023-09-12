from flask import Flask, render_template, request, url_for, flash, session, g
from datetime import timedelta
# Import to apply CSRF Functionality
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import redirect
import sqlite3
from sqlite3 import Error
# Import Bcrypt
from flask_bcrypt import Bcrypt

# Import LoginManager, login_user, current_user, logout_user, login_required
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

db_file = "mySQLite.db"


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_database():
    """ create a database connection to a SQLite database and create the relevant tables """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # cursor object
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS USER")
        # Creating USER table
        table = """ CREATE TABLE USER (
                            Username VARCHAR(255) PRIMARY KEY,
                            Password VARCHAR(255) NOT NULL,
                            Email VARCHAR(255) NOT NULL,
                            First_Name CHAR(25),
                            Last_Name CHAR(25),
                            Gender CHAR(25)
                            ); """
        cursor.execute(table)

        # Create Genre table
        cursor.execute("DROP TABLE IF EXISTS FAVOURITE_GENRE")
        table = """ CREATE TABLE FAVOURITE_GENRE (
                                       Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       GenreName VARCHAR(255),
                                       Username VARCHAR(255),
                                       FOREIGN KEY(Username) REFERENCES USER(Username)
                                   ); """

        cursor.execute(table)
        # Drop the USER table if already exists.

        cursor.execute("DROP TABLE IF EXISTS SHIPPING_INFO")
        # Creating shipping_info table
        table = """ CREATE TABLE SHIPPING_INFO (
                                Username VARCHAR(255) NOT NULL,
                                Address VARCHAR(255) NOT NULL,
                                City VARCHAR(255) NOT NULL,
                                State VARCHAR(255) NOT NULL,
                                ZIP VARCHAR(255) NOT NULL,
                                FOREIGN KEY(Username) REFERENCES USER(Username)
                            ); """

        cursor.execute(table)

        cursor.execute("DROP TABLE IF EXISTS PAYMENT_INFO")

        cursor.execute("DROP TABLE IF EXISTS BOOK_INFO")

        table = """CREATE TABLE BOOK_INFO (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Title VARCHAR(255) NOT NULL,
                        Author VARCHAR(255) NOT NULL,
                        Genre VARCHAR(255) NOT NULL,
                        Review TEXT
                    ); """

        cursor.execute(table)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def insertData():
    """ create a database connection to a SQLite database and insert data into tables """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # cursor object
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                            VALUES ('Where the Crawdads Sing', 'Delia Owens', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                    VALUES('The Thursday Murder Club', 'Richard Osman', 'Mystery')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                        VALUES('Atomic Habits', 'James Clear', 'Non-Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                        VALUES('The Silent Patient', 'Alex Michaelides', 'Mystery')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                VALUES('The Boy, the Mole, the Fox and the Horse', 'Charlie Mackesy', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                             VALUES('Becoming', 'Michelle Obama', 'Non-Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                         VALUES('The Alchemist', 'Paulo Coelho', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                   VALUES('The Book of Dust: The Secret Commonwealth', 'Philip Pullman', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                VALUES('The Beekeeper of Aleppo', 'Christy Lefteri', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                 VALUES('Girl, Woman, Other', 'Bernardine Evaristo', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                        VALUES('Normal People', 'Sally Rooney', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                        VALUES('Educated', 'Tara Westover', 'Non-Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                         VALUES('The Testaments', 'Margaret Atwood', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                         VALUES('The Dutch House', 'Ann Patchett', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                         VALUES('The Water Dancer', 'Ta-Nehisi Coates', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                        VALUES('The Giver of Stars', 'Jojo Moyes', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                 VALUES('The Mirror and the Light', 'Hilary Mantel', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                 VALUES('An American Marriage', 'Tayari Jones', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                 VALUES('The Overstory', 'Richard Powers', 'Fiction')''')
        cursor.execute('''INSERT INTO BOOK_INFO (Title, Author, Genre)
                                                 VALUES('The Nickel Boys', 'Colson Whitehead', 'Fiction')''')
        # persist the changes
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


# Press the green button in the gutter to run the script.
app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True
# enable CSRF protection
csrf = CSRFProtect(app)

# Create a Bcrypt object
bcrypt = Bcrypt(app)

# Create a LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginAction'


# Create a User Class for the user that will be stored when the user is logged in
class User():
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


# Define a userloader function
@login_manager.user_loader
def load_user(username):
    return User(username)


# Set a secret key for the login session
app.secret_key = 'super secret key'


# check is user is authenticated/logged
@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('profile'))
    return render_template("signup.html")


@app.route('/signupAction', methods=['POST'])
def signupAction():
    # initalize variables
    username = ""
    password = ""
    email = ""
    fname = ""
    lname = ""
    gender = ""
    list_preferred_genres = []
    # retrieve data
    if request.form.get("username"):
        username = request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")
        # password must be at least 10 characters
        if len(password) < 10:
            flash("Password must be at least 10 characters long.")
            return redirect(url_for('signup'))
        # This password is a normal string
        # Therefore, we need to hash it before we put it in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print("True Password: ", password, ", Hashed Password: ", hashed_password)
        password = hashed_password

    if request.form.get("email"):
        email = request.form.get("email")
    if request.form.get("fname"):
        fname = request.form.get("fname")
    if request.form.get("lname"):
        lname = request.form.get("lname")
    if request.form.get("gender"):
        gender = request.form.get("gender")
    if request.form.get("selected_fiction"):
        list_preferred_genres.append("Fiction")
    if request.form.get("selected_non_fiction"):
        list_preferred_genres.append("Non-Fiction")
    if request.form.get("selected_horror"):
        list_preferred_genres.append("Horror")
    if request.form.get("selected_romance"):
        list_preferred_genres.append("Romance")
    if request.form.get("selected_children"):
        list_preferred_genres.append("Children")
    if request.form.get("selected_mystery"):
        list_preferred_genres.append("Mystery")
    if request.form.get("selected_cooking"):
        list_preferred_genres.append("Cooking")
    if request.form.get("selected_sport"):
        list_preferred_genres.append("Sport")

    try:
        # connect to DB
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # insert user data into USER table
        myquery = "INSERT INTO USER (Username,Password,Email,First_Name,Last_Name,Gender) VALUES (?,?,?,?,?,?)"
        print("My query is: ", myquery)
        cursor.execute(myquery, (username, password, email, fname, lname, gender))
        # insert users favourite genre into table
        for genreName in list_preferred_genres:
            myquery = "INSERT INTO FAVOURITE_GENRE (GenreName,Username) VALUES (?,?)"
            print("My query is: ", myquery)
            cursor.execute(myquery, (genreName, username))
        conn.commit()

        # if this works, this means the user have been added successfully
        # Therefore, we need to send them to the login page
    except Error as e:
        # if the user is not added, we will get an exception which will be caught here
        # So we need to say what to do if the user signup has failed and send them to the sign up page again
        flash("Failed to signup. Try again!")
        return redirect(url_for('signup'))
    finally:
        if conn:
            conn.close()
    flash("Account created successfully.")
    return redirect(url_for('login'))


# this route is used for login page.
@app.route('/login')
def login():
    # If user is already logged in we need to redirect them to their profile
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('profile'))
    return render_template("login.html")


# this route is used to display the terms and conditions
@app.route('/terms-conditions')
def terms_conditions():
    return render_template("terms-conditions.html")


# this route is used as part of login function
@app.route('/loginAction', methods=['POST'])
def loginAction():
    username = ""
    password = ""
    # get username and password from submitted form.
    if request.form.get("username"):
        username = request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myquery = "SELECT Password FROM USER WHERE Username=?"
        data = cursor.execute(myquery, (username,))
        passwordInDB = None
        for row in data:
            passwordInDB = row[0]
        if passwordInDB:
            # We have found a username matching the one provide for the login
            # Now, we need to check that the password provide for the login is also correct
            validPassword = bcrypt.check_password_hash(passwordInDB, password)

            # If the passwords match, we need to mark them as logged in and send them to their profile
            # Else we need to send them to the login page again
            if validPassword:
                login_user(User(username))
                flash("You are now logged in.")
                return redirect(url_for('profile'))
            else:
                flash("Your username or password are incorrect! Try to login again.")
                return redirect(url_for('login'))

            pass
        else:
            # The Username does not exist
            # we need to send them to the login page again
            flash("Your username or password is incorrect! Try to login again.")
            return redirect(url_for('login'))
    except Error as e:
        # if there was an error in the login, we will get an exception which will be caught here
        # So we need to send the user to the login page again
        flash("Failed to login. Try again!")
        return redirect(url_for('login'))
    finally:
        if conn:
            conn.close()
    flash("You are now logged in.")
    return redirect(url_for('profile'))


# route to display details of user logged in.
@app.route('/profile', methods=['GET'])
def profile():
    # If the user is not logged in, we need to redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, we need to get their username
    myusername = current_user.username

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myemail = ""
        myfname = ""
        mylname = ""
        mygender = ""
        mygenre = []
        # Get the personal data of the user
        myquery = "SELECT Email, First_Name, Last_Name, Gender FROM USER WHERE Username=?"
        dataUser = cursor.execute(myquery, (myusername,))
        print("These are the details of the user: ")
        rows = []
        for row in dataUser:
            print(row)
            rows.append(row)
        if len(rows) == 1:
            myemail = rows[0][0]
            myfname = rows[0][1]
            mylname = rows[0][2]
            mygender = rows[0][3]
        else:
            return "Error: the Username does not exist"

        # Get the know genre of the User
        myquery = "SELECT GenreName FROM FAVOURITE_GENRE WHERE Username=?"
        dataUser = cursor.execute(myquery, (myusername,))
        print("These are the user's known genres: ")
        for row in dataUser:
            print(row)
            mygenre.append(row[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    # redner the profile page with the users details.
    return render_template("profile.html", username=myusername, email=myemail, fname=myfname, lname=mylname,
                           gender=mygender, genre=mygenre)


# route to address input
@app.route('/address', methods=['GET', 'POST'])
def address():
    # If the user is not logged in, we need to redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, we need to get their username
    myusername = current_user.username
    # if form submitted get value of form fields
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        try:
            # connect database
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            # insert values into SHIPPING INFO table
            myquery = "INSERT INTO SHIPPING_INFO (Username, Address, City, State, Zip) VALUES (?, ?, ?, ?, ?)"
            print("My query is: ", myquery)
            cursor.execute(myquery, (myusername, address, city, state, zip))
            # commit and redirect to delivery_payment page
            conn.commit()
            flash('0')
            return redirect(url_for('delivery_payment'))
        except Exception as e:
            print('Error:', e)
            flash('An error occurred while saving your information. Please try again.')
        finally:
            conn.close()
    # if form not submitted, address page will be rendered
    return render_template('address.html')


# route the prepopulated address information page.
@app.route('/delivery_payment', methods=['GET'])
def delivery_payment():
    # If the user is not logged in, we need to redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, we need to get their username
    myusername = current_user.username

    conn = None
    try:
        # connect to the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myaddress = ""
        mycity = ""
        mystate = ""
        myzip = ""
        # Get the personal data of the user
        myquery = "SELECT Address, City, State, Zip FROM SHIPPING_INFO WHERE Username=?"
        dataUser = cursor.execute(myquery, (myusername,))
        print("My query is: ", myquery)
        rows = []
        for row in dataUser:
            print(row)
            rows.append(row)
        if len(rows) == 1:
            myaddress = rows[0][0]
            mycity = rows[0][1]
            mystate = rows[0][2]
            myzip = rows[0][3]
        else:
            return "Error: the Username does not exist"
    except Error as e:
        print(e)
    finally:
        # close db connection
        if conn:
            conn.close()
    # render the delivery_payment page with the address information.
    return render_template("delivery_payment.html", username=myusername, address=myaddress, city=mycity, state=mystate,
                           zip=myzip
                           )


# route to homepage
@app.route("/homepage")
def homepage():
    # Get the message parameter and render the homepage with the message.
    message = request.args.get('message')
    return render_template('homepage.html', message=message)


# Defining the search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    # If the user is not logged in, redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, get their username
    myusername = current_user.username
    if request.method == "POST":
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Sanitize the user input
        title = request.form['q']
        # Get information on book from search
        query = "SELECT * FROM BOOK_INFO WHERE Title = ?"
        cursor.execute(query, (title,))

        # Fetch the result of the query
        data = cursor.fetchall()

        # Close the db connection
        cursor.close()
        conn.close()
        # render the search page with the query and data
        return render_template('search.html', query=title, data=data)
    else:
        # Return an empty result
        return render_template('search.html', query="", data=[])


# review route
@app.route('/review', methods=['GET', 'POST'])
def review():
    # If the user is not logged in, redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, get their username
    myusername = current_user.username
    if request.method == 'POST':
        # Get the form data from request.form
        title = request.form['title']
        review = request.form['review']
        # Connect to the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Insert the review into the database
        cursor.execute("UPDATE BOOK_INFO SET Review=? WHERE Title=?", (review, title))
        conn.commit()
        cursor.close()
        conn.close()
        # Redirect to the home page and show a confirmation message
        flash('Review submitted successfully!')
        return redirect(url_for('homepage'))

    else:
        title = request.args.get('title')
        # Render the review page
        return render_template('review.html', book_title=title)


# reserved route
@app.route('/reserved', methods=['GET'])
def reserved():
    # If the user is not logged in, redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, get their username
    myusername = current_user.username
    # get the book title and render to reserved page
    title = request.args.get('title')
    return render_template('reserved.html', title=title)


# route confirm reservation
@app.route('/confirm-reservation', methods=['POST'])
def confirm_reservation():
    # If the user is not logged in, redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access this page.")
        return redirect(url_for('login'))

    # If the user is logged in, get their username
    myusername = current_user.username
    # get the book title and render to reserved page
    title = request.form['title']
    # Redirect to the homepage with a message confirming the reservation
    message = f"Reservation for '{title}' has been confirmed."
    return redirect(url_for('homepage', message=message))


@app.route("/logout")
def logout():
    # If the user is log in, then logout the user
    if current_user.is_authenticated:
        logout_user()
    flash("Logout successful.")
    return redirect(url_for('login'))


@app.before_request
def before_request():
    # Make the session permanent by setting its lifetime to 20 minutes
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    # Indicate that the session has been modified
    session.modified = True
    # Set the variable 'g.user' to the current user
    g.user = current_user


if __name__ == '__main__':
    app.run(debug=True)
    ##create_database()
    ##insertData()
