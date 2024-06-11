from admin_sign_up import *
from tkinter import *
from tkinter import font
from tkinter.ttk import Combobox, Style, Treeview
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from accounts import accounts_clicked
from borrowed_books import borrowed_books_clicked
from db_connection import connect_to_database
from reports import reports_clicked
from returned_books import returned_books_clicked
from show_books import filter_books, search_book, show_all_books, show_currently_borrowed, show_history_borrowed

    
def register_student(root):
    root.destroy()
    registration_root = Tk()
    registration_root.title("SEAIT Library Management System")

    screen_width = registration_root.winfo_screenwidth()
    screen_height = registration_root.winfo_screenheight()
    x = (screen_width // 2) - (480 // 2)
    y = (screen_height // 2) - (350 // 2)
    registration_root.geometry(f"{480}x{350}+{x}+{y}")

    registration_root.resizable(False,False)
    system_icon =PhotoImage(file = "seait.png")
    registration_root.iconphoto(True, system_icon)
    
    container = Frame(registration_root)
    container.pack(anchor='center',pady=(10,0))
    
    sign_up = Label(container,text="Sign Up",font=("Arial Black",28))
    sign_up.grid(row=0, columnspan=2,pady=(0,5),padx=(50,0))
    
    

    def register():
        # Retrieve user input from the entry fields
        school_id = schoolID_entry.get()
        first_name = firstName_entry.get()
        last_name = lastName_entry.get()
        middle_initial = middleInitial_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not school_id or not first_name or not last_name or not username or not password:
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

            # Check if user_school_id already exists
            query = "SELECT * FROM user WHERE user_school_id = %s"
            cursor.execute(query, (school_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showwarning("Registration Error", "A user with the same school ID already exists.")
                return

            # Check if username already exists
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
            sql = "INSERT INTO user (user_school_id, first_name, last_name, middle_initial, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (school_id, first_name, last_name, middle_initial, username, hashed_password)

            # Execute the INSERT statement
            cursor.execute(sql, values)

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and database connection
            cursor.close()
            conn.close()

            # Show a success message
            messagebox.showinfo("Registration Successful", "User registered successfully.")
            back_login(registration_root)

        except mysql.connector.Error as error:
            # Handle database error
            messagebox.showerror("Database Error", f"Error inserting user data into the database: {error}")

            # Roll back any changes in case of an error
            conn.rollback()

            # Close the cursor and database connection
            cursor.close()
            conn.close()



    # Register validation functions
    validate_name_cmd = (container.register(validate_name), "%P")
    validate_middle_initial_cmd = (container.register(validate_middle_initial), "%P")
    validate_password_entry_cmd = (container.register(validate_password_entry),)

    # Create and grid the labels and entry fields
    firstName_label = Label(container, text="First Name:", font=("Calibri", 12, "bold"))
    firstName_label.grid(row=1, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    firstName_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_name_cmd)
    firstName_entry.grid(row=1, column=1, ipady=2, pady=(0, 10))

    lastName_label = Label(container, text="Last Name:", font=("Calibri", 12, "bold"))
    lastName_label.grid(row=2, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    lastName_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_name_cmd)
    lastName_entry.grid(row=2, column=1, pady=(0, 10))

    middleInitial_label = Label(container, text="Middle Initial:", font=("Calibri", 12, "bold"))
    middleInitial_label.grid(row=3, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    middleInitial_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_middle_initial_cmd)
    middleInitial_entry.grid(row=3, column=1, pady=(0, 10))

    schoolID_label = Label(container, text="School ID:", font=("Calibri", 12, "bold"))
    schoolID_label.grid(row=4, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    schoolID_entry = Entry(container, font=("Calibri", 12), width=30)
    schoolID_entry.grid(row=4, column=1, pady=(0, 10))

    username_label = Label(container, text="Username:", font=("Calibri", 12, "bold"))
    username_label.grid(row=5, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    username_entry = Entry(container, font=("Calibri", 12), width=30)
    username_entry.grid(row=5, column=1, pady=(0, 10))

    password_label = Label(container, text="Password:", font=("Calibri", 12, "bold"))
    password_label.grid(row=6, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    password_entry = Entry(container, font=("Calibri", 12), width=30, show="*",  validatecommand=validate_password_entry_cmd)
    password_entry.grid(row=6, column=1, pady=(0, 10))
    
    button_frame = Frame(container)
    button_frame.grid(row=7,column=1)
    
    login_button = Button(button_frame, font=("Calibri", 12,), width = 12, text="Login", command=lambda:back_login(registration_root))
    login_button.grid(row=0, column=0,ipady=1,padx=(0,20))
    
    register_button = Button(button_frame, font=("Calibri", 12, ),width = 12, text="Register", command=register)
    register_button.grid(row=0, column=1,ipady=1)
    root.mainloop()
def _insert_book(accession_number_entry, author_entry, title_entry, category_entry, topLevel, treeview):
    accession_number = accession_number_entry.get().strip()
    author = author_entry.get().strip()
    title = title_entry.get().strip()
    category = category_entry.get().strip()

    if not accession_number or not author or not title or not category:
        messagebox.showerror("Error", "Please fill in all the fields", parent=topLevel)
        return
    conn = connect_to_database()
    if conn is None:
        # Handle the case when the connection is not successful
        messagebox.showerror("Error", "Failed to connect to the database", parent=topLevel)
        return

    cursor = conn.cursor()
    
    
    query = "SELECT * FROM category WHERE category_name = %s"
    values = (category,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        categoryID = result[0]
    else:
        messagebox.showerror("Error", "Category not found in the database")
        cursor.close()
        conn.close()
        return
    
    # Check if the accession_no already exists
    query = "SELECT COUNT(*) FROM books WHERE accession_no = %s"
    cursor.execute(query, (accession_number,))
    result = cursor.fetchone()
    if result[0] > 0:
        messagebox.showerror("Error", "Book with the given accession number already exists", parent=topLevel)
        cursor.close()
        conn.close()
        return

    # Insert the book
    query = "INSERT INTO books (accession_no, categoryID, author, title) VALUES (%s, %s, %s, %s)"
    values = (accession_number, categoryID, author, title)

    try:
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Book inserted successfully", parent=topLevel)
        show_all_books(treeview)
        accession_number_entry.delete(0, 'end')
        author_entry.delete(0, 'end')
        title_entry.delete(0, 'end')
    except mysql.connector.Error as error:
        print("Error inserting book:", error)
        messagebox.showerror("Error", "Failed to insert the book", parent=topLevel)

    cursor.close()
    conn.close()

def _update_book(accession_number_entry, author_entry, title_entry, category_entry,bookID, root, treeview, topLevel):
    accession_number = accession_number_entry.get().strip()
    category = category_entry.get().strip()
    author = author_entry.get().strip()
    title = title_entry.get().strip()

    if not accession_number or not author or not title:
        messagebox.showerror("Error", "Please fill in all the fields", parent=root)
        return
    
    conn = connect_to_database()
    if conn is None:
        messagebox.showerror("Error", "Failed to connect to the database")
        return

    cursor = conn.cursor()
    
    query = "SELECT * FROM category WHERE category_name = %s"
    values = (category,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        categoryID = result[0]
    else:
        messagebox.showerror("Error", "Category not found in the database")
        cursor.close()
        conn.close()
        return

    # Check if the updated accession number is a duplicate except for the value itself
    query = "SELECT COUNT(*) FROM books WHERE accession_no = %s AND bookID != %s"
    values = (accession_number, bookID)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] > 0:
        messagebox.showerror("Error", "Duplicate accession number found", parent=root)
        cursor.close()
        conn.close()
        return

    # Update the book
    query = "UPDATE books SET author = %s, title = %s, accession_no = %s, categoryID = %s WHERE bookID = %s"
    values = (author, title, accession_number, categoryID,bookID)

    try:
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully", master=root)
        show_all_books(treeview)
        topLevel.destroy()
    except mysql.connector.Error as error:
        print("Error updating book:", error)
        messagebox.showerror("Error", "Failed to update the book")

    cursor.close()
    conn.close()

def _delete_book(treeview):
    selected_item = treeview.focus()
    if selected_item:
        accession_number = treeview.item(selected_item, "values")[0]
        author = treeview.item(selected_item, "values")[2]
        title = treeview.item(selected_item, "values")[3]
        
        # Display confirmation dialog
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete this book?")
        if not confirmed:
            return

        conn = connect_to_database()
        if conn is None:
            messagebox.showerror("Error", "Failed to connect to the database")
            return
        
        cursor = conn.cursor()
        query = "SELECT bookID FROM books WHERE accession_no = %s AND author = %s AND title = %s"
        values = (accession_number, author, title)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            bookID = result[0]
        else:
            messagebox.showerror("Error", "Book not found in the database")
            cursor.close()
            conn.close()
            return

        # Delete the book
        query = "DELETE FROM books WHERE bookID = %s"
        values = (bookID,)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully")
            show_all_books(treeview)
        except mysql.connector.Error as error:
            print("Error deleting book:", error)
            messagebox.showerror("Error", "Failed to delete the book")


    else:
        messagebox.showerror("Error", "No book selected")
        
def populate_category_combobox(category_combobox):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM category ORDER BY category_name")
            categories = [category[0] for category in cursor.fetchall()] 
            conn.close()
            categories.insert(0, "All Category")
            category_combobox["values"] = categories
            category_combobox.current(0)
            
def _insert_category(category_entry, root, treeview,category_combobox):   
    category = category_entry.get().strip()

    if not category:
        messagebox.showerror("Error", "Please fill in the field")
        return
    conn = connect_to_database()
    if conn is None:
        messagebox.showerror("Error", "Failed to connect to the database")
        return

    cursor = conn.cursor()
    
    query = "SELECT * FROM category WHERE category_name = %s"
    cursor.execute(query, (category,))
    result = cursor.fetchone()
    if result is not None and result[0] > 0:
        messagebox.showerror("Error", "Category name already exists", master=root)
        root.grab_set()
        cursor.close()
        conn.close()
        return

    # Insert the category
    query = "INSERT INTO category (category_name) VALUES (%s)"
    values = (category,)

    try:
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Category inserted successfully", master=root)
        root.grab_set()
        category_entry.delete(0, 'end')
        show_all_category(treeview)
        populate_category_combobox(category_combobox)
    except mysql.connector.Error as error:
        print("Error inserting category:", error)
        messagebox.showerror("Error", "Failed to insert the category")

    cursor.close()
    conn.close()
    
    

    
    
    
def validate_login(root, username, password):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        # Check if the username exists in the database
        query = "SELECT password, user_type FROM admin WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            stored_password = user[0] 
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_type = user[1]

            if stored_password == hashed_password:
                conn.close()
                root.destroy()
                admin_dashboard(user_type)
            else:
                conn.close()
                messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            query = "SELECT password, userID FROM user WHERE username = %s"
            values = (username,)
            cursor.execute(query, values)
            user = cursor.fetchone()
            
            if user:
                stored_password = user[0] 
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                userID = user[1]
                
                if stored_password == hashed_password:
                    conn.close()
                    root.destroy()
                    student_dashboard(userID)
                else:
                    conn.close()
                    messagebox.showerror("Login Failed", "Invalid username or password")
            else:
                conn.close()
                messagebox.showerror("Login Failed", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Failed to connect to the database")
        
        
def submit_login(root, username_entry, password_entry):
    validate_login(root, username_entry.get(), password_entry.get())


# change root
def change_root(root):
    root.destroy()
    show_startup_books()

def back_login(root):
    root.destroy()
    call()

# call
def call():
    root = Tk()
    start_root(root)
    root.mainloop()

def start_root(root):
    root.title("SEAIT Library Management System")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (480 // 2)
    y = (screen_height // 2) - (250 // 2)
    root.geometry(f"{480}x{250}+{x}+{y}")

    root.resizable(False,False)
    system_icon =PhotoImage(file = "seait.png")
    root.iconphoto(True, system_icon)

    frame = Frame(root, width=390, height=230)
    frame.grid(row=0, column=0, padx=(40,0), pady=(30,0))
    heading = Label(frame,text="SEAIT Library Management System",font=('Arial', 18, 'bold'))
    heading.grid(row=0, column=0, columnspan=5, pady=(0, 10))

    username_label = Label(frame, text='Username: ', font= ('Arial', 14))
    username_label.grid(row=1, column=0, padx=(10,0), pady=10, sticky=W)

    username_entry = Entry(frame, width=23, border=1, fg='black', bg='white', font=('Arial', 14))
    username_entry.grid(row=1, column=1, pady=10)

    password_label = Label(frame, text='Password: ', font= ('Arial', 14))
    password_label.grid(row=2, column=0, padx=(10,0), pady=10, sticky=W)

    password_entry = Entry(frame, width=23, border=1, font=('Arial', 14),  show="*")
    password_entry.grid(row=2, column=1, pady=10)

    show_books = Button(frame, text='Show Books', width=12, font=('Arial', 12),command=lambda : change_root(root))
    show_books.grid(row=3, column=0,pady=(2,0))
    
    portal_frame = Frame(frame)
    portal_frame.grid(row=3, column=1,pady=(2,0),sticky=E)
    
    register_button = Button(portal_frame, text='Register', width=12, font=('Arial', 12),command=lambda:register_student(root))
    register_button.pack(side=LEFT, padx=(0,10))

    login_button = Button(portal_frame, text='Login', width=12, font=('Arial', 12), command=lambda: validate_login(root, username_entry.get(), password_entry.get()))
    login_button.pack(side=LEFT, padx=(0,5))
    


def show_startup_books():
    root = Tk()
    root.title("List of Books")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 950
    height = 640
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (720 // 2)
    
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.resizable(False,False)
    
    options_frame = Frame(root)
    options_frame.pack(anchor="w")
    back_button = Button(options_frame, text="Login", font=('Bold', 12), fg="#158aff", bd=0, width=12,bg="white",command=lambda : back_login(root))
    back_button.pack(side=LEFT,anchor='n', ipady=5, pady=(10,0),padx=(8,0))
    
    search_frame = Frame(options_frame)
    search_frame.pack(side=LEFT, pady=(15,0))
    
    search_label = Label(search_frame, text="Search: ",font=("Calibri", 14))
    search_label.grid(row = 0, column = 0,padx=(10,0))
    
    class PlaceholderEntry(Entry):
        def __init__(self, container, placeholder, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            self.placeholder = placeholder
            self.insert("0", self.placeholder)
            self.bind("<FocusIn>", self._clear_placeholder)
            self.bind("<FocusOut>", self._add_placeholder)
            self.configure(foreground="gray")

        def _clear_placeholder(self, event):
            if self.get() == self.placeholder:
                self.delete("0", "end")

        def _add_placeholder(self, event):
            if self.get() == "":
                self.insert("0", self.placeholder)
                
    
                    

    search_entry = PlaceholderEntry(search_frame, "Filter title, author...",font=("Calibri", 14),width=32)
    search_entry.grid(row=0, column=1, ipady=2,padx=(0,5))
    
    search_button = Button(search_frame, text="Search",font=("Bold", 10),command=lambda:search_book(search_entry, root, tree))
    search_button.grid(row=0, column=2,ipadx=15,ipady=1,padx=(0,10))
    
    category_combobox = Combobox(search_frame, state="readonly",width=25,font=("",12))
    category_combobox.grid(row=0, column=3,ipady=2)

    hidden_label = Label(search_frame, width=0, height=0,font=("",2))
    hidden_label.grid(row=1, column=3)
    hidden_label.focus_set() 

    def populate_category_combobox():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM category ORDER BY category_name")
            categories = [category[0] for category in cursor.fetchall()] 
            conn.close()
            categories.insert(0, "All Category")
            category_combobox["values"] = categories
            category_combobox.current(0)

    def clear_combobox_selection(event):
        hidden_label.focus_set()  
        category_combobox.selection_clear() 

    category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
    populate_category_combobox()
    
    
    filter_button = Button(search_frame, text="Filter", font=("Bold", 10), command=lambda:filter_books(tree,category_combobox))
    filter_button.grid(row=0, column=4,ipadx=15,padx=(5,0),ipady=1)
    
    list_of_books_frame = Frame(root)
    list_of_books_frame.pack(fill='x', expand=True)
    
    tree = Treeview(list_of_books_frame, height=28)

    # Insert columns
    tree["columns"] = ("Accession", "Category","Author", "Title", "Status")
    
    tree.heading("#0", text="ID")
    tree.heading("Accession", text="Accession",anchor='w')
    tree.heading("Category", text="Category",anchor='w')
    tree.heading("Author", text="Author",anchor='w')
    tree.heading("Title", text="Title",anchor='w')
    tree.heading("Status", text="Status",anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="orange", foreground="white",font=("TkDefaultFont", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("#0", width=5)  # ID column
    tree.column("Accession", width=60)
    tree.column("Category", width=80)
    tree.column("Author", width=120)
    tree.column("Title", width=250)
    tree.column("Status", width=40)
    
    show_all_books(tree)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))
    
    
    root.mainloop()

    
def admin_dashboard(user_type):
    
    root = Tk()
    root.title("SEAIT Library Management System")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 1050
    height = 670
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (750 // 2)
    system_icon =PhotoImage(file = "seait.png")
    root.iconphoto(True, system_icon)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.resizable(False,False)
    icon_width = 40
    icon_height = 40
    add_book_icon = Image.open("add_book.png")
    delete_book_icon = Image.open("delete_book.png")
    update_book_icon = Image.open("update_book.png")
    add_book = ImageTk.PhotoImage(add_book_icon.resize((icon_width, icon_height), Image.ANTIALIAS))
    delete_book = ImageTk.PhotoImage(delete_book_icon.resize((icon_width, icon_height), Image.ANTIALIAS))
    update_book = ImageTk.PhotoImage(update_book_icon.resize((icon_width, icon_height), Image.ANTIALIAS))

    def list_of_books_clicked():
        clear_bottom_frame()
        list_of_books_frame()
        # Add the necessary widgets and functionality for the "List of Books" section
        # ...

    def clear_bottom_frame():
        # Clear existing content in the bottom_frame
        for widget in bottom_frame.winfo_children():
            widget.destroy()
    
    top_frame = Frame(root)
    top_frame.pack(anchor="nw")
    
    options_frame = Frame(top_frame, bg="#c3c3c3")
    options_frame.pack(ipadx=485,side=LEFT)
    options_frame.pack_propagate(False)
    options_frame.configure(height=45)
    
    exit_frame = Frame(top_frame, bg="#c3c3c3")
    exit_frame.pack(ipadx=35, padx=(8,0), side=RIGHT)
    exit_frame.pack_propagate(False)
    exit_frame.configure(height=45)
    
    button_font = font.Font(family="Calibri", size=12, weight="bold")
    list_of_books = Button(options_frame, text="List of Books", font=button_font, fg="#158aff", bd=0,bg="white",width=15)
    list_of_books.pack(side=LEFT,padx=(10,0))
    
    borrowed_books = Button(options_frame, text="Borrowed Books", font=button_font, fg="#158aff", bd=0, bg="white",width=15)
    borrowed_books.pack(side=LEFT,padx=(10,0))
    
    returned_books = Button(options_frame, text="Returned Books", font=button_font, fg="#158aff", bd=0, bg="white",width=15)
    returned_books.pack(side=LEFT,padx=(10,0))
    
    reports = Button(options_frame, text="Reports", font=button_font, fg="#158aff", bd=0, bg="white",width=15)
    if user_type == 'Staff':
        reports.pack_forget()
    else:
        reports.pack(side=LEFT, padx=(10, 0))
    
    accounts = Button(options_frame, text="Accounts", font=button_font, fg="#158aff", bd=0, bg="white",width=12, command=lambda:accounts_clicked(bottom_frame))
    if user_type == 'Staff':
        accounts.pack_forget()
    else:
        accounts.pack(side=LEFT, padx=(10, 0))
    
    
    list_of_books.configure(command=lambda:list_of_books_clicked())
    borrowed_books.configure(command=lambda:borrowed_books_clicked(bottom_frame))
    returned_books.configure(command=lambda:returned_books_clicked(bottom_frame))
    reports.configure(command=lambda:reports_clicked(bottom_frame))
    
    logout_button = Button(options_frame, text="Logout", font=button_font, fg="#e02e2e", bd=0, bg="white",width=8,command=lambda:back_login(root))
    logout_button.pack(side=RIGHT,padx=(0,5))
    
    exit_button = Button(exit_frame, text="Exit", font=button_font, fg="#e02e2e", bd=0, bg="white", command=lambda:root.destroy())
    exit_button.pack(side=LEFT,padx=5,ipadx=15)
    
    bottom_frame = Frame(root)
    bottom_frame.pack(fill='x')
    
    def list_of_books_frame():
        list_of_books_frame = Frame(bottom_frame)
        list_of_books_frame.pack(anchor="w",pady=(10,0))
        
        search_frame = Frame(list_of_books_frame)
        search_frame.pack(side=LEFT,anchor='n',padx=(10,0))
        
        search_label = Label(search_frame, text="Search:", font=('Bold', 12))
        search_label.grid(row=0, column=0, padx=(0,5))

        class PlaceholderEntry(Entry):
            def __init__(self, container, placeholder, *args, **kwargs):
                super().__init__(container, *args, **kwargs)
                self.placeholder = placeholder
                self.insert("0", self.placeholder)
                self.bind("<FocusIn>", self._clear_placeholder)
                self.bind("<FocusOut>", self._add_placeholder)
                self.configure(foreground="gray")

            def _clear_placeholder(self, event):
                if self.get() == self.placeholder:
                    self.delete("0", "end")

            def _add_placeholder(self, event):
                if self.get() == "":
                    self.insert("0", self.placeholder)




        search_entry = PlaceholderEntry(search_frame, "Filter title, author...", font=("Arial", 12), width=41)
        search_entry.grid(row=0, column=1, padx=(5, 0), ipady=2, sticky="w")


        search_button = Button(search_frame, text="Search", command=lambda:search_book(search_entry, root, tree))
        search_button.grid(row=0, column=2, ipadx=20, ipady=1, padx=(5, 0))

        
        
        
        filter_frame = Frame(list_of_books_frame)
        filter_frame.pack(side=LEFT, anchor='n')  
        
        category_combobox = Combobox(filter_frame, state="readonly",width=24,font=("",10))
        category_combobox.grid(row=0, column=0, ipady=4, padx=(10,0))

        hidden_label = Label(filter_frame, width=0, height=0,font=("",14))
        hidden_label.grid(row=1, column=0)
        hidden_label.focus_set() 

        def populate_category_combobox():
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT category_name FROM category ORDER BY category_name")
                categories = [category[0] for category in cursor.fetchall()] 
                conn.close()
                categories.insert(0, "All Category")
                category_combobox["values"] = categories
                category_combobox.current(0)

        def clear_combobox_selection(event):
            hidden_label.focus_set()  
            category_combobox.selection_clear() 

        category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
        populate_category_combobox()
        
        
        filter_button = Button(filter_frame, text="Filter", font=("Bold", 10),command=lambda:filter_books(tree, category_combobox))
        filter_button.grid(row=0, column=1,ipadx=20,padx=(5,0))
        
        add_category_button = Button(filter_frame, text="Add Category",width=19, font=("", 11), command=lambda:add_category(root,category_combobox))
        add_category_button.grid(row=1, columnspan=1, ipadx=4, padx=(9,0),pady=(5,0), ipady=2)
        books_function = Frame(list_of_books_frame, bg="skyblue")
        books_function.pack(side=LEFT,ipadx=5, ipady=5,padx=(5,0))
        
        add_book_button = Button(books_function,image=add_book,command=lambda : add_book_window(root, tree))
        add_book_button.pack(ipadx=5,ipady=5,side=LEFT, padx=(10,0))
        update_book_button = Button(books_function, image=update_book, command=lambda: update_book_window(root, tree))
        update_book_button.pack(ipadx=5,ipady=5,side=LEFT, padx=(10,0))
        delete_book_button = Button(books_function,image=delete_book, command=lambda: _delete_book(tree) )
        delete_book_button.pack(ipadx=5,ipady=5,side=LEFT, padx=(10,0))
        
        list_of_books = Frame(bottom_frame)
        list_of_books.pack(fill='x')
        
        # Create the Treeview widget
        tree = Treeview(list_of_books,height=26)

        # Insert columns
        tree["columns"] = ("Accession", "Category","Author", "Title", "Status")
        
        tree.heading("#0", text="#")
        tree.heading("Accession", text="Accession",anchor='w')
        tree.heading("Category", text="Category",anchor='w')
        tree.heading("Author", text="Author",anchor='w')
        tree.heading("Title", text="Title",anchor='w')
        tree.heading("Status", text="Status",anchor='w')
        s = Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background="orange", foreground="white",font=("TkDefaultFont", 12, "bold"), bordercolor="white", borderwidth=2)
        s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
        # Set column widths based on content
        tree.column("#0", width=5,)  # ID column
        tree.column("Accession", width=60)
        tree.column("Category", width=80)
        tree.column("Author", width=120)
        tree.column("Title", width=250)
        tree.column("Status", width=40)
        
        
        show_all_books(tree)

        # Pack the Treeview widget
        tree.pack(fill='both', expand=True, pady=(8, 0))
    list_of_books_frame()
    root.mainloop()
    


def show_all_category(treeview):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category_name FROM category ORDER BY category_name")
        categories = cursor.fetchall()
        conn.close()

        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert data rows
        for category in categories:
            treeview.insert("", "end", values=category)
                
                
def validate_numbers(action, value_if_allowed):
    # Only allow digits and empty string
    if action == '1':  # '1' means inserting text
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False
    return True
    
def add_book_window(root, treeview):
    add_book = Toplevel(root)
    add_book.grab_set()
    add_book.title("Add Book")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 650
    height = 290
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    add_book.geometry(f"{width}x{height}+{x}+{y}")

    add_book.resizable(False,False)
    validate_func = add_book.register(validate_numbers)
    

    
    container_frame = Frame(add_book)
    container_frame.pack(pady=(20,0),padx=(0,20))
    
    title_label = Label(container_frame, text="Title: ",font=("Bold",16))
    title_label.grid(row=0,column=0,sticky='e',pady=(15,0))
    
    title_entry = Entry(container_frame,font=("", 14),)
    title_entry.grid(row=0,column=1,ipadx=100,ipady=5,pady=(15,0))
    
    author_label = Label(container_frame, text="Author: ",font=("Bold",16))
    author_label.grid(row=1,column=0,sticky='e',pady=(15,0))
    
    author_entry = Entry(container_frame,font=("", 14),)
    author_entry.grid(row=1,column=1,ipadx=100,ipady=5,pady=(15,0))
    
    accession_number_label = Label(container_frame, text="Accession #: ",font=("Bold",15))
    accession_number_label.grid(row=2,column=0,sticky='e',pady=(15,0))
    
    accession_number_entry = Entry(container_frame,font=("", 14),validate="key", validatecommand=(validate_func, '%d', '%P'))
    accession_number_entry.grid(row=2,column=1,ipadx=100,ipady=5,pady=(15,0))
    
    category_label = Label(container_frame, text="Category: ",font=("Bold",15))
    category_label.grid(row=3,column=0,sticky='e',pady=(15,0))
    
    category_combobox = Combobox(container_frame, state="readonly",width=27,font=("",12))
    category_combobox.grid(row=3, column=1, ipady=5, sticky='w',pady=(15,0))

    hidden_label = Label(container_frame, width=0, height=0,font=("",14))
    hidden_label.grid(row=4, column=0)
    hidden_label.focus_set() 

    def populate_category_combobox():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM category ORDER BY category_name")
            categories = [category[0] for category in cursor.fetchall()] 
            conn.close()

            category_combobox["values"] = categories

    def clear_combobox_selection(event):
        hidden_label.focus_set()  
        category_combobox.selection_clear() 

    category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
    populate_category_combobox()

    
    add_book_button = Button(container_frame, text="Add Book", font=("Bold", 13), command=lambda: _insert_book(accession_number_entry, author_entry, title_entry, category_combobox, add_book, treeview))
    add_book_button.grid(row=3, column=1,sticky='e', pady=(10,0), ipadx=15, ipady=2)
    
def update_book_window(root, treeview): 
  
    selected_item = treeview.focus()
    if selected_item:
        accession_number = treeview.item(selected_item, "values")[0]
        category = treeview.item(selected_item, "values")[1]
        author = treeview.item(selected_item, "values")[2]
        title = treeview.item(selected_item, "values")[3]
        
        conn = connect_to_database()
        if conn is None:
            messagebox.showerror("Error", "Failed to connect to the database")
            return
        
        cursor = conn.cursor()
        
        query = "SELECT bookID FROM books WHERE accession_no = %s AND author = %s AND title = %s"
        values = (accession_number, author, title)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            bookID = result[0]
        else:
            messagebox.showerror("Error", "Book not found in the database")
            cursor.close()
            conn.close()
            return

        cursor.close()
        conn.close()
        
        update_book = Toplevel(root)
        update_book.withdraw()
        update_book.title("Update Book")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 650
        height = 290
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        update_book.geometry(f"{width}x{height}+{x}+{y}")

        update_book.resizable(False,False)
        validate_func = update_book.register(validate_numbers)

        container_frame = Frame(update_book)
        container_frame.pack(pady=(20,0),padx=(0,20))

        title_label = Label(container_frame, text="Title: ",font=("Bold",16))
        title_label.grid(row=0,column=0,sticky="e",pady=(15,0))
        
        title_entry = Entry(container_frame,font=("", 14),)
        title_entry.grid(row=0,column=1,ipadx=100,ipady=5,pady=(15,0))   
            
        author_label = Label(container_frame, text="Author: ",font=("Bold",16))
        author_label.grid(row=1,column=0,sticky="e",pady=(15,0))
    
        author_entry = Entry(container_frame,font=("", 14),)
        author_entry.grid(row=1,column=1,ipadx=100,ipady=5,pady=(15,0))
        
        accession_number_label = Label(container_frame, text="Accession #: ",font=("Bold",15))
        accession_number_label.grid(row=2,column=0,sticky="e",pady=(15,0))
    
        accession_number_entry = Entry(container_frame,font=("", 14),validate="key", validatecommand=(validate_func, '%d', '%P'))
        accession_number_entry.grid(row=2,column=1,ipadx=100,ipady=5,pady=(15,0))
        
        category_label = Label(container_frame, text="Category: ",font=("Bold",15))
        category_label.grid(row=3,column=0,sticky='e',pady=(15,0))
        
        category_combobox = Combobox(container_frame, state="readonly",width=27,font=("",12))
        category_combobox.grid(row=3, column=1, ipady=5, sticky='w',pady=(15,0))

        hidden_label = Label(container_frame, width=0, height=0,font=("",14))
        hidden_label.grid(row=4, column=0)
        hidden_label.focus_set() 

        def populate_category_combobox():
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT category_name FROM category ORDER BY category_name")
                categories = [category[0] for category in cursor.fetchall()] 
                conn.close()
                
                category_combobox["values"] = categories

        def clear_combobox_selection(event):
            hidden_label.focus_set()  
            category_combobox.selection_clear() 

        category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
        populate_category_combobox()
        
            
        update_book_button = Button(container_frame, text="Update Book", font=("Bold", 13), command=lambda:_update_book(accession_number_entry, author_entry, title_entry, category_combobox, bookID, root, treeview,update_book))
        update_book_button.grid(row=3, column=1,sticky='e', pady=(10,0), ipadx=10, ipady=2)
        

        accession_number_entry.insert(0, accession_number)
        author_entry.insert(0, author)
        title_entry.insert(0, title)
        category_combobox.set(category)
        update_book.deiconify()

    else:
        messagebox.showerror("Error", "No book selected")

def add_category(root,category_combobox):
    add_category = Toplevel(root)
    add_category.withdraw()
    add_category.grab_set()
    add_category.title("Add Category")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 500
    height = 260
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    add_category.geometry(f"{width}x{height}+{x}+{y}")
    
    container = Frame(add_category)
    container.pack(pady=(15,0))
    function_frame = Frame(container)
    function_frame.grid(row=0, column=0,sticky='n',padx=(0,20),)
    category_entry = Entry(function_frame,font=("", 15))
    category_entry.grid(row=0, columnspan=3,pady=(0,15))
    category_button_frame = Frame(function_frame)
    category_button_frame.grid(row=1, columnspan=3)
    add_button = Button(category_button_frame, text="Add",font=("", 10), width=10, command=lambda:_insert_category(category_entry, add_category, tree, category_combobox))
    add_button.pack(side=LEFT, padx=(0,10))
    update_button = Button(category_button_frame, text="Update",font=("", 10), width=10,command=lambda:update_category_window(add_category,tree))
    update_button.pack(side=LEFT)

    
    list_category = Frame(container)
    list_category.grid(row=0, column=1)
    
    tree = Treeview(list_category, columns=("column"), show="headings")
    tree.heading("#0", text="") 
    
    tree.heading("column", text="Category")
    show_all_category(tree)
    tree.pack()
    add_category.deiconify()
    add_category.resizable(False,False)
    
    def update_category_window(root,treeview):
        selected_item = treeview.focus()
        if selected_item:
            category = treeview.item(selected_item, "values")[0]
            
            conn = connect_to_database()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database")
                return
            
            cursor = conn.cursor()
            query = "SELECT * FROM category WHERE category_name = %s"
            values = (category,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                categoryID = result[0]
            else:
                messagebox.showerror("Error", "Category not found in the database")
                cursor.close()
                conn.close()
                return

            cursor.close()
            conn.close()
            
            
            update_category = Toplevel(root)
            update_category.title("Update Category")
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            width = 400
            height = 90
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            update_category.geometry(f"{width}x{height}+{x}+{y}")

            container = Frame(update_category)
            container.pack(pady=(20,0))
            
            update_entry = Entry(container, font=("", 14), width=22)
            update_entry.grid(row = 0, column = 0,padx=(0,10))
            update_button = Button(container, text="Update",font=("", 12), command=lambda:_update_category(update_entry,categoryID, update_category))
            update_button.grid(row = 0, column = 1)
            
            update_entry.insert(0,category)
            
        else:
            messagebox.showerror("Error", "No category selected", parent=root)
            
        def _update_category(category_entry, categoryID, topLevel):
            category = category_entry.get().strip()

            if not category:
                messagebox.showerror("Error", "Please fill in all the fields", parent=root)
                return
            
            conn = connect_to_database()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database")
                return

            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM category WHERE category_name = %s AND categoryID != %s"
            values = (category, categoryID)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result and result[0] > 0:
                messagebox.showerror("Error", "Duplicate category name found", parent=root)
                cursor.close()
                conn.close()
                return

            query = "UPDATE category SET category_name = %s WHERE categoryID = %s"
            values = (category, categoryID)

            try:
                cursor.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success", "Category updated successfully", parent=root)
                show_all_category(treeview)
                topLevel.destroy()
            except mysql.connector.Error as error:
                print("Error updating category:", error)
                messagebox.showerror("Error", "Failed to update the category", parent=root)

            cursor.close()
            conn.close()
            
def student_dashboard(userID):
    root = Tk()
    root.title("SEAIT Library Management System")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 1050
    height = 670
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (750 // 2)
    system_icon =PhotoImage(file = "seait.png")
    root.iconphoto(True, system_icon)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.resizable(False,False)
    
    top_frame = Frame(root)
    top_frame.pack(anchor='w',padx=(15,0),pady=(10,0))
    
    logout_button = Button(top_frame, text="Logout", font=("Calibri", 12, "bold"), fg="#e02e2e", bd=0, bg="white",width=8,command=lambda:back_login(root))
    logout_button.pack(side='left')
    
    currently_borrowed = Button(top_frame, text="Currently Borrowed", font=("Calibri", 11,),width=17,command=lambda:currently_borrowed_books(root, userID))
    currently_borrowed.pack(side=LEFT,padx=(10,0))
    history = Button(top_frame, text="History", font=("Calibri", 11, ),width=11,command=lambda:history_books(root, userID))
    history.pack(side=LEFT,padx=(10,0))
    
    category_combobox = Combobox(top_frame, state="readonly",width=22,font=("Calibri",11))
    category_combobox.pack(side='left',ipady=3,padx=(10,0))

    hidden_label = Label(top_frame, width=0, height=0,font=("",1))
    hidden_label.pack(side='right')
    hidden_label.focus_set() 

    def populate_category_combobox():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM category ORDER BY category_name")
            categories = [category[0] for category in cursor.fetchall()] 
            conn.close()
            categories.insert(0, "All Category")
            category_combobox["values"] = categories
            category_combobox.current(0)

    def clear_combobox_selection(event):
        hidden_label.focus_set()  
        category_combobox.selection_clear() 

    category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
    populate_category_combobox()
    
    
    filter_button = Button(top_frame, text="Filter", font=("Calibri", 11), width=8, command=lambda:filter_books(tree,category_combobox))
    filter_button.pack(side='left',padx=(10,0))
    
    search_label = Label(top_frame,text="Search: ", font=("Calibri", 13))
    search_label.pack(side='left', padx=(10,0))
    
    search_entry = Entry(top_frame, font=("", 12),width=29)
    search_entry.pack(side='left', padx=(5,0), ipady=2)
    
    search_button = Button(top_frame, text="Search", font=("Calibri", 11),width=9,command=lambda:search_book(search_entry, root, tree))
    search_button.pack(side='left', padx=(5,0))
    
  
    
    bottom_frame = Frame(root)
    bottom_frame.pack(fill='x')
    
    list_of_books = Frame(bottom_frame)
    list_of_books.pack(fill='x')
    
    # Create the Treeview widget
    tree = Treeview(list_of_books,height=30)

    # Insert columns
    tree["columns"] = ("Accession", "Category","Author", "Title", "Status")
    
    tree.heading("#0", text="#")
    tree.heading("Accession", text="Accession",anchor='w')
    tree.heading("Category", text="Category",anchor='w')
    tree.heading("Author", text="Author",anchor='w')
    tree.heading("Title", text="Title",anchor='w')
    tree.heading("Status", text="Status",anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="orange", foreground="white",font=("TkDefaultFont", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("#0", width=5,)  # ID column
    tree.column("Accession", width=60)
    tree.column("Category", width=80)
    tree.column("Author", width=120)
    tree.column("Title", width=250)
    tree.column("Status", width=40)
    
    
    show_all_books(tree)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))
    
    root.mainloop()
    
def history_books(root, userID):
    history = Toplevel(root)
    history.grab_set()
    history.title("History")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 930
    height = 590
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (650 // 2)
    history.geometry(f"{width}x{height}+{x}+{y}")

    history.resizable(False,False)
    
    tree = Treeview(history,height=15)

    # Insert columns
    tree["columns"] = ("Accession", "Category", "Title", "Date Issued", "Date Returned")

    tree.heading("Accession", text="Accession", anchor='w')
    tree.heading("Category", text="Category", anchor='w')
    tree.heading("Title", text="Title", anchor='w')
    tree.heading("Date Issued", text="Date Issued", anchor='w')
    tree.heading("Date Returned", text="Date Returned", anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="orange", foreground="white", font=("TkDefaultFont", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("Accession", width=30)
    tree.column("Category", width=120)
    tree.column("Title", width=200)
    tree.column("Date Issued", width=100)
    tree.column("Date Returned", width=100)
    tree["show"] = "headings"
    show_history_borrowed(tree, userID)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))
    
def currently_borrowed_books(root, userID):
    borrowed = Toplevel(root)
    borrowed.grab_set()
    borrowed.title("Currently Borrowed")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 930
    height = 150
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (300 // 2)
    borrowed.geometry(f"{width}x{height}+{x}+{y}")

    borrowed.resizable(False,False)
    
    tree = Treeview(borrowed,height=15)

    # Insert columns
    tree["columns"] = ("Accession", "Category", "Author", "Title", "Date Issued", "Fines")

    tree.heading("Accession", text="Accession", anchor='w')
    tree.heading("Category", text="Category", anchor='w')
    tree.heading("Author", text="Author", anchor='w')
    tree.heading("Title", text="Title", anchor='w')
    tree.heading("Date Issued", text="Date Issued", anchor='w')
    tree.heading("Fines", text="Fines", anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="orange", foreground="white", font=("TkDefaultFont", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("Accession", width=80)
    tree.column("Category", width=120)
    tree.column("Author", width=120)
    tree.column("Title", width=220)
    tree.column("Date Issued", width=100)
    tree.column("Fines", width=30)
    tree["show"] = "headings"
    show_currently_borrowed(tree, userID)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))

call()    


    