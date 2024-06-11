from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Combobox, Style, Treeview
from tkcalendar import Calendar
import datetime
import mysql.connector
from db_connection import connect_to_database
from show_books import show_reports
def reports_clicked(bottom_frame):
    
    clear_bottom_frame(bottom_frame)
    
    # Add the content for the "Returned Books" section
    reports_frame = Frame(bottom_frame)
    reports_frame.pack(fill='both', expand=True)
   
    container = Frame(reports_frame)
    container.pack(anchor='nw',pady=(5,0),padx=(10,0)) 
    
    def generate_report(from_date_entry, to_date_entry,tree):
        def validate_date_format(date_str):
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        from_date = from_date_entry.get().strip()
        to_date = to_date_entry.get().strip()
        
        if not from_date or not to_date:
            messagebox.showwarning("Incomplete Form", "Please fill in all the required fields.")
            return
        # Validate and process the from_date
        if validate_date_format(from_date):
            # Process the from_date further
            print("Valid from_date:", from_date)
        else:
            messagebox.showwarning("Error", "Invalid from_date. Please use the yyyy-mm-dd format.")
            
            return
        # Validate and process the to_date
        if validate_date_format(to_date):
            # Process the to_date further
            print("Valid to_date:", to_date)
        else:
            messagebox.showwarning("Error", "Invalid to_date. Please use the yyyy-mm-dd format.")
            return
        
        conn = connect_to_database()
        if conn is None:
            # Handle connection error
            messagebox.showerror("Database Error", "Error connecting to the database. Please try again later.")
            return

        try:
            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Check if user_school_id already exists
            query = "SELECT COUNT(*) FROM books WHERE date_created BETWEEN %s AND %s"
            values = (from_date, to_date)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result is not None and result[0] > 0:
                new_arrival = result[0]
            else:
                messagebox.showerror("Error", "Invalid Date")
                cursor.close()
                conn.close()
                return

            # Check if username already exists
            query = "SELECT SUM(fines) FROM returned_books WHERE date_returned BETWEEN %s AND %s"
            values = (from_date, to_date)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result is not None and result[0] >= 0:
                total_fines = result[0]
            else:
                messagebox.showerror("Error", "Invalid Date")
                cursor.close()
                conn.close()
                return

            # Prepare the INSERT statement
            sql = "INSERT INTO reports (from_date, to_date, new_arrival, total_fines) VALUES (%s, %s, %s, %s)"
            values = (from_date, to_date, new_arrival, total_fines)

            # Execute the INSERT statement
            cursor.execute(sql, values)

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and database connection
            cursor.close()
            conn.close()

            # Show a success message
            messagebox.showinfo("Generated Report Successful", "Report generated successfully.")
            from_date_entry.delete(0, 'end')
            to_date_entry.delete(0, 'end')
            show_reports(tree)

        except mysql.connector.Error as error:
            # Handle database error
            messagebox.showerror("Database Error", f"Error inserting user data into the database: {error}")

            # Roll back any changes in case of an error
            conn.rollback()

            # Close the cursor and database connection
            cursor.close()
            conn.close()
        
        
    
    def from_date_picker():
        top = Toplevel(container)
        top.grab_set()
        top.title("From Date")
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        width = 250
        height = 185
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        top.geometry(f"{width}x{height}+{x}+{y}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack()

        def get_selected_date(event=None):
            selected_date = cal.get_date()
            from_entry.delete(0, 'end') 
            from_entry.insert(0, selected_date)
            top.destroy()

        cal.bind("<<CalendarSelected>>", get_selected_date)

        top.mainloop()

    from_date = Button(container, text='From', command=from_date_picker, font=("Calibri", 11), width=8)
    from_date.pack(side=LEFT,padx=(10,0))
    
    from_entry = Entry(container, font=("Calibri", 12))
    from_entry.pack(side=LEFT,padx=(10,0),ipady=2)
    
    def to_date_picker():
        top = Toplevel(container)
        top.grab_set()
        top.title("To Date")
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        width = 250
        height = 185
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        top.geometry(f"{width}x{height}+{x}+{y}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack()

        def get_selected_date(event=None):
            selected_date = cal.get_date()
            to_entry.delete(0, 'end') 
            to_entry.insert(0, selected_date)
            top.destroy()

        cal.bind("<<CalendarSelected>>", get_selected_date)

        top.mainloop()

    to_date = Button(container, text='To', command=to_date_picker, font=("Calibri", 11), width=8)
    to_date.pack(side=LEFT,padx=(10,0))
    
    to_entry = Entry(container, font=("Calibri", 12))
    to_entry.pack(side=LEFT,padx=(10,0),ipady=2)
    
    generate_report_button = Button(container, text="Generate Report", width=15, font=("Calibri", 12),fg="brown",command=lambda:generate_report(from_entry, to_entry,tree))
    generate_report_button.pack(side=LEFT,padx=(10,0))
    
    remarks_list_frame = Frame(reports_frame)
    remarks_list_frame.pack(fill='both', expand=True,ipadx=140)
    
    tree = Treeview(remarks_list_frame,height=30)

    # Insert columns
    tree["columns"] = ("From", "To", "New Arrival", "Total Fines", "Date Created")

    tree.heading("From", text="From", anchor='w')
    tree.heading("To", text="To", anchor='w')
    tree.heading("New Arrival", text="New Arrival", anchor='w')
    tree.heading("Total Fines", text="Total Fines", anchor='w')
    tree.heading("Date Created", text="Date Created", anchor='w')
    s = Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="brown", foreground="white", font=("TkDefaultFont", 11, "bold"), bordercolor="white", borderwidth=2)
    s.map('Treeview.Heading', background=[('active', '!disabled', 'grey')])
    # Set column widths based on content
    tree.column("From", width=40)
    tree.column("To", width=80)
    tree.column("New Arrival", width=40)
    tree.column("Total Fines", width=40)
    tree.column("Date Created", width=100)
    tree["show"] = "headings"
    show_reports(tree)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True, pady=(8, 0))
    


def clear_bottom_frame(bottom_frame):
    # Clear existing content in the bottom_frame
    for widget in bottom_frame.winfo_children():
        widget.destroy()
  