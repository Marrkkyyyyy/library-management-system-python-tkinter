from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Style, Treeview
from db_connection import connect_to_database
from datetime import datetime
import mysql.connector

from qr_code_scanner import scan_book_qr, scan_id_qr
from show_books import search_borrowed_books, show_borrowed_books

def borrowed_books_clicked(bottom_frame):
           
    def issue_book(accession_no_entry,studentID_entry):
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
        
        query = "SELECT * FROM borrowed_books WHERE bookID = %s"
        values = (bookID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] > 0:
            messagebox.showerror("Error", "This book is already issued")
            cursor.close()
            conn.close()
            return
            
        query = "SELECT COUNT(*) FROM borrowed_books WHERE userID = %s"
        values = (userID,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None and result[0] >= 3:
            messagebox.showerror("Limit Reached", "You have reached the maximum limit for book borrowing. Please return one or more books to borrow additional titles.")
            cursor.close()
            conn.close()
            return
            
        query = "INSERT INTO borrowed_books (userID, bookID) VALUES (%s, %s)"
        values = (userID, bookID)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Issue book successfully")
            accession_no_entry.delete(0, 'end')
            studentID_entry.delete(0, 'end')
            show_borrowed_books(tree)
        except mysql.connector.Error as error:
            print("Error inserting category:", error)
            messagebox.showerror("Error", "Failed to issue book")

        cursor.close()
        conn.close()
        
        
    clear_bottom_frame(bottom_frame)

    borrowed_books_frame = Frame(bottom_frame)
    borrowed_books_frame.pack(fill='both', expand=True)


    issue_book_frame = Frame(borrowed_books_frame)
    issue_book_frame.pack(fill='x', expand=True,) 
    
    container = Frame(issue_book_frame)
    container.pack(side='left',pady=(5,0)) 

    scan_book = Button(container, text="Scan Book", font=("Calibri", 11), width=10,command=lambda:scan_book_qr(book_entry))
    scan_book.pack(side='left', padx=(10,0))
    book_entry = Entry(container, font=("", 12), width=14)
    book_entry.pack(side='left', ipady=2, padx=(10,0))
    scan_ID = Button(container, text="Scan ID", font=("Calibri", 11), width=10,command=lambda:scan_id_qr(ID_entry))
    scan_ID.pack(side='left', padx=(10,0))
    ID_entry = Entry(container, font=("", 12), width=14)
    ID_entry.pack(side='left', ipady=2, padx=(10,0))
    issue_button = Button(container, text="Issue", font=("Calibri", 12,"bold"), width=10, fg="#f71111",command=lambda:issue_book(book_entry, ID_entry))
    issue_button.pack(side='left', padx=(10,0))
    
    search_label = Label(container,text="Search: ", font=("Calibri", 13))
    search_label.pack(side='left', padx=(10,0))
    
    search_entry = Entry(container, font=("", 12),width=32)
    search_entry.pack(side='left', padx=(5,0), ipady=2)
    
    search_button = Button(container, text="Search", font=("Calibri", 11),width=10,command= lambda:search_borrowed_books(search_entry, borrowed_books_frame, tree))
    search_button.pack(side='left', padx=(5,0))
    
    borrowed_list_frame = Frame(borrowed_books_frame)
    borrowed_list_frame.pack(fill='both', expand=True,ipadx=140)


    tree = Treeview(borrowed_list_frame, height=30)

    # Insert columns
    tree["columns"] = ("School ID", "Name", "Title", "Category", "Accession", "Date Issued")
    
    tree.heading("#0", text="")
    tree.heading("School ID", text="School ID",anchor='w')
    tree.heading("Name", text="Name",anchor='w')
    tree.heading("Title", text="Title",anchor='w')
    tree.heading("Category", text="Category",anchor='w')
    tree.heading("Accession", text="Accession",anchor='w')
    tree.heading("Date Issued", text="Date Issued",anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#f71111", foreground="white",font=("Calibri", 12, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree['show'] = 'headings'
    tree.column("School ID", width=30)
    tree.column("Name", width=70)
    tree.column("Title", width=140)
    tree.column("Category", width=60)
    tree.column("Accession", width=20)
    tree.column("Date Issued", width=20)
    
    show_borrowed_books(tree)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))

def clear_bottom_frame(bottom_frame):
    # Clear existing content in the bottom_frame
    for widget in bottom_frame.winfo_children():
        widget.destroy()
