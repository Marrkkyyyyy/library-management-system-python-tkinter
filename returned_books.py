from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Combobox, Style, Treeview
from datetime import datetime

import mysql.connector
from db_connection import connect_to_database
from qr_code_scanner import scan_book_qr, scan_id_qr
from show_books import filter_by_date, search_remarks, search_returned_book, show_remarks, show_returned_books
def returned_books_clicked(bottom_frame):
    
    clear_bottom_frame(bottom_frame)
    
    
    def return_information(accession_no_entry,studentID_entry, root):
        if book_condition.get() == "Book Condition":
            messagebox.showerror("Error", "Please select book condition")
            return
        accession = accession_no_entry.get().strip()
        studentID = studentID_entry.get().strip()
        
        conn = connect_to_database()
        if conn is None:
            messagebox.showerror("Error", "Failed to connect to the database")
            return
        
        cursor = conn.cursor()
        
        query = "SELECT bookID, title, accession_no FROM books WHERE accession_no = %s"
        values = (accession,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            bookID = result[0]
            title = result[1]
            accession_no = result[2]
        else:
            messagebox.showerror("Error", "Accession number not found in the database")
            cursor.close()
            conn.close()
            return
        
        query = "SELECT userID, CONCAT(last_name, ', ', first_name, ' ', middle_initial) as fullname, user_school_id FROM user WHERE user_school_id = %s"
        values = (studentID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            userID = result[0]
            fullname = result[1]
            user_school_id = result[2]
        else:
            messagebox.showerror("Error", "Student ID not found in the database")
            cursor.close()
            conn.close()
            return
        
        query = "SELECT GREATEST(DATEDIFF(CURDATE(), date_issued) - 3, 0) AS fines FROM borrowed_books WHERE userID = %s AND bookID = %s"
        values = (userID, bookID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            fines = result[0]
        else:
            messagebox.showerror("Error", "Student ID not found in the database")
            cursor.close()
            conn.close()
            return
        
        info = Toplevel(root)
        info.withdraw()
        info.title("Book Information")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 650
        height = 245
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        info.geometry(f"{width}x{height}+{x}+{y}")
        

        info.resizable(False,False)
        
        container = Frame(info)
        container.pack(anchor='center',pady=(25,0),padx=(15,0))
        
        school_id_label = Label(container, text="School ID:",font=("Calibri", 12, ))
        school_id_label.grid(row=0, column = 0,sticky=E)
        
        school_id = Label(container, text=user_school_id,font=("Calibri", 14, "bold"))
        school_id.grid(row=0, column=1,sticky=W, padx=(5,0))
        
        name_label = Label(container, text="Name:",font=("Calibri", 12, ))
        name_label.grid(row=1, column = 0,sticky=E)
        
        name = Label(container, text=fullname,font=("Calibri", 14, "bold"))
        name.grid(row=1, column=1,sticky=W, padx=(5,0))
        
        accession_label = Label(container, text="Accession:",font=("Calibri", 12, ))
        accession_label.grid(row=2, column = 0,sticky=E)
        
        accession = Label(container, text=accession_no,font=("Calibri", 14, "bold"))
        accession.grid(row=2, column=1,sticky=W, padx=(5,0))
        
        book_title_label = Label(container, text="Book Title:",font=("Calibri", 12, ))
        book_title_label.grid(row=3, column = 0,sticky=E)
        
        book_title = Label(container, text=title,font=("Calibri", 14, "bold"))
        book_title.grid(row=3, column=1,sticky=W, padx=(5,0))
        
        total_fines_label = Label(container, text="Total Fines:",font=("Calibri", 12, ))
        total_fines_label.grid(row=4, column = 0,sticky=E)
        
        total_fines = Label(container, text="₱"+str(fines),font=("Calibri", 14, "bold"))
        total_fines.grid(row=4, column=1,sticky=W, padx=(5,0)) 
        
        return_button = Button(container, text="Return Book",font=("Calibri", 14, "bold"),fg="red",command=lambda:returned_book(accession_no_entry,studentID_entry, info, root, fines))
        return_button.grid(row=5, columnspan=2,pady=(5,0))
        info.deiconify()
    def returned_book(accession_no_entry,studentID_entry,topLevel, root, fines):
        
        if book_condition.get() == "Book Condition":
            messagebox.showerror("Error", "Please select book condition")
            return
        accession = accession_no_entry.get().strip()
        studentID = studentID_entry.get().strip()
        conn = connect_to_database()
        if conn is None:
            messagebox.showerror("Error", "Failed to connect to the database")
            return
        
        cursor = conn.cursor()
        
        query = "SELECT bookID FROM books WHERE accession_no = %s"
        values = (accession,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            bookID = result[0]
        else:
            messagebox.showerror("Error", "Accession number not found in the database")
            cursor.close()
            conn.close()
            return
        
        query = "SELECT userID FROM user WHERE user_school_id = %s"
        values = (studentID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            userID = result[0]
        else:
            messagebox.showerror("Error", "Student ID not found in the database")
            cursor.close()
            conn.close()
            return
        
        query = "SELECT borrowed_bookID, date_issued FROM borrowed_books WHERE bookID = %s and userID = %s"
        values = (bookID,userID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:
            messagebox.showerror("Error", "Invalid Return")
            cursor.close()
            conn.close()
            return
        else:
            borrowed_bookID = result[0]
            date_issued = result[1]
            
        query = "INSERT INTO returned_books (userID, bookID, book_condition, remarks, date_issued, fines) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (userID, bookID, book_condition.get(), remarks_entry.get("1.0", "end-1c"), date_issued, fines)

        try:
            cursor.execute(query, values)

            # Delete the borrowed book record
            delete_query = "DELETE FROM borrowed_books WHERE borrowed_bookID = %s"
            delete_values = (borrowed_bookID,)
            cursor.execute(delete_query, delete_values)

            # Commit the changes
            conn.commit()

            # Show success message
            messagebox.showinfo("Success", "Returned book successfully", master = root)

            # Close the topLevel Toplevel window
            topLevel.destroy()

            # Clear entry fields
            accession_no_entry.delete(0, 'end')
            studentID_entry.delete(0, 'end')

            # Update the Treeview
            show_returned_books(tree)
        except mysql.connector.Error as error:
            print("Error inserting category:", error)
            messagebox.showerror("Error", "Failed to return book")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    # Add the content for the "Returned Books" section
    returned_books_frame = Frame(bottom_frame)
    returned_books_frame.pack(fill='both', expand=True)
    
    returned_book_entry_frame = Frame(returned_books_frame)
    returned_book_entry_frame.pack(side=LEFT, anchor='n',pady=(45,0),padx=7) 
    
    scan_book = Button(returned_book_entry_frame, text="Scan Book", font=("Calibri", 12, ), width=15,command=lambda:scan_book_qr(book_entry))
    scan_book.pack(ipady=2,pady=(0,5))
    book_entry = Entry(returned_book_entry_frame, font=("", 12),width=15)
    book_entry.pack(ipady=2,pady=(0,25))
    scan_ID = Button(returned_book_entry_frame, text="Scan ID", font=("Calibri", 12, ), width=15,command=lambda:scan_id_qr(ID_entry))
    scan_ID.pack(ipady=2,pady=(0,5))
    ID_entry = Entry(returned_book_entry_frame, font=("", 12),width=15)
    ID_entry.pack(ipady=2,pady=(0,25))
    
    book_condition = Combobox(returned_book_entry_frame, values=["Good", "Bad"], state="readonly",font=("Calibri", 12), width=15)
    book_condition.set("Book Condition")
    book_condition.pack(ipady=2)
    hidden_label = Label(returned_book_entry_frame, width=0, height=0,font=("",14))
    hidden_label.pack()
    hidden_label.focus_set() 
    def clear_combobox_selection(event):
            hidden_label.focus_set()  
            book_condition.selection_clear() 

    book_condition.bind("<<ComboboxSelected>>", clear_combobox_selection)
    remarks_label = Label(returned_book_entry_frame, text="Remarks", font=("Calibri", 13))
    remarks_label.pack(pady=(0,5))  
    remarks_entry = scrolledtext.ScrolledText(returned_book_entry_frame, font=("", 12), width=14, height=5)
    remarks_entry.pack(pady=(0,15))
    
    return_book = Button(returned_book_entry_frame, text="Return", font=("Calibri", 12, "bold"), width=15, fg="#0089a3", command=lambda:return_information(book_entry,ID_entry,returned_books_frame))
    return_book.pack(ipady=2)
    
    right_frame = Frame(returned_books_frame)
    right_frame.pack(side=LEFT,fill='both', expand=True,ipadx=140)
    search_frame = Frame(right_frame)
    search_frame.pack(anchor='w',pady=5)
    
    search_label = Label(search_frame, text="Search: ", font=('Calibri', 13))
    search_label.pack(side=LEFT,padx=(2,0))
    search_entry = Entry(search_frame, font=("", 12),width=37)
    search_entry.pack(side=LEFT,ipady=2,padx=(2,0))
    search_button = Button(search_frame, text='Search', font=("Calibri", 12),width=10,command=lambda:search_returned_book(search_entry, returned_books_frame, tree))
    search_button.pack(side=LEFT,padx=(5,0))
    
    category_combobox = Combobox(search_frame, state="readonly",width=15,font=("",12))
    category_combobox.pack(side='left', padx=(5,0), ipady=4)

    hidden_label = Label(search_frame, width=0, height=0,font=("",2))
    hidden_label.pack(side='left',)
    hidden_label.focus_set() 

    def clear_combobox_selection(event):
        hidden_label.focus_set()  
        category_combobox.selection_clear() 

    category_combobox.bind("<<ComboboxSelected>>", clear_combobox_selection)
    category_combobox["values"] = ['All','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    category_combobox.current(0)
    
    filter_button = Button(search_frame, text='Filter', font=("Calibri", 12),width=10, command=lambda:filter_by_date(tree, category_combobox) )
    filter_button.pack(side='left')
    remarks_button = Button(search_frame, text='Remarks', font=("Calibri", 12),width=13, command=lambda:remarks(returned_books_frame) )
    remarks_button.pack(side='left',padx=(10,0))
    
    returned_list_frame = Frame(right_frame)
    returned_list_frame.pack(side=LEFT,fill='both', expand=True,ipadx=140)
    
    tree = Treeview(returned_list_frame, height=28)

    # Insert columns
    tree["columns"] = ("Name", "Title", "Category", "Accession", "Date Issued", "Date Returned")
    
    tree.heading("#0", text="")
    tree.heading("Name", text="Name",anchor='w')
    tree.heading("Title", text="Title",anchor='w')
    tree.heading("Category", text="Category",anchor='w')
    tree.heading("Accession", text="Accession",anchor='w')
    tree.heading("Date Issued", text="Date Issued",anchor='w')
    tree.heading("Date Returned", text="Date Returned",anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#02d2d3", foreground="white",font=("Calibri", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree['show'] = 'headings'
    tree.column("Name", width=5)
    tree.column("Title", width=40)
    tree.column("Category", width=40)
    tree.column("Accession", width=5)
    tree.column("Date Issued", width=10)
    tree.column("Date Returned", width=10)
    show_returned_books(tree)
    tree.pack(fill='both', expand=True)


def clear_bottom_frame(bottom_frame):
    # Clear existing content in the bottom_frame
    for widget in bottom_frame.winfo_children():
        widget.destroy()
        
def remarks(root):
    borrowed = Toplevel(root)
    borrowed.grab_set()
    borrowed.title("Remarks")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 980
    height = 580
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (600 // 2)
    borrowed.geometry(f"{width}x{height}+{x}+{y}")

    borrowed.resizable(False,False)
    

    
    container = Frame(borrowed)
    container.pack(anchor='nw',pady=(5,0),padx=(10,0)) 
    
    search_label = Label(container, text="Search: ", font=('Calibri', 13))
    search_label.pack(side=LEFT,padx=(2,0))
    search_entry = Entry(container, font=("", 12),width=37)
    search_entry.pack(side=LEFT,ipady=2,padx=(2,0))
    search_button = Button(container, text='Search', font=("Calibri", 12),width=10,command=lambda:search_remarks(search_entry, borrowed, tree))
    search_button.pack(side=LEFT,padx=(5,0))
    
    remarks_list_frame = Frame(borrowed)
    remarks_list_frame.pack(fill='both', expand=True,ipadx=140)
    
    tree = Treeview(remarks_list_frame,height=15)

    # Insert columns
    tree["columns"] = ("School ID", "Name", "Title", "Accession", "Condition", "Remarks")

    tree.heading("School ID", text="School ID", anchor='w')
    tree.heading("Name", text="Name", anchor='w')
    tree.heading("Title", text="Title", anchor='w')
    tree.heading("Accession", text="Accession", anchor='w')
    tree.heading("Condition", text="Condition", anchor='w')
    tree.heading("Remarks", text="Remarks", anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#02d2d3", foreground="white", font=("TkDefaultFont", 11, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("School ID", width=40)
    tree.column("Name", width=80)
    tree.column("Title", width=100)
    tree.column("Accession", width=40)
    tree.column("Condition", width=40)
    tree.column("Remarks", width=100)
    tree["show"] = "headings"
    show_remarks(tree)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))