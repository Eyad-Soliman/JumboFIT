from flask import Flask,jsonify,render_template, request, url_for, flash, redirect, session
import mysql.connector
import bcrypt
import os
from openai import OpenAI

app=Flask(__name__, template_folder="templates")
app.secret_key = "secretkey123"
con=mysql.connector.connect(
    host='localhost',
    username='root',
    password='Dracut_10315',
    database='jumbo_fit'
)

cursor=con.cursor()

@app.route('/')
def login_page():
    return render_template('/pages/sign_in.html')

@app.route('/login', methods=['POST'])
def login():
    """ Authenticates a user with hashed password verification """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Fetch user details 
    cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Verify hashed password
        session['user_id'] = user[0]  # Store user ID in session
        return jsonify({"success": True, "message": "Login successful!", "redirect": "/home"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password!"})

# ----------------------
# HOME PAGE (AFTER LOGIN/ AFTER LOGOUT)
# ----------------------
@app.route('/home')
def home():
    """ Renders the home page after successful login """
    if 'user_id' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not authenticated
    
    user_id = session['user_id']
    try:
        with con.cursor() as cursor:  # Using a new cursor for this query
            cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

        if user:
            name, email = user  # Unpack tuple values
        else:
            name, email = "Guest", "Not available"  # Fallback if user not found

        return render_template('index.html', name=name, email=email)
    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Ensure the users table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('user', 'admin') DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
con.commit()

# ----------------------
# USER REGISTRATION PAGE
# ----------------------

@app.route('/register', methods=['GET'])
def get_register_page():
    return render_template('/pages/register.html')

@app.route('/register', methods=['POST'])
def register():
    """ Registers a new user """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"success": False, "message": "Email already registered. Try logging in."})

    # Insert new user into database
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                   (name, email, hashed_password.decode('utf-8')))
    con.commit()

    return jsonify({"success": True, "message": "Registration successful! You can now log in."})


@app.route('/toggle-checkin', methods=['POST'])
def toggle_checkin():
    """ Toggles the user's check-in status """
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_id = session['user_id']

    try:
        with con.cursor() as cursor:
            # Get current checked_in status
            cursor.execute("SELECT checked_in FROM users WHERE id = %s", (user_id,))
            current_status = cursor.fetchone()

            if current_status is None:
                return jsonify({"success": False, "message": "User not found"}), 404

            new_status = not current_status[0]  # Toggle between True/False

            # Update user's checked_in status
            cursor.execute("UPDATE users SET checked_in = %s WHERE id = %s", (new_status, user_id))
            con.commit()

            return jsonify({"success": True, "checked_in": new_status, "message": "Status updated successfully!"})

    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# ----------------------
# USER LOGOUT
# ----------------------
@app.route('/logout')
def logout():
    """ Logs out a user """
    session.pop('user_id', None)
    return redirect(url_for('index'))

# ----------------------
# GET USER PROFILE
# ----------------------
@app.route('/account', methods=['GET'])
def get_profile():
    """ Retrieves user details if logged in """
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in."})

    user_id = session['user_id']
    cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "success": True,
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[3],
                "created_at": user[4].strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    else:
        return jsonify({"success": False, "message": "User not found."})
    
# # ----------------------
# # GET GYM BUDDIES
# # ----------------------
# @app.route('/gymbuddies', methods=['GET'])
# def get_buddies():
#     """ Retrieves buddies if logged in """
#     if 'user_id' not in session:
#         return jsonify({"success": False, "message": "User not logged in."})

#     user_id = session['user_id']
#     cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()

#     if user:
#         return jsonify({
#             "success": True,
#             "user": {
#                 "id": user[0],
#                 "name": user[1],
#                 "email": user[2],
#                 "role": user[3],
#                 "created_at": user[4].strftime('%Y-%m-%d %H:%M:%S')
#             }
#         })
#     else:
#         return jsonify({"success": False, "message": "User not found."})
    
# # ----------------------
# # GET GYM BUDDIES
# # ----------------------
# @app.route('/workout-preferences', methods=['GET'])
# def get_profile():
#     """ Retrieves user details if logged in """
#     if 'user_id' not in session:
#         return jsonify({"success": False, "message": "User not logged in."})

#     user_id = session['user_id']
#     cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()

#     if user:
#         return jsonify({
#             "success": True,
#             "user": {
#                 "id": user[0],
#                 "name": user[1],
#                 "email": user[2],
#                 "role": user[3],
#                 "created_at": user[4].strftime('%Y-%m-%d %H:%M:%S')
#             }
#         })
#     else:
#         return jsonify({"success": False, "message": "User not found."})

# ----------------------
# UPDATE USER PROFILE
# ----------------------
@app.route('/update-profile', methods=['POST'])
def update_profile():
    """ Updates user information """
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in."})

    user_id = session['user_id']
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Update user information
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    con.commit()

    return jsonify({"success": True, "message": "Profile updated successfully."})


# GPT Integration
@app.route('/generate-workout', methods=['POST'])
def generate_workout():
    """Handles the request from frontend to generate a workout plan."""
    data = request.get_json()
    user_message = data.get('question')

    client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key ="f496a4f4bdbf4e72b9707e8c28226ec2"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates workout plans based on user input."},
            {"role": "user", "content": user_message}
        ],
    )

    assistant_message = response.choices[0].message.content
    return jsonify({"response": assistant_message})

# ----------------------
# RUN FLASK APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)