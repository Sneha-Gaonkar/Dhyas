from flask import Flask, render_template, request, redirect, session, jsonify, flash
import mysql.connector
import os
import pandas as pd
import logging
from pandas.api.types import is_numeric_dtype
from PIL import Image, ImageDraw, ImageFont
import datetime
# from logging.config import dictConfig
# #Adding loggers Config
# dictConfig(
#     {
#         "version": 1,
#         "formatters": {
#             "default": {
#                 "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
#                  "datefmt": "%B %d, %Y %H:%M:%S %Z",
#             }
#         },
#         "handlers": {
#             "size-rotate": {
#                 "class": "logging.handlers.RotatingFileHandler",
#                 "filename": "/home/dhyas/ElectionApp/EManagement/logs/EManagmentApp.log",
#                 "maxBytes": 1000000,
#                 "backupCount": 30,
#                 "formatter": "default",
#                 },
#             },
#         "file": {
#                 "class": "logging.FileHandler",
#                 "filename": "flask.log",
#                 "formatter": "default",
#             },
#         "root": {"level": "DEBUG", "handlers": ["size-rotate"]},
#     }
# )
#

# Initialize Flask app
app = Flask(__name__, static_folder='C:/Users/ADMIN/PycharmProjects/EManagementDemo/images')# Path to access images folder for html files
app.secret_key = os.urandom(24)

# # Initialize Flask app
# app = Flask(__name__, static_folder='/home/dhyas/ElectionApp/EManagement/static')# Path to access images folder for html files
# app.secret_key = os.urandom(24)
# UPLOAD_FOLDER = 'path_to_upload_folder'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # Configure logging
# logging.basicConfig(level=logging.DEBUG)




# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'new_password',
    'database': 'election'
}
# # MySQL database connection configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'dhyas_operator',
#     'password': 'Krishn@19561107',
#     'database': 'dhyas_election'
# }




# @app.route('/fetch_signup_notifications')
# def fetch_signup_notifications():
#     try:
#         # Fetch the database_name and table_name associated with the admin in the session
#         admin_database = session.get('database_name')
#         admin_table = session.get('table_name')
#         if not admin_database or not admin_table:
#             return jsonify({'error': 'Database name or table name not found in session.'})
#
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Construct the table name based on the admin's database name and table name
#         table_name = f"admin_{admin_database.lower()}_{admin_table.lower()}_signupnotifications"
#
#         # Fetch signup notifications from the dynamically constructed table
#         query = f"SELECT * FROM {table_name}"
#         cursor.execute(query)
#         notifications = cursor.fetchall()
#
#         return jsonify(notifications)
#
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': 'An error occurred.'})
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()


@app.route('/fetch_signup_notifications')
def fetch_signup_notifications():
    try:
        # Fetch the database_name, table_name, and sub_database_name associated with the admin in the session
        admin_database = session.get('database_name')
        admin_sub_database = session.get('sub_database_name')  # Added for sub dropdown
        admin_table = session.get('table_name')

        if not admin_database or not admin_table:
            return jsonify({'error': 'Database name or table name not found in session.'})

        if admin_database == 'Vidhan_Parishad' and admin_sub_database:
            admin_database = admin_sub_database

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Construct the table name based on the admin's database name and table name
        table_name = f"admin_{admin_database.lower()}_{admin_table.lower()}_signupnotifications"

        # Fetch signup notifications from the dynamically constructed table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        notifications = cursor.fetchall()

        return jsonify(notifications)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred.'})

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



# @app.route('/process_signup_notification', methods=['POST'])
# def process_signup_notification():
#     if request.method == 'POST':
#         id = request.form['id']
#         action = request.form['action']
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Get the database_name and table_name associated with the admin session
#             admin_database = session.get('database_name')
#             admin_table = session.get('table_name')
#             if not admin_database or not admin_table:
#                 return render_template('admin_panel.html', error_message='Database name or table name not found in session.')
#
#             # Construct the table name based on the admin's database name and table name
#             table_name = f"admin_{admin_database.lower()}_{admin_table.lower()}_signupnotifications"
#
#             # Get signup notification details from the admin-specific table
#             cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (id,))
#             notification = cursor.fetchone()
#
#             print("Fetched notification:", notification)  # Debug print
#
#             if notification:
#                 # If admin approves, insert into signup and login tables
#                 if action == 'approve':
#                     # Insert into signup table
#                     signup_query = "INSERT INTO signup (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
#                     cursor.execute(signup_query, (notification['username'], notification['password'], notification['email'], notification['database_name'], notification['table_name']))
#                     conn.commit()
#
#                     # Insert into login table
#                     login_query = "INSERT INTO login (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
#                     cursor.execute(login_query, (notification['username'], notification['password'], notification['email'], notification['database_name'], notification['table_name']))
#                     conn.commit()
#
#                     # Remove the signup notification from the table
#                     cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
#                     conn.commit()
#
#                     # Set success message for account creation
#                     success_message_account = 'Signup request approved.'
#                     return render_template('admin_panel.html', success_message_account=success_message_account, error_message=None)
#                 # If admin refuses, remove the signup notification
#                 elif action == 'refuse':
#                     cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
#                     conn.commit()
#
#                     # Set success message for signup refusal
#                     success_message_refusal = 'Signup request refused.'
#                     return render_template('admin_panel.html', success_message_refusal=success_message_refusal, error_message=None)
#             else:
#                 # Set error message for notification not found
#                 error_message = 'Signup notification not found.'
#                 return render_template('admin_panel.html', success_message=None, error_message=error_message)
#         except Exception as e:
#             print("Error:", e)  # Print the error message
#             import traceback
#             traceback.print_exc()  # Print the traceback
#             return jsonify({'error': 'An error occurred.'})
#
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()


@app.route('/process_signup_notification', methods=['POST'])
def process_signup_notification():
    if request.method == 'POST':
        id = request.form['id']
        action = request.form['action']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Get the database_name, table_name, and sub_database_name associated with the admin session
            admin_database = session.get('database_name')
            admin_sub_database = session.get('sub_database_name')  # Added for sub dropdown
            admin_table = session.get('table_name')

            if not admin_database or not admin_table:
                return render_template('admin_panel.html', error_message='Database name or table name not found in session.')

            if admin_database == 'Vidhan_Parishad' and admin_sub_database:
                admin_database = admin_sub_database

            # Construct the table name based on the admin's database name and table name
            table_name = f"admin_{admin_database.lower()}_{admin_table.lower()}_signupnotifications"

            # Get signup notification details from the admin-specific table
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (id,))
            notification = cursor.fetchone()

            print("Fetched notification:", notification)  # Debug print

            if notification:
                # If admin approves, insert into signup and login tables
                if action == 'approve':
                    # Insert into signup table
                    signup_query = "INSERT INTO signup (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(signup_query, (notification['username'], notification['password'], notification['email'], notification['database_name'], notification['table_name']))
                    conn.commit()

                    # Insert into login table
                    login_query = "INSERT INTO login (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(login_query, (notification['username'], notification['password'], notification['email'], notification['database_name'], notification['table_name']))
                    conn.commit()

                    # Remove the signup notification from the table
                    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
                    conn.commit()

                    # Set success message for account creation
                    success_message_account = 'Signup request approved.'
                    return render_template('admin_panel.html', success_message_account=success_message_account, error_message=None)
                # If admin refuses, remove the signup notification
                elif action == 'refuse':
                    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
                    conn.commit()

                    # Set success message for signup refusal
                    success_message_refusal = 'Signup request refused.'
                    return render_template('admin_panel.html', success_message_refusal=success_message_refusal, error_message=None)
            else:
                # Set error message for notification not found
                error_message = 'Signup notification not found.'
                return render_template('admin_panel.html', success_message=None, error_message=error_message)
        except Exception as e:
            print("Error:", e)  # Print the error message
            import traceback
            traceback.print_exc()  # Print the traceback
            return jsonify({'error': 'An error occurred.'})

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main_admin_panel', methods=['GET', 'POST'])
def main_admin_panel():
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Insert the new admin into the superadmin table
            signup_query = """
                INSERT INTO superadmin (username, password, email)
                VALUES (%s, %s, %s)
            """
            cursor.execute(signup_query, (username, password, email))
            conn.commit()

            success_message = 'Admin access created successfully.'
            return redirect('/view_superadmin')  # Redirect to admin list page after successful creation

        except Exception as e:
            print("Error:", e)
            error_message = 'An error occurred while creating admin access.'

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    # Render the main_admin_panel.html template with messages
    return render_template('main_admin_panel.html', error_message=error_message, success_message=success_message)

# @app.route('/createadmin_access', methods=['GET', 'POST'])
# def createadmin_access():
#     error_message = None
#     success_message = None
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         election_type = request.form['database_name']
#         constituency = request.form['table_name']
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             signup_query = f"INSERT INTO admin (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(signup_query, (username, password, email, election_type, constituency))
#             conn.commit()
#
#             success_message = 'Admin access created successfully.'
#             return redirect('/view_admin')
#
#         except Exception as e:
#             print("Error:", e)
#             error_message = 'An error occurred.'
#
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()
#
#     # If it's a GET request or if there was an error, render the createadmin_access.html template
#     return render_template('createadmin_access.html', error_message=error_message, success_message=success_message)
#

# @app.route('/createadmin_access', methods=['GET', 'POST'])
# def createadmin_access():
#     error_message = None
#     success_message = None
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         election_type = request.form['database_name']
#         constituency = request.form['table_name']
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Insert the new admin into the admin table
#             signup_query = """
#                 INSERT INTO admin (username, password, email, database_name, table_name)
#                 VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute(signup_query, (username, password, email, election_type, constituency))
#             conn.commit()
#
#             # Create the new table for signup notifications
#             notification_table_name = f"admin_{election_type.lower()}_{constituency.lower()}_signupnotifications"
#             create_table_query = f"""
#                 CREATE TABLE `{notification_table_name}` (
#                     `id` int NOT NULL AUTO_INCREMENT,
#                     `username` varchar(255) NOT NULL,
#                     `email` varchar(255) NOT NULL,
#                     `database_name` varchar(255) NOT NULL,
#                     `signup_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
#                     `password` varchar(50) DEFAULT NULL,
#                     `table_name` varchar(255) DEFAULT '',
#                     PRIMARY KEY (`id`)
#                 )
#             """
#             cursor.execute(create_table_query)
#             conn.commit()
#
#             success_message = 'Admin access created successfully.'
#             return redirect('/view_admin')
#
#         except Exception as e:
#             print("Error:", e)
#             error_message = 'An error occurred.'
#
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()
#
#     # If it's a GET request or if there was an error, render the createadmin_access.html template
#     return render_template('createadmin_access.html', error_message=error_message, success_message=success_message)
#

# @app.route('/createadmin_access', methods=['GET', 'POST'])
# def createadmin_access():
#     error_message = None
#     success_message = None
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         election_type = request.form['database_name']
#         constituency = request.form['table_name']
#         sub_election_type = request.form.get('sub_database_name')  # Get sub dropdown value if exists
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             if election_type == 'Vidhan_Parishad' and sub_election_type:
#                 election_type = sub_election_type
#
            # # Insert the new admin into the admin table
            # signup_query = """
            #     INSERT INTO admin (username, password, email, database_name, table_name)
            #     VALUES (%s, %s, %s, %s, %s)
            # """
            # cursor.execute(signup_query, (username, password, email, election_type, constituency))
            # conn.commit()
#
#             # Create the new table for signup notifications
#             notification_table_name = f"admin_{election_type.lower()}_{constituency.lower()}_signupnotifications"
#             create_table_query = f"""
#                 CREATE TABLE `{notification_table_name}` (
#                     `id` int NOT NULL AUTO_INCREMENT,
#                     `username` varchar(255) NOT NULL,
#                     `email` varchar(255) NOT NULL,
#                     `database_name` varchar(255) NOT NULL,
#                     `signup_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
#                     `password` varchar(50) DEFAULT NULL,
#                     `table_name` varchar(255) DEFAULT '',
#                     PRIMARY KEY (`id`)
#                 )
#             """
#             cursor.execute(create_table_query)
#             conn.commit()
#
#             success_message = 'Admin access created successfully.'
#             return redirect('/view_admin')
#
#         except Exception as e:
#             print("Error:", e)
#             error_message = 'An error occurred.'
#
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()
#
#     # If it's a GET request or if there was an error, render the createadmin_access.html template
#     return render_template('createadmin_access.html', error_message=error_message, success_message=success_message)


@app.route('/createadmin_access', methods=['GET', 'POST'])
def createadmin_access():
    error_message = None
    success_message = None

    if request.method == 'POST':
        # Get logged-in username from session for table name
        username_logged_in = session.get('username')
        password = request.form['password']
        email = request.form['email']
        election_type = request.form['database_name']
        constituency = request.form['table_name']
        sub_election_type = request.form.get('sub_database_name')  # Get sub dropdown value if exists
        username_form_data = request.form['username']  # Username from form data

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            if election_type == 'Vidhan_Parishad' and sub_election_type:
                election_type = sub_election_type

            # Insert the new admin into the admin table
            signup_query = """
                INSERT INTO admin (username, password, email, database_name, table_name)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(signup_query, (username_form_data, password, email, election_type, constituency))
            conn.commit()

            # Create table for superadmin details using logged-in username
            superadmin_table_name = f"superadmin_{username_logged_in.lower()}"
            create_superadmin_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{superadmin_table_name}` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `username` varchar(255) NOT NULL,
                    `email` varchar(255) NOT NULL,
                    `database_name` varchar(255) NOT NULL,
                    `signup_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                    `password` varchar(50) DEFAULT NULL,
                    `table_name` varchar(255) DEFAULT '',
                    PRIMARY KEY (`id`)
                )
            """
            cursor.execute(create_superadmin_table_query)
            conn.commit()

            # Insert into dynamically named superadmin table using form data username
            superadmin_insert_query = f"""
                INSERT INTO `{superadmin_table_name}` (username, password, email, database_name, table_name) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(superadmin_insert_query, (username_form_data, password, email, election_type, constituency))
            conn.commit()

            # Create the new table for signup notifications
            notification_table_name = f"admin_{election_type.lower()}_{constituency.lower()}_signupnotifications"
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{notification_table_name}` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `username` varchar(255) NOT NULL,
                    `email` varchar(255) NOT NULL,
                    `database_name` varchar(255) NOT NULL,
                    `signup_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                    `password` varchar(50) DEFAULT NULL,
                    `table_name` varchar(255) DEFAULT '',
                    PRIMARY KEY (`id`)
                )
            """
            cursor.execute(create_table_query)
            conn.commit()

            success_message = 'Admin access created successfully.'
            return redirect('/view_admin')

        except Exception as e:
            print("Error:", e)
            error_message = 'An error occurred while creating admin access.'

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    # Render the createadmin_access.html template with messages
    return render_template('createadmin_access.html', error_message=error_message, success_message=success_message)


# @app.route('/view_admin')
# def view_admin():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Fetch data from admin table
#         cursor.execute("SELECT * FROM admin")
#         admin_data = cursor.fetchall()
#
#         return render_template('view_admin.html', admin_data=admin_data)
#
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred while fetching the admin data."
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()


@app.route('/view_admin')
def view_admin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch data from dynamically named superadmin table
        username = session.get('username')  # Assuming username is stored in session
          # Assuming user_id is stored in session

        superadmin_table_name = f"superadmin_{username.lower()}"
        cursor.execute(f"SELECT * FROM `{superadmin_table_name}`")
        admin_data = cursor.fetchall()

        return render_template('view_admin.html', admin_data=admin_data)

    except Exception as e:
        print("Error:", e)
        return "An error occurred while fetching the superadmin data."

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/view_superadmin')
def view_superadmin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch data from admin table
        cursor.execute("SELECT * FROM superadmin")
        admin_data = cursor.fetchall()

        return render_template('view_superadmin.html', admin_data=admin_data)

    except Exception as e:
        print("Error:", e)
        return "An error occurred while fetching the admin data."

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/fetch_superadmin_admin/<username>', methods=['GET'])
def fetch_superadmin_admin(username):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Build table name dynamically
        table_name = f"superadmin_{username}"

        # Fetch data from the dynamically built table
        cursor.execute(f"SELECT * FROM {table_name}")
        admin_data = cursor.fetchall()

        return render_template('fetch_superadmin_admin.html', username=username, admin_data=admin_data)

    except Exception as e:
        print("Error:", e)
        return render_template('fetch_superadmin_admin.html', error="An error occurred while fetching the table data.")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/view_superadmin_admin')
def view_superadmin_admin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch data from admin table
        cursor.execute("SELECT * FROM admin")
        admin_data = cursor.fetchall()

        return render_template('view_superadmin_admin.html', admin_data=admin_data)

    except Exception as e:
        print("Error:", e)
        return "An error occurred while fetching the admin data."

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Check if the user is in the login table
#         query_user = "SELECT * FROM login WHERE username = %s AND password = %s"
#         cursor.execute(query_user, (username, password))
#         user = cursor.fetchone()
#
#         # Check if the user is in the admin table
#         query_admin = "SELECT * FROM admin WHERE username = %s AND password = %s"
#         cursor.execute(query_admin, (username, password))
#         admin = cursor.fetchone()
#
#         # Check if the user is in the superadmin table
#         query_superadmin = "SELECT * FROM superadmin WHERE username = %s AND password = %s"
#         cursor.execute(query_superadmin, (username, password))
#         superadmin = cursor.fetchone()
#
#         user_id = None
#         if superadmin:
#             user_id = superadmin['user_id']
#             session['username'] = username
#             session['user_role'] = 'superadmin'
#         elif admin:
#             user_id = admin['user_id']
#             session['username'] = username
#             session['database_name'] = admin['database_name']
#             session['table_name'] = admin['table_name']
#             session['user_role'] = 'admin'
#         elif user:
#             user_id = user['user_id']
#             session['username'] = username
#             session['database_name'] = user['database_name']
#             session['table_name'] = user['table_name']
#             session['user_role'] = 'user'
#         else:
#             error_message = "Invalid username or password."
#             return render_template('login.html', error_message=error_message)
#
#         # Insert login logs
#         login_time = datetime.datetime.now()
#         ip_address = request.remote_addr
#
#         insert_query = "INSERT INTO loginlogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#         conn.commit()
#
#         if session['user_role'] == 'superadmin':
#             return redirect('/superadminpanel')
#         elif session['user_role'] == 'admin':
#             return redirect('/display_index')
#         else:
#             return redirect('/display_index')
#
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred."
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Check if the user is in the login table
        query_user = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query_user, (username, password))
        user = cursor.fetchone()

        # Check if the user is in the admin table
        query_admin = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query_admin, (username, password))
        admin = cursor.fetchone()

        # Check if the user is in the superadmin table
        query_superadmin = "SELECT * FROM superadmin WHERE username = %s AND password = %s"
        cursor.execute(query_superadmin, (username, password))
        superadmin = cursor.fetchone()

        # Check if the user is in the main_admin table
        query_main_admin = "SELECT * FROM main_admin WHERE username = %s AND password = %s"
        cursor.execute(query_main_admin, (username, password))
        main_admin = cursor.fetchone()

        user_id = None
        if superadmin:
            user_id = superadmin['user_id']
            session['username'] = username
            session['user_role'] = 'superadmin'
        elif admin:
            user_id = admin['user_id']
            session['username'] = username
            session['database_name'] = admin['database_name']
            session['table_name'] = admin['table_name']
            session['user_role'] = 'admin'
        elif main_admin:
            user_id = main_admin['user_id']
            session['username'] = username
            session['user_role'] = 'main_admin'
        elif user:
            user_id = user['user_id']
            session['username'] = username
            session['database_name'] = user['database_name']
            session['table_name'] = user['table_name']
            session['user_role'] = 'user'
        else:
            error_message = "Invalid username or password."
            return render_template('login.html', error_message=error_message)

        # Insert login logs
        login_time = datetime.datetime.now()
        ip_address = request.remote_addr

        insert_query = "INSERT INTO loginlogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
        conn.commit()

        if session['user_role'] == 'superadmin':
            return redirect('/superadminpanel')
        elif session['user_role'] == 'admin':
            return redirect('/display_index')
        elif session['user_role'] == 'main_admin':
            return redirect('/main_admin_panel')  # Adjust as per your route for main admin
        else:
            return redirect('/display_index')

    except Exception as e:
        print("Error:", e)
        return "An error occurred."

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Check if the user is in the login table
#         query_user = "SELECT * FROM login WHERE username = %s AND password = %s"
#         cursor.execute(query_user, (username, password))
#         user = cursor.fetchone()
#
#         # Check if the user is in the admin table
#         query_admin = "SELECT * FROM admin WHERE username = %s AND password = %s"
#         cursor.execute(query_admin, (username, password))
#         admin = cursor.fetchone()
#
#         # Check if the user is in the superadmin table
#         query_superadmin = "SELECT * FROM superadmin WHERE username = %s AND password = %s"
#         cursor.execute(query_superadmin, (username, password))
#         superadmin = cursor.fetchone()
#
#         if user:
#             user_id = user['user_id']
#             session['username'] = username
#             session['database_name'] = user['database_name']
#             session['table_name'] = user['table_name']
#             session['user_role'] = 'user'  # Assuming regular users
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO LoginLogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#             return redirect('/display_index')
#
#         elif admin:
#             user_id = admin['user_id']
#             session['username'] = username
#             session['database_name'] = admin['database_name']
#             session['table_name'] = admin['table_name']
#             session['user_role'] = 'admin'
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO loginlogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#             return redirect('/display_index')
#
#
#         elif superadmin:
#             user_id = superadmin['user_id']
#             session['username'] = username
#
#             session['user_role'] = 'superadmin'
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO LoginLogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#
#             # Redirect superadmin to superadmin panel
#
#             return redirect('/superadminpanel')
#
#         else:
#             error_message = "Invalid username or password."
#             return render_template('login.html', error_message=error_message)
#
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred."
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()



# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Check if the user is in the login table
#         query_user = "SELECT * FROM login WHERE username = %s AND password = %s"
#         cursor.execute(query_user, (username, password))
#         user = cursor.fetchone()
#
#
#
#         # Check if the user is in the admin table
#         query_admin = "SELECT * FROM admin WHERE username = %s AND password = %s"
#         cursor.execute(query_admin, (username, password))
#         admin = cursor.fetchone()
#
#         # Check if the user is in the superadmin table
#         query_superadmin = "SELECT * FROM superadmin WHERE username = %s AND password = %s"
#         cursor.execute(query_superadmin, (username, password))
#         superadmin = cursor.fetchone()
#
#         if user:
#             user_id = user['user_id']
#             session['username'] = username
#             session['database_name'] = user['database_name']
#             session['table_name'] = user['table_name']
#             session['user_role'] = 'user'  # Regular users
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO LoginLogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#             # Redirect based on database_name
#             if session['database_name'] in ['Teachers', 'Graduates']:
#                 return redirect('/display_new_index')
#             else:
#                 return redirect('/display_index')
#
#         elif admin:
#             user_id = admin['user_id']
#             session['username'] = username
#             session['database_name'] = admin['database_name']
#             session['table_name'] = admin['table_name']
#             session['user_role'] = 'admin'
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO loginlogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#             # Redirect based on database_name
#             if session['database_name'] in ['Teachers', 'Graduates']:
#                 return redirect('/display_new_index')
#             else:
#                 return redirect('/display_index')
#
#         elif superadmin:
#             user_id = superadmin['user_id']
#             session['username'] = username
#             session['user_role'] = 'superadmin'
#
#             # Insert login logs
#             login_time = datetime.datetime.now()
#             ip_address = request.remote_addr
#
#             insert_query = "INSERT INTO LoginLogs (UserID, Username, LoginTime, IPAddress, LoginSuccess) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (user_id, username, login_time, ip_address, True))
#             conn.commit()
#
#             return redirect('/superadminpanel')
#
#         else:
#             error_message = "Invalid username or password."
#             return render_template('login.html', error_message=error_message)
#
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred."
#
#     finally:
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'conn' in locals() and conn:
#             conn.close()


@app.context_processor
def inject_user_role():
    return dict(user_role=session.get('user_role'))

@app.context_processor
def inject_database_name():
    return dict(database_name=session.get('database_name'))



def get_db_connection(database_name=None):
    config = db_config.copy()
    if database_name:
        config['database'] = database_name
    return mysql.connector.connect(**config)

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         election_type = request.form['database_name']
#         constituency = request.form['table_name']
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Construct the table name based on the selected election type and constituency
#             table_name = f"admin_{election_type.lower()}_{constituency.lower()}_signupnotifications"
#
#             # Insert into the dynamically constructed table
#             signup_query = f"INSERT INTO {table_name} (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
#             cursor.execute(signup_query, (username, password, email, election_type, constituency))
#             conn.commit()
#
#             flash("Signup request sent for approval. Please wait for admin confirmation. Try to login from your end.")
#             return redirect('/')
#
#         except Exception as e:
#             print("Error:", e)
#             return "An error occurred."
#
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()
#
#     return render_template('signup.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        election_type = request.form['database_name']
        constituency = request.form['table_name']
        sub_election_type = request.form.get('sub_database_name')  # Get sub dropdown value if exists

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            if election_type == 'Vidhan_Parishad' and sub_election_type:
                election_type = sub_election_type

            # Construct the table name based on the selected election type and constituency
            table_name = f"admin_{election_type.lower()}_{constituency.lower()}_signupnotifications"

            # Insert into the dynamically constructed table
            signup_query = f"INSERT INTO {table_name} (username, password, email, database_name, table_name) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(signup_query, (username, password, email, election_type, constituency))
            conn.commit()

            flash("Signup request sent for approval. Please wait for admin confirmation. Try to login from your end.")
            return redirect('/')

        except Exception as e:
            print("Error:", e)
            return "An error occurred."

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('signup.html')



@app.route('/get_databases')
def get_databases():
    databases = ['Lok_Sabha', 'Vidhan_Sabha', 'Zilla_Parishad', 'Nagar_Parishad', 'Nagar_Palika', 'Vidhan_Parishad']
    return jsonify(databases)

# @app.route('/get_tables/<database_name>')
# def get_tables(database_name):
#     try:
#         conn = get_db_connection(database_name)
#         cursor = conn.cursor()
#         cursor.execute("SHOW TABLES")
#         tables = [table[0] for table in cursor.fetchall()]
#         return jsonify(tables)
#     except Exception as e:
#         print("Error fetching tables:", e)
#         return jsonify([])
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()


@app.route('/get_tables/<database_name>')
def get_tables(database_name):
    try:
        conn = get_db_connection(database_name)
        cursor = conn.cursor()

        if database_name == 'Vidhan_Parishad':
            # Special handling for Vidhan_Parishad
            return jsonify(['Teachers', 'Graduates'])

        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        return jsonify(tables)
    except Exception as e:
        print("Error fetching tables:", e)
        return jsonify([])
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/adminpanel')
def adminpanel():
    return render_template('admin_panel.html')




# Define the function to sanitize column names
# def sanitize_column_names(columns):
#     return [col.strip().replace(' ', '_') for col in columns]
#
# # Define the function to sanitize table names
# def sanitize_table_name(filename):
#     return os.path.splitext(filename)[0].replace(' ', '_')




# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     if 'username' not in session or session.get('user_role') != 'superadmin':
#         return redirect('/login')
#
#     selected_db = request.form['database']
#     sub_database = request.form.get('sub_database')  # Use .get to avoid KeyError
#     file = request.files.get('file')
#
#     if not file:
#         logging.error("No file uploaded.")
#         flash("No file uploaded.", 'error')
#         return redirect('/superadminpanel')
#
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#
#     try:
#         file.save(file_path)
#     except Exception as e:
#         logging.error(f"Error saving file: {e}")
#         flash("Error saving file.", 'error')
#         return redirect('/superadminpanel')
#
#     try:
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(file_path)
#         elif file.filename.endswith(('.xls', '.xlsx')):
#             df = pd.read_excel(file_path)
#         else:
#             logging.error("Unsupported file format.")
#             flash("Unsupported file format.", 'error')
#             return redirect('/superadminpanel')
#
#         df.columns = sanitize_column_names(df.columns)
#         df.fillna('', inplace=True)
#
#         if 'SrNo' not in df.columns:
#             df.insert(0, 'SrNo', range(1, 1 + len(df)))
#
#         if is_numeric_dtype(df['SrNo']):
#             df['SrNo'] = df['SrNo'].astype(int)
#             df.set_index('SrNo', inplace=True)
#         else:
#             logging.warning("Non-numeric 'SrNo' column found. Ignoring.")
#             df.drop(columns=['SrNo'], inplace=True)
#
#         # Determine the final database to use
#         final_database = selected_db
#         if selected_db == 'Vidhan_Parishad' and sub_database:
#             final_database = sub_database
#
#         db_config_selected = db_config.copy()
#         db_config_selected['database'] = final_database
#         conn = mysql.connector.connect(**db_config_selected)
#         cursor = conn.cursor()
#
#         table_name = sanitize_table_name(file.filename)
#
#         cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
#
#         # Use TEXT type for columns to avoid row size limits
#         columns_definition = ", ".join([f"`{col}` TEXT" for col in df.columns])
#         create_table_query = f"""
#         CREATE TABLE `{table_name}` (
#             `SrNo` INT AUTO_INCREMENT PRIMARY KEY,
#             {columns_definition}
#         )
#         """
#         logging.debug(f"Executing query: {create_table_query}")
#         cursor.execute(create_table_query)
#
#         for row in df.itertuples(index=False):
#             columns = ', '.join([f"`{col}`" for col in df.columns])
#             values = ', '.join(['%s'] * len(df.columns))
#             insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({values})"
#             cursor.execute(insert_query, tuple(row))
#
#         conn.commit()
#
#         flash(f"File uploaded and data inserted into table '{table_name}' successfully.", 'success')
#         return redirect('/superadminpanel')
#
#     except Exception as e:
#         logging.error(f"Error processing file: {e}")
#         flash(f"An error occurred: {e}", 'error')
#         return redirect('/superadminpanel')
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()
#         if os.path.exists(file_path):
#             os.remove(file_path)
#
#     return "File uploaded and data inserted into table successfully."



@app.route('/superadminpanel')
def superadminpanel():
    # Replace this with actual logic to fetch databases from your MySQL server
    # databases = ['Lok_Sabha', 'Vidhan_Sabha', 'Zilla_Parishad', 'Nagar_Parishad', 'Nagar_Palika', 'Vidhan_Parishad']
    return render_template('newsuperadmin.html')



@app.route('/display_index')
def display_index():
    try:
        # Get parameters from the URL
        username = request.args.get('username')
        database_name = request.args.get('database_name')
        table_name = request.args.get('table_name')

        # Only set session variables if they are provided in the URL (for superadmin)
        if username and database_name and table_name:
            session['username'] = username
            session['database_name'] = database_name
            session['table_name'] = table_name
        else:
            # Ensure session variables are already set for a regular user
            if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
                return redirect('/login')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table_name is not None or empty
        if not session['table_name']:
            return "No table name provided.", 400

        # Check if the Address column exists
        query = f"SHOW COLUMNS FROM {session['database_name']}.{session['table_name']} LIKE 'Address'"
        cursor.execute(query)
        address_column_exists = cursor.fetchone() is not None

        # Construct the query dynamically using session variables
        query = "SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Gat, Gat_Name, Gan, Gan_Name"

        # Check if address column exists and add it to the query
        if address_column_exists:
            query += ", Address"

        # Complete the query with the table name from the session
        query += f" FROM {session['database_name']}.{session['table_name']}"

        # Execute the query
        cursor.execute(query)

        # Fetch all the data from the executed query
        table_data = cursor.fetchall()

        # Replace gender values with "Female" or "Male"
        for row in table_data:
            if row['Gender'] == 'F':
                row['Gender'] = 'Female'
            elif row['Gender'] == 'M':
                row['Gender'] = 'Male'

        # Filter the data based on search parameters, if any
        search_query = request.args.get('search')
        if search_query:
            table_data = [row for row in table_data if search_query.lower() in row.values()]




        # Calculate total count of male, female, and transgender entries after filtering
        total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
        total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
        total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

        # Total number of rows after filtering
        total_rows = len(table_data)

        return render_template('index.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])

    except Exception as e:

        print("Error fetching data:", e)
        return "An error occurred while fetching data: " + str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# @app.route('/display_index')
# def display_index():
#     try:
#         # Get parameters from the URL
#         username = request.args.get('username')
#         database_name = request.args.get('database_name')
#         table_name = request.args.get('table_name')
#
#         # Only set session variables if they are provided in the URL (for superadmin)
#         if username and database_name and table_name:
#             session['username'] = username
#             session['database_name'] = database_name
#             session['table_name'] = table_name
#         else:
#             # Ensure session variables are already set for a regular user
#             if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
#                 return redirect('/login')
#
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Ensure table_name is not None or empty
#         if not session['table_name']:
#             return "No table name provided.", 400
#
#         # List of columns to check
#         columns_to_check = ['Address', 'Gat', 'Gat_Name', 'Gan', 'Gan_Name']
#         existing_columns = []
#
#         for column in columns_to_check:
#             query = f"SHOW COLUMNS FROM {session['database_name']}.{session['table_name']} LIKE '{column}'"
#             cursor.execute(query)
#             if cursor.fetchone() is not None:
#                 existing_columns.append(column)
#
#         # Construct the query dynamically using session variables
#         base_columns = ['Part_No', 'SrNo', 'Name', 'Epic_No', 'Age', 'Gender']
#         query = "SELECT " + ", ".join(base_columns + existing_columns)
#         query += f" FROM {session['database_name']}.{session['table_name']}"
#
#         # Execute the query
#         cursor.execute(query)
#
#         # Fetch all the data from the executed query
#         table_data = cursor.fetchall()
#
#         # Replace gender values with "Female" or "Male"
#         for row in table_data:
#             if row['Gender'] == 'F':
#                 row['Gender'] = 'Female'
#             elif row['Gender'] == 'M':
#                 row['Gender'] = 'Male'
#
#         # Filter the data based on search parameters, if any
#         search_query = request.args.get('search')
#         if search_query:
#             table_data = [row for row in table_data if search_query.lower() in str(row.values()).lower()]
#
#         # Calculate total count of male, female, and transgender entries after filtering
#         total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
#         total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
#         total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
#
#         # Total number of rows after filtering
#         total_rows = len(table_data)
#
#         return render_template('index.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])
#
#     except Exception as e:
#         print("Error fetching data:", e)
#         return "An error occurred while fetching data: " + str(e)
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()



@app.route('/display_index_name')
def display_index_name():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name} ORDER BY Name"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in row.values()]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('varna.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')




@app.route('/display_index_age')
def display_index_age():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name} ORDER BY Age"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in row.values()]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('vaya.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')



# @app.route('/display_index_family')
# def display_index_family():
#     if 'username' in session and 'database_name' in session:
#         conn = None
#         cursor = None
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Check if the user's table name is provided in the URL
#             if 'table_name' in request.args:
#                 table_name = request.args['table_name']
#             else:
#                 # If not provided, retrieve the table name from the session
#                 table_name = session.get('table_name')
#
#             # Ensure table_name is not None or empty
#             if not table_name:
#                 return "No table name provided.", 400
#
#             # Construct the query dynamically using session variables
#             query = f"""
#             SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, House_No, Relative_Name, Surname, Relation
#             FROM {session['database_name']}.{table_name}
#             ORDER BY House_No
#             """
#             cursor.execute(query)
#             table_data = cursor.fetchall()
#
#             # Replace gender values with "Female" or "Male"
#             for row in table_data:
#                 if row['Gender'] == 'F':
#                     row['Gender'] = 'Female'
#                 elif row['Gender'] == 'M':
#                     row['Gender'] = 'Male'
#                 elif row['Gender'] == 'T':
#                     row['Gender'] = 'Transgender'
#
#             # Filter the data based on search parameters, if any
#             search_query = request.args.get('search')
#             if search_query:
#                 table_data = [row for row in table_data if search_query.lower() in str(row.values()).lower()]
#
#             # Custom order for family members
#             family_order = {
#                 'Father': 1, 'Mother': 2, 'Uncle': 3, 'Aunt': 4, 'Cousin': 5,
#                 'Son': 6, 'Daughter': 7, 'Brother': 8, 'Sister': 9, 'Husband': 10,
#                 'Wife': 11, 'Grandfather': 12, 'Grandmother': 13, 'Other': 14
#             }
#
#             # Sort table_data based on custom criteria
#             sorted_table_data = sorted(
#                 table_data,
#                 key=lambda row: (
#                     row['House_No'] if row['House_No'] and row['House_No'] != '-' else '',
#                     row['House_No'] in [None, '', '-'],
#                     row['Relative_Name'] if row['House_No'] in [None, '', '-'] else '',
#                     row['Surname'] if row['House_No'] in [None, '', '-'] else '',
#                     family_order.get(row['Relation'], 14),
#                     row['Surname'],
#                     row['Name']
#                 )
#             )
#
#             # Calculate total count of male, female, and transgender entries after filtering
#             total_male = sum(1 for row in sorted_table_data if row['Gender'] == 'Male')
#             total_female = sum(1 for row in sorted_table_data if row['Gender'] == 'Female')
#             total_transgender = sum(1 for row in sorted_table_data if row['Gender'] == 'Transgender')
#
#             # Total number of rows after filtering
#             total_rows = len(sorted_table_data)
#
#             return render_template(
#                 'family.html',
#                 table_data=sorted_table_data,
#                 total_male=total_male,
#                 total_female=total_female,
#                 total_transgender=total_transgender,
#                 total_rows=total_rows,
#                 user_role=session.get('user_role'),
#                 table_name=table_name
#             )
#         except Exception as e:
#             print("Error fetching data:", e)  # Print the specific error message
#             return "An error occurred while fetching data: " + str(e)  # Return the specific error message
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#     else:
#         return redirect('/')

# @app.route('/display_index_family')
# def display_index_family():
#     if 'username' in session and 'database_name' in session:
#         conn = None
#         cursor = None
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Check if the user's table name is provided in the URL
#             if 'table_name' in request.args:
#                 table_name = request.args['table_name']
#             else:
#                 # If not provided, retrieve the table name from the session
#                 table_name = session.get('table_name')
#
#             # Ensure table_name is not None or empty
#             if not table_name:
#                 return "No table name provided.", 400
#
#             # Construct the query dynamically using session variables
#             query = f"""
#             SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, House_No, Relative_Name, Surname, Relation
#             FROM {session['database_name']}.{table_name}
#             ORDER BY
#                 CASE
#                     WHEN House_No IS NULL OR House_No = '' OR House_No = '-' OR House_No = '0' THEN
#                         CASE
#                             WHEN Relation = 'Father' THEN 1
#                             WHEN Relation = 'Mother' THEN 2
#                             WHEN Relation = 'Uncle' THEN 3
#                             WHEN Relation = 'Aunt' THEN 4
#                             WHEN Relation = 'Cousin' THEN 5
#                             WHEN Relation = 'Son' THEN 6
#                             WHEN Relation = 'Daughter' THEN 7
#                             WHEN Relation = 'Brother' THEN 8
#                             WHEN Relation = 'Sister' THEN 9
#                             WHEN Relation = 'Husband' THEN 10
#                             WHEN Relation = 'Wife' THEN 11
#                             WHEN Relation = 'Grandfather' THEN 12
#                             WHEN Relation = 'Grandmother' THEN 13
#                             ELSE 14
#                         END
#                     ELSE House_No
#                 END,
#                 House_No IS NULL OR House_No = '' OR House_No = '-' OR House_No = '0',
#                 Relative_Name,
#                 Surname,
#                 CASE
#                     WHEN Relation = 'Father' THEN 1
#                     WHEN Relation = 'Mother' THEN 2
#                     WHEN Relation = 'Uncle' THEN 3
#                     WHEN Relation = 'Aunt' THEN 4
#                     WHEN Relation = 'Cousin' THEN 5
#                     WHEN Relation = 'Son' THEN 6
#                     WHEN Relation = 'Daughter' THEN 7
#                     WHEN Relation = 'Brother' THEN 8
#                     WHEN Relation = 'Sister' THEN 9
#                     WHEN Relation = 'Husband' THEN 10
#                     WHEN Relation = 'Wife' THEN 11
#                     WHEN Relation = 'Grandfather' THEN 12
#                     WHEN Relation = 'Grandmother' THEN 13
#                     ELSE 14
#                 END,
#                 Surname,
#                 Name
#             """
#             cursor.execute(query)
#             table_data = cursor.fetchall()
#
#             # Replace gender values with "Female" or "Male"
#             for row in table_data:
#                 if row['Gender'] == 'F':
#                     row['Gender'] = 'Female'
#                 elif row['Gender'] == 'M':
#                     row['Gender'] = 'Male'
#                 elif row['Gender'] == 'T':
#                     row['Gender'] = 'Transgender'
#
#             # Filter the data based on search parameters, if any
#             search_query = request.args.get('search')
#             if search_query:
#                 table_data = [row for row in table_data if search_query.lower() in str(row.values()).lower()]
#
#             # Calculate total count of male, female, and transgender entries after filtering
#             total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
#             total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
#             total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
#
#             # Total number of rows after filtering
#             total_rows = len(table_data)
#
#             return render_template(
#                 'family.html',
#                 table_data=table_data,
#                 total_male=total_male,
#                 total_female=total_female,
#                 total_transgender=total_transgender,
#                 total_rows=total_rows,
#                 user_role=session.get('user_role'),
#                 table_name=table_name
#             )
#         except Exception as e:
#             print("Error fetching data:", e)  # Print the specific error message
#             return "An error occurred while fetching data: " + str(e)  # Return the specific error message
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#     else:
#         return redirect('/')


# @app.route('/display_index_family')
# def display_index_family():
#     if 'username' in session and 'database_name' in session:
#         conn = None
#         cursor = None
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor(dictionary=True)
#
#             # Check if the user's table name is provided in the URL
#             if 'table_name' in request.args:
#                 table_name = request.args['table_name']
#             else:
#                 # If not provided, retrieve the table name from the session
#                 table_name = session.get('table_name')
#
#             # Ensure table_name is not None or empty
#             if not table_name:
#                 return "No table name provided.", 400
#
#             # Construct the query dynamically using session variables
#             query = f"""
#             SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, House_No, Relative_Name, Surname, Relation
#             FROM {session['database_name']}.{table_name}
#             """
#             cursor.execute(query)
#             table_data = cursor.fetchall()
#
#             if not table_data:
#                 return "No data found.", 404
#
#             # Generate group IDs
#             group_counter = 1
#             previous_surname = ""
#             previous_house_no = ""
#             group_id = 0
#
#             for row in table_data:
#                 if 'Surname' in row and 'House_No' in row:
#                     # Assign a new group ID if surname or house number changes
#                     if row['Surname'] != previous_surname or row['House_No'] != previous_house_no:
#                         group_id = group_counter
#                         group_counter += 1
#                     row['group_id'] = group_id
#                     previous_surname = row['Surname']
#                     previous_house_no = row['House_No']
#                 else:
#                     # Handle the case where Surname or House_No might be missing
#                     row['group_id'] = None
#
#             # Replace gender values with "Female" or "Male"
#             for row in table_data:
#                 if row['Gender'] == 'F':
#                     row['Gender'] = 'Female'
#                 elif row['Gender'] == 'M':
#                     row['Gender'] = 'Male'
#                 elif row['Gender'] == 'T':
#                     row['Gender'] = 'Transgender'
#
#             # Filter the data based on search parameters, if any
#             search_query = request.args.get('search')
#             if search_query:
#                 table_data = [row for row in table_data if search_query.lower() in str(row.values()).lower()]
#
#             # Calculate total count of male, female, and transgender entries after filtering
#             total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
#             total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
#             total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
#
#             # Total number of rows after filtering
#             total_rows = len(table_data)
#
#             return render_template(
#                 'family.html',
#                 table_data=table_data,
#                 total_male=total_male,
#                 total_female=total_female,
#                 total_transgender=total_transgender,
#                 total_rows=total_rows,
#                 user_role=session.get('user_role'),
#                 table_name=table_name
#             )
#         except Exception as e:
#             print("Error fetching data:", e)  # Print the specific error message
#             return "An error occurred while fetching data: " + str(e)  # Return the specific error message
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#     else:
#         return redirect('/')

@app.route('/display_index_family')
def display_index_family():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"""
            SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, House_No, Relative_Name, Surname, Relation, Gat, Gat_Name, Gan, Gan_Name
            FROM {session['database_name']}.{table_name}
            ORDER BY House_No
            """
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with labels
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'
                elif row['Gender'] == 'T':
                    row['Gender'] = 'Transgender'

            # # Function to group family members
            # def group_family_members(data):
            #     groups = {}
            #     for row in data:
            #         key = (row['House_No'], row['Surname'])  # Group by Surname
            #         if row['Relation'] == 'Wife':
            #             key = (row['House_No'], row['Relative_Name'])  # Use Husband's name for Wife
            #         if key not in groups:
            #             groups[key] = {
            #                 'members': [],
            #                 'group_id': len(groups) + 1  # Assign a unique group_id
            #             }
            #         groups[key]['members'].append(row)
            #         row['group_id'] = groups[key]['group_id']
            #     return groups
            #
            # # Group family members based on House_No and Surname (or Relative_Name for Wife)
            # grouped_data = group_family_members(table_data)
            #
            # # Flatten grouped data for rendering
            # sorted_table_data = []
            # for key in sorted(grouped_data.keys(), key=lambda x: (x[0], x[1])):
            #     sorted_table_data.extend(grouped_data[key]['members'])

            # Calculate totals based on sorted data
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            total_rows = len(table_data)

            return render_template(
                'family.html',
                table_data=table_data,
                total_male=total_male,
                total_female=total_female,
                total_transgender=total_transgender,
                total_rows=total_rows,
                user_role=session.get('user_role'),
                table_name=table_name
            )
        except Exception as e:
            print("Error fetching data:", e)
            return f"An error occurred while fetching data: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_family_new')
def display_index_family_new():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"""
                SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Address, Relative_Name, Gat, Gat_Name, Gan, Gan_Name
                FROM {session['database_name']}.{table_name}
                ORDER BY Address
            """
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with labels
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'
                elif row['Gender'] == 'T':
                    row['Gender'] = 'Transgender'

            # # Function to group family members
            # def group_family_members(data):
            #     groups = {}
            #     for row in data:
            #         key = (row['House_No'], row['Surname'])  # Group by Surname
            #         if row['Relation'] == 'Wife':
            #             key = (row['House_No'], row['Relative_Name'])  # Use Husband's name for Wife
            #         if key not in groups:
            #             groups[key] = {
            #                 'members': [],
            #                 'group_id': len(groups) + 1  # Assign a unique group_id
            #             }
            #         groups[key]['members'].append(row)
            #         row['group_id'] = groups[key]['group_id']
            #     return groups
            #
            # # Group family members based on House_No and Surname (or Relative_Name for Wife)
            # grouped_data = group_family_members(table_data)
            #
            # # Flatten grouped data for rendering
            # sorted_table_data = []
            # for key in sorted(grouped_data.keys(), key=lambda x: (x[0], x[1])):
            #     sorted_table_data.extend(grouped_data[key]['members'])

            # Calculate totals based on sorted data
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            total_rows = len(table_data)

            return render_template(
                'newfamily.html',
                table_data=table_data,
                total_male=total_male,
                total_female=total_female,
                total_transgender=total_transgender,
                total_rows=total_rows,
                user_role=session.get('user_role'),
                table_name=table_name
            )
        except Exception as e:
            print("Error fetching data:", e)
            return f"An error occurred while fetching data: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')



@app.route('/display_index_duplicate')
def display_index_duplicate():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Step 1: Find duplicate names
            duplicate_query = f"""
            SELECT Name
            FROM {session['database_name']}.{table_name}
            GROUP BY Name
            HAVING COUNT(*) > 1
            """
            cursor.execute(duplicate_query)
            duplicate_names = cursor.fetchall()

            # Extract names from the query result
            duplicate_names = [row['Name'] for row in duplicate_names]

            # If there are no duplicate names, return an empty result
            if not duplicate_names:
                return render_template('dubar.html', table_data=[], total_male=0, total_female=0, total_transgender=0, total_rows=0, user_role=session.get('user_role'), table_name=table_name)

            # Step 2: Fetch records that have duplicate names
            # Using parameterized query to avoid SQL injection
            format_strings = ','.join(['%s'] * len(duplicate_names))
            fetch_query = f"""
            SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Gat, Gat_Name, Gan, Gan_Name
            FROM {session['database_name']}.{table_name}
            WHERE Name IN ({format_strings})
            """
            cursor.execute(fetch_query, tuple(duplicate_names))
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in (str(value).lower() for value in row.values())]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('dubar.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')





@app.route('/display_index_surname')
def display_index_surname():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Surname, COUNT(*) AS Count FROM {session['database_name']}.{table_name} GROUP BY Surname ORDER BY Surname"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Check if table_data is empty
            if not table_data:
                return "No data found.", 404

            return render_template('adnav.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)
            return "An error occurred while fetching data: " + str(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')





@app.route('/display_index_surname_list')
def display_index_surname_list():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Retrieve the surname from the query parameter
            surname = request.args.get('surname')

            if not surname:
                return "No surname provided.", 400

            # Retrieve the table name from the session
            table_name = session.get('table_name')
            if not table_name:
                return "No table name provided in session.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Surname, Epic_No, Age, Gender, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name} WHERE Surname = %s"
            cursor.execute(query, (surname,))
            surname_data = cursor.fetchall()

            # Check if surname_data is empty
            if not surname_data:
                surname_data = []  # Ensure surname_data is an empty list if no results found

            return render_template('surnamelist.html', surname_data=surname_data, user_role=session.get('user_role'), surname=surname)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "An error occurred while fetching data: " + str(err), 500
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while fetching data: " + str(e), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')



@app.route('/display_index_deadoralive')
def display_index_deadoralive():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, deadalive, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name}"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in row.values()]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('deadoralive.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')




@app.route('/display_index_votedetails')
def display_index_votedetails():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Vote_Status, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name}"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in row.values()]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('votedetails.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_redgreen')
def display_index_redgreen():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Color, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name}"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # Replace gender values with "Female" or "Male"
            for row in table_data:
                if row['Gender'] == 'F':
                    row['Gender'] = 'Female'
                elif row['Gender'] == 'M':
                    row['Gender'] = 'Male'

            # Filter the data based on search parameters, if any
            search_query = request.args.get('search')
            if search_query:
                table_data = [row for row in table_data if search_query.lower() in row.values()]

            # Calculate total count of male, female, and transgender entries after filtering
            total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

            # Total number of rows after filtering
            total_rows = len(table_data)

            return render_template('redgreen.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_addresswise')
def display_index_addresswise():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Address_of_Polling_Station AS Count FROM {session['database_name']}.{table_name} GROUP BY Address_of_Polling_Station ORDER BY Address_of_Polling_Station"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('addresswisereport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_boothwise')
def display_index_boothwise():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT DISTINCT Section_No_and_Name, No_and_Name_of_Polling_Station, Address_of_Polling_Station FROM {session['database_name']}.{table_name}"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('boothwisereport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_gender')
def display_index_gender():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Gender, COUNT(*) AS count FROM {session['database_name']}.{table_name} GROUP BY Gender"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('genderreport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_caste')
def display_index_caste():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Caste, COUNT(*) AS count FROM {session['database_name']}.{table_name} GROUP BY Caste"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('castereport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_wardwise')
def display_index_wardwise():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Ward, COUNT(*) AS count FROM {session['database_name']}.{table_name} GROUP BY Ward"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('wardwisereport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')


@app.route('/display_index_bloodgroup')
def display_index_bloodgroup():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Check if the user's table name is provided in the URL
            if 'table_name' in request.args:
                table_name = request.args['table_name']
            else:
                # If not provided, retrieve the table name from the session
                table_name = session.get('table_name')

            # Ensure table_name is not None or empty
            if not table_name:
                return "No table name provided.", 400

            # Construct the query dynamically using session variables
            query = f"SELECT Blood_Group, COUNT(*) AS count FROM {session['database_name']}.{table_name} GROUP BY Blood_Group"
            cursor.execute(query)
            table_data = cursor.fetchall()

            # # Replace gender values with "Female" or "Male"
            # for row in table_data:
            #     if row['Gender'] == 'F':
            #         row['Gender'] = 'Female'
            #     elif row['Gender'] == 'M':
            #         row['Gender'] = 'Male'
            #
            # # Filter the data based on search parameters, if any
            # search_query = request.args.get('search')
            # if search_query:
            #     table_data = [row for row in table_data if search_query.lower() in row.values()]
            #
            # # Calculate total count of male, female, and transgender entries after filtering
            # total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
            # total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
            # total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
            #
            # # Total number of rows after filtering
            # total_rows = len(table_data)

            return render_template('bloodgroupreport.html', table_data=table_data, user_role=session.get('user_role'), table_name=table_name)
        except Exception as e:
            print("Error fetching data:", e)  # Print the specific error message
            return "An error occurred while fetching data: " + str(e)  # Return the specific error message
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')



@app.route('/display_index_education')
def display_index_education():
    try:
        # Get parameters from the URL
        username = request.args.get('username')
        database_name = request.args.get('database_name')
        table_name = request.args.get('table_name')

        # Only set session variables if they are provided in the URL (for superadmin)
        if username and database_name and table_name:
            session['username'] = username
            session['database_name'] = database_name
            session['table_name'] = table_name
        else:
            # Ensure session variables are already set for a regular user
            if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
                return redirect('/login')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table_name is not None or empty
        if not session['table_name']:
            return "No table name provided.", 400


        query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Education, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name}"
        cursor.execute(query)
        table_data = cursor.fetchall()

        # Replace gender values with "Female" or "Male"
        for row in table_data:
            if row['Gender'] == 'F':
                row['Gender'] = 'Female'
            elif row['Gender'] == 'M':
                row['Gender'] = 'Male'

        # Filter the data based on search parameters, if any
        search_query = request.args.get('search')
        if search_query:
            table_data = [row for row in table_data if search_query.lower() in row.values()]

        # Calculate total count of male, female, and transgender entries after filtering
        total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
        total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
        total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

        # Total number of rows after filtering
        total_rows = len(table_data)

        return render_template('educationreport.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])

    except Exception as e:
        print("Error fetching data:", e)
        return "An error occurred while fetching data: " + str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



@app.route('/display_index_qualification')
def display_index_qualification():
    try:
        # Get parameters from the URL
        username = request.args.get('username')
        database_name = request.args.get('database_name')
        table_name = request.args.get('table_name')

        # Only set session variables if they are provided in the URL (for superadmin)
        if username and database_name and table_name:
            session['username'] = username
            session['database_name'] = database_name
            session['table_name'] = table_name
        else:
            # Ensure session variables are already set for a regular user
            if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
                return redirect('/login')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table_name is not None or empty
        if not session['table_name']:
            return "No table name provided.", 400

        # Construct the query dynamically using session variables
        query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Qualification, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name}"
        cursor.execute(query)
        table_data = cursor.fetchall()

        # Replace gender values with "Female" or "Male"
        for row in table_data:
            if row['Gender'] == 'F':
                row['Gender'] = 'Female'
            elif row['Gender'] == 'M':
                row['Gender'] = 'Male'

        # Filter the data based on search parameters, if any
        search_query = request.args.get('search')
        if search_query:
            table_data = [row for row in table_data if search_query.lower() in row.values()]

        # Calculate total count of male, female, and transgender entries after filtering
        total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
        total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
        total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

        # Total number of rows after filtering
        total_rows = len(table_data)

        return render_template('qualification.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])

    except Exception as e:
        print("Error fetching data:", e)
        return "An error occurred while fetching data: " + str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



@app.route('/display_index_shifted')
def display_index_shifted():
    try:
        # Get parameters from the URL
        username = request.args.get('username')
        database_name = request.args.get('database_name')
        table_name = request.args.get('table_name')

        # Only set session variables if they are provided in the URL (for superadmin)
        if username and database_name and table_name:
            session['username'] = username
            session['database_name'] = database_name
            session['table_name'] = table_name
        else:
            # Ensure session variables are already set for a regular user
            if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
                return redirect('/login')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table_name is not None or empty
        if not session['table_name']:
            return "No table name provided.", 400

        query = f"SELECT Part_No, SrNo, Name, Epic_No, Age, Gender, Shifted, Gat, Gat_Name, Gan, Gan_Name FROM {session['database_name']}.{table_name} "
        cursor.execute(query)
        table_data = cursor.fetchall()

        # Replace gender values with "Female" or "Male"
        for row in table_data:
            if row['Gender'] == 'F':
                row['Gender'] = 'Female'
            elif row['Gender'] == 'M':
                row['Gender'] = 'Male'

        # Filter the data based on search parameters, if any
        search_query = request.args.get('search')
        if search_query:
            table_data = [row for row in table_data if search_query.lower() in row.values()]

        # Calculate total count of male, female, and transgender entries after filtering
        total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
        total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
        total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')

        # Total number of rows after filtering
        total_rows = len(table_data)

        return render_template('shiftedreport.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])

    except Exception as e:
        print("Error fetching data:", e)
        return "An error occurred while fetching data: " + str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# @app.route('/display_index_school')
# def display_index_school():
#     try:
#         # Get parameters from the URL
#         username = request.args.get('username')
#         database_name = request.args.get('database_name')
#         table_name = request.args.get('table_name')
#
#         # Only set session variables if they are provided in the URL (for superadmin)
#         if username and database_name and table_name:
#             session['username'] = username
#             session['database_name'] = database_name
#             session['table_name'] = table_name
#         else:
#             # Ensure session variables are already set for a regular user
#             if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
#                 return redirect('/login')
#
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Ensure table_name is not None or empty
#         if not session['table_name']:
#             return "No table name provided.", 400
#
#         query = f"SELECT 'School/College', COUNT(*) AS count FROM {session['database_name']}.{table_name} GROUP BY School/College"
#         cursor.execute(query)
#         table_data = cursor.fetchall()
#
#         # Replace gender values with "Female" or "Male"
#         for row in table_data:
#             if row['Gender'] == 'F':
#                 row['Gender'] = 'Female'
#             elif row['Gender'] == 'M':
#                 row['Gender'] = 'Male'
#
#         # Filter the data based on search parameters, if any
#         search_query = request.args.get('search')
#         if search_query:
#             table_data = [row for row in table_data if search_query.lower() in row.values()]
#
#         # Calculate total count of male, female, and transgender entries after filtering
#         total_male = sum(1 for row in table_data if row['Gender'] == 'Male')
#         total_female = sum(1 for row in table_data if row['Gender'] == 'Female')
#         total_transgender = sum(1 for row in table_data if row['Gender'] == 'Transgender')
#
#         # Total number of rows after filtering
#         total_rows = len(table_data)
#
#         return render_template('schoolwisereport.html', table_data=table_data, total_male=total_male, total_female=total_female, total_transgender=total_transgender, total_rows=total_rows, user_role=session.get('user_role'), table_name=session['table_name'])
#
#     except Exception as e:
#         print("Error fetching data:", e)
#         return "An error occurred while fetching data: " + str(e)
#
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()


@app.route('/display_index_school')
def display_index_school():
    try:
        # Get parameters from the URL
        username = request.args.get('username')
        database_name = request.args.get('database_name')
        table_name = request.args.get('table_name')

        # Only set session variables if they are provided in the URL (for superadmin)
        if username and database_name and table_name:
            session['username'] = username
            session['database_name'] = database_name
            session['table_name'] = table_name
        else:
            # Ensure session variables are already set for a regular user
            if not session.get('username') or not session.get('database_name') or not session.get('table_name'):
                return redirect('/login')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table_name is not None or empty
        if not session.get('table_name'):
            return "No table name provided.", 400

        # Fetch the table name from session
        table_name = session['table_name']

        # Ensure the table_name is not "none"
        if table_name.lower() == 'none':
            return "Invalid table name provided.", 400

        query = f"SELECT `School/College`, COUNT(*) AS count FROM `{session['database_name']}`.`{table_name}` GROUP BY `School/College`"
        cursor.execute(query)
        table_data = cursor.fetchall()

        # Filter the data based on search parameters, if any
        search_query = request.args.get('search')
        if search_query:
            table_data = [row for row in table_data if search_query.lower() in row.values()]

        return render_template(
            'schoolwisereport.html',
            table_data=table_data,
            user_role=session.get('user_role'),
            table_name=table_name
        )

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return f"An error occurred while fetching data: {err}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route('/update_record', methods=['POST'])
def update_record():
    if 'username' in session and 'selected_table' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Extract data from the request
            row_data = request.form.to_dict()

            # Check if the table is empty
            cursor.execute(f"SELECT COUNT(*) FROM `{session['database_name']}`.`{session['selected_table']}`")
            count = cursor.fetchone()[0]

            if count == 0:
                # If table is empty, directly perform an insert operation
                columns = ', '.join([f"`{column}`" for column in row_data.keys()])
                values = ', '.join([f"'{value}'" for value in row_data.values()])
                query = f"INSERT INTO `{session['database_name']}`.`{session['selected_table']}` ({columns}) VALUES ({values})"
                cursor.execute(query)
            else:
                # Check if the record already exists in the table based on a unique identifier
                unique_column = 'SrNo'  # Change this to the name of the unique identifier column in your table
                unique_value = row_data.get(unique_column)

                if unique_value:
                    # Check if the record already exists in the table
                    cursor.execute(
                        f"SELECT * FROM `{session['database_name']}`.`{session['selected_table']}` WHERE {unique_column} = '{unique_value}'")
                    existing_record = cursor.fetchone()

                    if existing_record:
                        # Construct the update query dynamically
                        set_clause = ', '.join([f"`{column}` = '{value}'" for column, value in row_data.items() if
                                                column != unique_column])
                        query = f"UPDATE `{session['database_name']}`.`{session['selected_table']}` SET {set_clause} WHERE {unique_column} = '{unique_value}'"
                        cursor.execute(query)
                    else:
                        # Construct the insert query dynamically
                        columns = ', '.join([f"`{column}`" for column in row_data.keys()])
                        values = ', '.join([f"'{value}'" for value in row_data.values()])
                        query = f"INSERT INTO `{session['database_name']}`.`{session['selected_table']}` ({columns}) VALUES ({values})"
                        cursor.execute(query)

            # Commit the changes
            conn.commit()

            # Redirect back to the display_index route after updating or inserting
            return redirect('/display_index')
        except mysql.connector.Error as e:
            print("MySQL Error:", e)
            return "An error occurred while updating or inserting record. Please try again."
        except Exception as e:
            print("Error updating or inserting record:", e)
            return "An unexpected error occurred. Please try again."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return "User not logged in."



@app.route('/row_details')
def view_row():
    if 'username' in session and 'database_name' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Get the table name from the request arguments or session
            table_name = request.args.get('table_name', session.get('table_name'))

            # Debugging: Print the table name to ensure it's being set correctly
            print(f"Table name: {table_name}")

            # Get the SrNo from the request arguments
            sr_no = request.args.get('sr_no')

            if not sr_no:
                return "No SrNo provided.", 400

            # Check if table_name is None or empty
            if not table_name:
                return "No table name provided.", 400

            # Properly format the database and table names to avoid SQL syntax errors
            database_name = session['database_name']
            formatted_table_name = f"`{database_name}`.`{table_name}`"

            # Debugging: Print the formatted table name
            print(f"Formatted table name: {formatted_table_name}")

            # Construct and execute the query to fetch row details
            query = f"SELECT * FROM {formatted_table_name} WHERE SrNo = %s"
            cursor.execute(query, (sr_no,))
            row_data = cursor.fetchone()

            if not row_data:
                return "No data found for the provided SrNo.", 404

            # Replace gender values with "Female" or "Male"
            if row_data['Gender'] == 'F':
                row_data['Gender'] = 'Female'
            elif row_data['Gender'] == 'M':
                row_data['Gender'] = 'Male'

            return render_template('form.html', row_data=row_data)
        except Exception as e:
            print("Error fetching row details:", e)
            return "An error occurred while fetching row details: " + str(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return redirect('/')





@app.route('/update_row', methods=['POST'])
def update_row():
    if 'username' in session and 'table_name' in session and 'database_name' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Extract data from the form
            updated_data = request.form.to_dict()

            if 'SrNo' not in updated_data:
                return "SrNo is required for updating the row."

            sr_no = updated_data.pop('SrNo')

            # Construct the update query dynamically with parameterized values
            set_clause = ', '.join([f"`{column}` = %s" for column in updated_data.keys()])
            query = f"UPDATE `{session['database_name']}`.`{session['table_name']}` SET {set_clause} WHERE `SrNo` = %s"
            values = list(updated_data.values())
            values.append(sr_no)

            cursor.execute(query, values)

            # Commit the changes
            conn.commit()

            # Fetch column names of the selected table
            cursor.execute(f"SHOW COLUMNS FROM `{session['database_name']}`.`{session['table_name']}`")
            columns = [column[0] for column in cursor.fetchall()]

            # Fetch the updated data
            cursor.execute(f"SELECT * FROM `{session['database_name']}`.`{session['table_name']}` WHERE `SrNo` = %s",
                           (sr_no,))
            updated_row = cursor.fetchone()

            # Convert the fetched row to a dictionary
            updated_data_dict = dict(zip(columns, updated_row))

            # Render the template and pass the column names and updated data to it
            return render_template('text.html', columns=columns, updated_data=updated_data_dict)
        except Exception as e:
            print("Error updating row:", e)
            return "An error occurred while updating row."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return "User not logged in."




# def generate_image(message):
#     image = Image.new('RGB', (400, 200), color='white')
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.truetype("arial.ttf", 20)
#     text_width, text_height = draw.textsize(message, font=font)
#     x = (image.width - text_width) / 2
#     y = (image.height - text_height) / 2
#     draw.text((x, y), message, fill='black', font=font)
#     image.save('message_image.png')
#
# @app.route('/generate_image_test')
# def generate_image_test():
#     message = "This is a test message"
#     generate_image(message)
#     return "Image generated successfully!"



if __name__ == '__main__':
    app.run(debug=True)
# if __name__ == '__main__':
#     app.run(debug=True,host='127.0.0.1',port='8000')