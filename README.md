
# Building a Secure Website


## Description

This is a Flask application that demonstrates a basic login system for a local community library that has been built with
sufficient security measures put in place.

<img src="https://i.imgur.com/3NGERXD.png" alt="Library - Flask" width="600">

## Technologies Used 

The application has been built using:
 - Python
 - HTML 
 - Javascript
 - SQLite database.

## Requirements

To run this app, you need to have the following installed:

- Python 3.5+
- Flask
- Flask-WTF
- Flask-Bcrypt
- Flask-Login
- SQLite3

## Installation

To run the app flawlessly, satisfy the requirements

```bash
$ pip install -r requirements.txt
```


## Run the application

1. Run the main.py script to start the Flask application.
2. Navigate to http://localhost:5000/signup in a web browser to access the signup page.
3. Fill out the required information on the "Sign Up" page and click the "Submit" button.
4. After successfully creating an account, you will be redirected to the "Log In" page. Log in with your new account credentials.
5. Once you are logged in, you will be redirected to the "Profile" page. Here you can view your details.
6. You can add and view address information on the profile page.
8. Search library of books by clicking on option on the navigation bar.
9. When a result is returned from a search, you have the option to Review and Reserve books.
10. To log out, click the "Log Out" button on the navigation bar.


## File structure

The following files are included in this application:

- main.py: The main Flask application file.
- templates/: Contains all the HTML templates used in the application.
- static/: Contains all the static files (CSS, and images) used in the application.
- requirements.txt: Contains the list of required packages for the application.
- README.txt: The readme file you are currently reading.


## Contributing
Contributions are welcome, if you find a bug, feel free to submit an issue.
