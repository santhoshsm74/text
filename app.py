from flask import Flask, render_template, redirect, flash, url_for, request
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",  # Replace with your MySQL username
    "password": "San_game7",  # Replace with your MySQL password
    "database": "user_db"  # Replace with your database name
}

@app.route('/')
def index():
    # Render the login form
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query to validate user credentials
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Login successful: redirect to detail page
            return redirect('/detail')
        else:
            # Invalid credentials: reload index.html with an error message
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for('index'))

    except mysql.connector.Error as err:
        # Handle database errors
        flash(f"Database error: {err}", "danger")
        return redirect(url_for('index'))

    finally:
        cursor.close()
        conn.close()

@app.route('/detail')
def detail():
    # Render the detail.html page from the templates folder
    return render_template('detail.html')

@app.route('/user_detail')
def user_detail():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True for key-value pairs

        # Fetch user data from the `user1` table (excluding password)
        query = "SELECT id, username, email, phone_number FROM user1"
        cursor.execute(query)
        users = cursor.fetchall()  # Fetch all rows as a list of dictionaries

        # Pass the data to the template
        return render_template('user_detail.html', users=users)

    except mysql.connector.Error as err:
        return f"Database error: {err}"

    finally:
        cursor.close()
        conn.close()

@app.route('/remove_user/<int:user_id>', methods=['POST'])
def remove_user(user_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Delete the user from the database by user_id
        query = "DELETE FROM user1 WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()

        flash("User successfully removed.", "success")
        return redirect(url_for('user_detail'))  # Redirect to the user details page after removal

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
        return redirect(url_for('user_detail'))

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
