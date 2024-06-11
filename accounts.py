from tkinter import *
from tkinter.ttk import Combobox, Style, Treeview
from show_books import show_admin, show_user
from admin_sign_up import *

def search_borrowed_books(search_entry, add_account_frame, tree ):
        search = search_entry.get().strip()
        add_account_frame.focus()
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT userID, CONCAT(last_name, ', ', first_name, ' ', middle_initial) as fullname, username, user_school_id FROM user 
                WHERE user_school_id LIKE %s 
                OR CONCAT(last_name, ', ', first_name) LIKE %s 
                OR last_name LIKE %s 
                OR first_name LIKE %s 
                ORDER BY last_name
            """
            values = ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%')
            cursor.execute(query, values)
            books = cursor.fetchall()
            conn.close()


            # Clear existing items in the Treeview
            tree.delete(*tree.get_children())
            id_counter = 1
            for book in books:
                tree.insert("", "end", text=id_counter, values=(book[1], book[2],book[3]))
                id_counter += 1

def add_account_window(root,treeAdmin):
    add_account = Toplevel(root)
    add_account.grab_set()
    add_account.title("Add Account")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 470
    height = 340
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    add_account.geometry(f"{width}x{height}+{x}+{y}")

    add_account.resizable(False,False)
    
    container = Frame(add_account)
    container.pack(pady=(30,0), padx=(0,20))
    
    validate_name_cmd = (container.register(validate_name), "%P")
    validate_middle_initial_cmd = (container.register(validate_middle_initial), "%P")
    validate_password_entry_cmd = (container.register(validate_password_entry),)
    
    firstName_label = Label(container, text="First Name:", font=("Calibri", 12, "bold"))
    firstName_label.grid(row=1, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    firstName_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_name_cmd)
    firstName_entry.grid(row=1, column=1, ipady=2, pady=(0, 10))

    lastName_label = Label(container, text="Last Name:", font=("Calibri", 12, "bold"))
    lastName_label.grid(row=2, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    lastName_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_name_cmd)
    lastName_entry.grid(row=2, column=1, pady=(0, 10), ipady=2)

    middleInitial_label = Label(container, text="Middle Initial:", font=("Calibri", 12, "bold"))
    middleInitial_label.grid(row=3, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    middleInitial_entry = Entry(container, font=("Calibri", 12), width=30, validate="key", validatecommand=validate_middle_initial_cmd)
    middleInitial_entry.grid(row=3, column=1, pady=(0, 10), ipady=2)
    
    user_type_label = Label(container, text="User Type:", font=("Calibri", 12, "bold"))
    user_type_label.grid(row=4, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    user_type_entry = Combobox(container, values=["Admin", "Staff"], state="readonly",font=("Calibri", 12), width=28)
    user_type_entry.set("Admin")
    user_type_entry.grid(row=4, column=1, pady=(0, 10),ipady=2,)
    hidden_label = Label(container, width=0, height=0,font=("",14))
    hidden_label.grid(row=5, column=1, pady=(0, 10))
    hidden_label.focus_set() 
    def clear_combobox_selection(event):
            hidden_label.focus_set()  
            user_type_entry.selection_clear() 

    user_type_entry.bind("<<ComboboxSelected>>", clear_combobox_selection)

    username_label = Label(container, text="Username:", font=("Calibri", 12, "bold"))
    username_label.grid(row=5, column=0, sticky='e', padx=(0, 5), pady=(0, 10))
    
    username_entry = Entry(container, font=("Calibri", 12), width=30)
    username_entry.grid(row=5, column=1, pady=(0, 10), ipady=2)
    
    password_label = Label(container, text="Password:", font=("Calibri", 12, "bold"))
    password_label.grid(row=6, column=0, sticky='e', padx=(0, 5), pady=(0, 10))

    password_entry = Entry(container, font=("Calibri", 12), width=30, show="*",  validatecommand=validate_password_entry_cmd)
    password_entry.grid(row=6, column=1, pady=(0, 10), ipady=2)
    
    register_button = Button(container, font=("Calibri", 12, ),width = 29, text="Register",command=lambda:register_admin(firstName_entry,lastName_entry,middleInitial_entry,username_entry,password_entry, user_type_entry,treeAdmin))
    register_button.grid(row=7, columnspan=2,ipady=1, sticky="e")


def accounts_clicked(bottom_frame):
        
    clear_bottom_frame(bottom_frame)

    accounts_frame = Frame(bottom_frame)
    accounts_frame.pack(fill='both', expand=True)
    
    option_frame = Frame(accounts_frame)
    option_frame.pack(fill='x', expand=True, padx=(0,10)) 
    
    container = Frame(option_frame)
    container.pack(side='left',pady=(5,0)) 
    
    add_account = Button(container, text="Add Account", font=("Calibri", 11), width=15, command=lambda:add_account_window(accounts_frame, treeAdmin))
    add_account.pack(side='left', padx=(125,0))
    delete_account = Button(container, text="Delete Account", font=("Calibri", 11), width=15,command=lambda:delete_admin(treeAdmin))
    delete_account.pack(side='left', padx=(10,0))
    
    search_label = Label(container,text="Search: ", font=("Calibri", 13))
    search_label.pack(side='left', padx=(130,0))
    
    search_entry = Entry(container, font=("", 12),width=39)
    search_entry.pack(side='left', padx=(5,0), ipady=2)
    
    search_button = Button(container, text="Search", font=("Calibri", 11),width=10, command=lambda:search_borrowed_books(search_entry,add_account,treeStudent))
    search_button.pack(side='left', padx=(5,0))

    

    account_list_frame = Frame(accounts_frame)
    account_list_frame.pack(anchor='e')
    
    admin_frame = Frame(account_list_frame)
    admin_frame.pack(side=LEFT,fill='both', expand=True,ipadx=120)
    
    student_frame = Frame(account_list_frame)
    student_frame.pack(side=LEFT,fill='both', expand=True,ipadx=120, padx=(5,5))
    


    treeStudent = Treeview(student_frame, height=28)

    # Insert columns
    treeStudent["columns"] = ("Name", "Username", "School ID")
    
    treeStudent.heading("#0", text="ID")
    treeStudent.heading("Name", text="Name", anchor='w')
    treeStudent.heading("Username", text="Username", anchor='w')
    treeStudent.heading("School ID", text="School ID", anchor='w')

    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#44bbff", foreground="white", font=("Calibri", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])

    # Set column widths based on content
    treeStudent.column("#0", width=5) 
    treeStudent.column("Name", width=140)
    treeStudent.column("Username", width=70)
    treeStudent.column("School ID", width=60)
    treeStudent["selectmode"] = "none"
    show_user(treeStudent)
    treeStudent.pack(fill='both', expand=True, pady=(8, 0))
    
    
    treeAdmin = Treeview(admin_frame)

    # Insert columns
    treeAdmin["columns"] = ("Name", "Username", "User Type")
    
    treeAdmin.heading("#0", text="")
    treeAdmin.heading("Name", text="Name",anchor='w')
    treeAdmin.heading("Username", text="Username",anchor='w')
    treeAdmin.heading("User Type", text="User Type",anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#44bbff", foreground="white",font=("Calibri", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    treeAdmin['show'] = 'headings'
    treeAdmin.column("Name", width=140)
    treeAdmin.column("Username", width=70)
    treeAdmin.column("User Type", width=60)
    show_admin(treeAdmin)
    treeAdmin.pack(fill='both', expand=True, pady=(8, 0))

def clear_bottom_frame(bottom_frame):
    # Clear existing content in the bottom_frame
    for widget in bottom_frame.winfo_children():
        widget.destroy()


