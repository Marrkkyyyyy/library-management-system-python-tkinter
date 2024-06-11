import hashlib
import re
from tkinter import messagebox
import mysql.connector
from db_connection import connect_to_database
from show_books import show_admin


def hash_password(password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    # Validation function for first name and last name fields
def validate_name(text):
    # Regular expression to match only letters
    pattern = r"^[A-Za-z]*$"
    return re.match(pattern, text) is not None


def validate_middle_initial(text):
    # Regular expression to match a single letter or an empty string
    pattern = r"^[A-Za-z]?$"
    return re.match(pattern, text) is not None


def check_password_strength(password):
    # Regular expressions to check for different password strength criteria
    uppercase_regex = r"[A-Z]"
    lowercase_regex = r"[a-z]"
    digit_regex = r"\d"
    special_char_regex = r"[\W_]"
    
    # Check for at least one uppercase letter
    if not re.search(uppercase_regex, password):
        return False
    
    # Check for at least one lowercase letter
    if not re.search(lowercase_regex, password):
        return False
    
    # Check for at least one digit
    if not re.search(digit_regex, password):
        return False
    
    # Check for at least one special character
    if not re.search(special_char_regex, password):
        return False
    
    # Check for minimum length of 8 characters
    if len(password) < 8:
        return False
    
    return True

def validate_password_entry(password_entry):
    password = password_entry.get()
    if not check_password_strength(password):
        messagebox.showwarning("Password Alert", "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        return False

    # Return True to allow the entry widget to accept the input
    return True


def register_admin(firstName_entry,lastName_entry,middleInitial_entry,username_entry,password_entry, user_type_entry, treeAdmin):
        # Retrieve user input from the entry fields
        first_name = firstName_entry.get().strip()
        last_name = lastName_entry.get().strip()
        middle_initial = middleInitial_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        user_type = user_type_entry.get().strip()
        
        if not first_name or not last_name or not username or not password:
            messagebox.showwarning("Incomplete Form", "Please fill in all the required fields.")
            return

        # Validate form fields
        if not validate_name(first_name):
            messagebox.showwarning("Invalid Input", "Please enter a valid first name.")
            return
        if not validate_name(last_name):
            messagebox.showwarning("Invalid Input", "Please enter a valid last name.")
            return
        if middle_initial and not validate_middle_initial(middle_initial):
            messagebox.showwarning("Invalid Input", "Please enter a valid middle initial.")
            
        if not check_password_strength(password):
            messagebox.showwarning("Password Alert", "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
            return

        # Connect to the database
        conn = connect_to_database()
        if conn is None:
            # Handle connection error
            messagebox.showerror("Database Error", "Error connecting to the database. Please try again later.")
            return

        try:
            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Check if email already exists
            query = "SELECT * FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showwarning("Registration Error", "Username already exists. Please choose a different username.")
                return
            
            query = "SELECT * FROM admin WHERE username = %s"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showwarning("Registration Error", "Username already exists. Please choose a different username.")
                return

            # Hash the password
            hashed_password = hash_password(password)

            # Prepare the INSERT statement
            sql = "INSERT INTO admin (first_name, last_name, middle_initial, username, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name, last_name, middle_initial, username, hashed_password, user_type)

            # Execute the INSERT statement
            cursor.execute(sql, values)

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and database connection
            cursor.close()
            conn.close()

            # Show a success message
            messagebox.showinfo("Registration Successful", "User registered successfully.")
            show_admin(treeAdmin)
        except mysql.connector.Error as error:
            # Handle database error
            messagebox.showerror("Database Error", f"Error inserting user data into the database: {error}")

            # Roll back any changes in case of an error
            conn.rollback()

            # Close the cursor and database connection
            cursor.close()
            conn.close()
            
            
def delete_admin(treeview):
    selected_item = treeview.focus()
    if selected_item:
        username = treeview.item(selected_item, "values")[1]
        
        # Display confirmation dialog
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete this account?")
        if not confirmed:
            return

        conn = connect_to_database()
        if conn is None:
            messagebox.showerror("Error", "Failed to connect to the database")
            return
        
        cursor = conn.cursor()

        # Delete the book
        query = "DELETE FROM admin WHERE username = %s"
        values = (username,)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Account deleted successfully")
            show_admin(treeview)
        except mysql.connector.Error as error:
            print("Error deleting account:", error)
            messagebox.showerror("Error", "Failed to delete the account")


    else:
        messagebox.showerror("Error", "No account selected")