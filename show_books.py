import datetime
from tkinter import messagebox
from db_connection import connect_to_database


def show_all_books(treeview):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                books.bookID,
                books.accession_no,
                category.category_name,
                books.author,
                books.title,
                CASE
                    WHEN borrowed_books.bookID IS NOT NULL THEN 'Unavailable'
                    ELSE 'Available'
                END AS status
            FROM
                books
            INNER JOIN category ON books.categoryID = category.categoryID
            LEFT JOIN borrowed_books ON books.bookID = borrowed_books.bookID
            ORDER BY
                category.category_name,
                books.title
        """)
        books = cursor.fetchall()
        conn.close()


        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert fetched books into the Treeview
        id_counter = 1
        for book in books:
            treeview.insert("", "end", text=id_counter, values=(book[1], book[2],book[3], book[4], book[5]))
            id_counter += 1
            
def show_currently_borrowed(treeview, userID):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT borrowed_books.borrowed_bookID, 
            books.accession_no, 
            category.category_name, 
            books.author,
            books.title,
            borrowed_books.date_issued,
            GREATEST(DATEDIFF(CURDATE(), borrowed_books.date_issued) - 3, 0) AS fines
            FROM borrowed_books 
            INNER JOIN books ON borrowed_books.bookID = books.bookID 
            INNER JOIN category ON books.categoryID = category.categoryID 
            WHERE userID = %s
            ORDER BY borrowed_books.date_issued DESC
        """
        values = (userID,)
        cursor.execute(query, values)
        books = cursor.fetchall()
        conn.close()


        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert fetched books into the Treeview
        for book in books:
            if isinstance(book[5], str):
                    date_issued = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
            else:
                date_issued = book[5]
                
            # Format the date
            formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
            treeview.insert("", "end", values=(book[1], book[2],book[3], book[4], formatted_date, book[6]))
            
def show_history_borrowed(treeview, userID):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT returned_books.returned_bookID, 
            books.accession_no, 
            category.category_name, 
            books.title, 
            returned_books.date_issued, 
            returned_books.date_returned 
            FROM returned_books 
            INNER JOIN books ON returned_books.bookID = books.bookID 
            INNER JOIN category ON books.categoryID = category.categoryID
            WHERE userID = %s
            ORDER BY returned_books.date_returned DESC
        """
        values = (userID,)
        cursor.execute(query, values)
        books = cursor.fetchall()
        conn.close()


        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert fetched books into the Treeview
        for book in books:
            if isinstance(book[4], str) or isinstance(book[5], str):
                date_issued = datetime.strptime(book[4], "%Y-%m-%d %H:%M:%S")
                date_returned = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
            else:
                date_issued = book[4]
                date_returned = book[5]
                
            # Format the date
            formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
            formatted_date2 = date_returned.strftime("%b. %d, %Y %I:%M %p")
            treeview.insert("", "end", values=(book[1], book[2],book[3], formatted_date, formatted_date2))

            
            
def search_book(search_entry, root, tree):
        filter_text = search_entry.get().strip()
        root.focus()
        if filter_text != "Filter title, author...":
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                query = """
                    SELECT books.bookID, books.accession_no, category.category_name, books.author, books.title,
                    CASE WHEN borrowed_books.bookID IS NOT NULL THEN 'Unavailable' ELSE 'Available' END AS status
                    FROM books
                    INNER JOIN category ON books.categoryID = category.categoryID
                    LEFT JOIN borrowed_books ON books.bookID = borrowed_books.bookID
                    WHERE books.title LIKE %s OR books.author LIKE %s OR books.accession_no LIKE %s
                    ORDER BY books.bookID DESC
                """
                values = ('%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%')
                cursor.execute(query, values)
                books = cursor.fetchall()
                conn.close()


                # Clear existing items in the Treeview
                tree.delete(*tree.get_children())

                id_counter = 1
                for book in books:
                    tree.insert("", "end", text=id_counter,values=(book[1], book[2],book[3], book[4], book[5]))
                    id_counter += 1
                    
        
def filter_books(treeview, category_entry):
            category = category_entry.get().strip()

            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()

                if category == "All Category":
                    query = """
                        SELECT books.bookID, books.accession_no, category.category_name, books.author, books.title,
                        CASE WHEN borrowed_books.bookID IS NOT NULL THEN 'Unavailable' ELSE 'Available' END AS status
                        FROM books
                        INNER JOIN category ON books.categoryID = category.categoryID
                        LEFT JOIN borrowed_books ON books.bookID = borrowed_books.bookID
                        ORDER BY books.title
                    """
                    cursor.execute(query)
                else:
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

                    query = """
                        SELECT books.bookID, books.accession_no, category.category_name, books.author, books.title,
                        CASE WHEN borrowed_books.bookID IS NOT NULL THEN 'Unavailable' ELSE 'Available' END AS status
                        FROM books
                        INNER JOIN category ON books.categoryID = category.categoryID
                        LEFT JOIN borrowed_books ON books.bookID = borrowed_books.bookID
                        WHERE books.categoryID = %s
                    """
                    values = (categoryID,)
                    cursor.execute(query, values)


                books = cursor.fetchall()
                conn.close()

                # Clear existing items in the Treeview
                treeview.delete(*treeview.get_children())

                # Insert filtered books into the Treeview
                id_counter = 1
                for book in books:
                    treeview.insert("", "end", text=id_counter, values=(book[1], book[2], book[3], book[4], book[5]))
                    id_counter += 1
                    
def search_borrowed_books(search_entry, borrowed_books_frame, tree ):
        search = search_entry.get().strip()
        borrowed_books_frame.focus()
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT borrowed_books.borrowed_bookID, user.user_school_id,CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname,
                books.title, category.category_name, books.accession_no, borrowed_books.date_issued
                FROM borrowed_books
                INNER JOIN books ON borrowed_books.bookID = books.bookID
                INNER JOIN user ON borrowed_books.userID = user.userID
                INNER JOIN category ON books.categoryID = category.categoryID
                WHERE books.title LIKE %s
                OR category.category_name LIKE %s
                OR user.user_school_id LIKE %s
                OR books.accession_no LIKE %s
                OR user.last_name LIKE %s
                OR user.first_name LIKE %s
                OR CONCAT(user.last_name, ', ', user.first_name) LIKE %s
                ORDER BY borrowed_books.borrowed_bookID DESC
            """
            values = ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%')
            cursor.execute(query, values)
            books = cursor.fetchall()
            conn.close()


            # Clear existing items in the Treeview
            tree.delete(*tree.get_children())

            for book in books:
                if isinstance(book[6], str):
                    date_issued = datetime.strptime(book[6], "%Y-%m-%d %H:%M:%S")
                else:
                    date_issued = book[6]
                    
                # Format the date
                formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                tree.insert("", "end", values=(book[1], book[2],book[3], book[4], book[5],formatted_date))
                

def search_returned_book(search_entry, returned_books_frame, tree):
        search = search_entry.get().strip()
        returned_books_frame.focus()
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT returned_books.returned_bookID, CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname,
                books.title, category.category_name, books.accession_no, returned_books.date_issued, returned_books.date_returned
                FROM returned_books
                INNER JOIN books ON returned_books.bookID = books.bookID
                INNER JOIN user ON returned_books.userID = user.userID
                INNER JOIN category ON books.categoryID = category.categoryID
                WHERE books.title LIKE %s
                OR category.category_name LIKE %s
                OR books.accession_no LIKE %s
                OR user.last_name LIKE %s
                OR user.first_name LIKE %s
                OR CONCAT(user.last_name, ', ', user.first_name) LIKE %s
                ORDER BY returned_books.returned_bookID DESC
            """
            values = ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%')
            cursor.execute(query, values)
            books = cursor.fetchall()
            conn.close()


            # Clear existing items in the Treeview
            tree.delete(*tree.get_children())

            for book in books:
                if isinstance(book[5], str) or isinstance(book[6], str):
                    date_issued = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
                    date_returned = datetime.strptime(book[6], "%Y-%m-%d %H:%M:%S")
                else:
                    date_issued = book[5]
                    date_returned = book[6]
                    
                # Format the date
                formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                formatted_date2 = date_returned.strftime("%b. %d, %Y %I:%M %p")
                tree.insert("", "end", values=(book[1], book[2],book[3], book[4], formatted_date, formatted_date2))
                
                
def show_returned_books(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT returned_books.returned_bookID, CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname, books.title, category.category_name, books.accession_no, returned_books.date_issued, returned_books.date_returned FROM (((returned_books INNER JOIN books ON returned_books.bookID = books.bookID) INNER JOIN user ON returned_books.userID = user.userID) INNER JOIN category ON books.categoryID = category.categoryID) ORDER BY returned_books.returned_bookID DESC")
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

           
            for book in books:
                # Check if the date is already a string
                if isinstance(book[5], str) or isinstance(book[6], str):
                    date_issued = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
                    date_returned = datetime.strptime(book[6], "%Y-%m-%d %H:%M:%S")
                else:
                    date_issued = book[5]
                    date_returned = book[6]
                    
                # Format the date
                formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                formatted_date2 = date_returned.strftime("%b. %d, %Y %I:%M %p")
                
                treeview.insert("", "end", values=(book[1], book[2], book[3], book[4], formatted_date, formatted_date2))
                
                
def show_borrowed_books(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT borrowed_books.borrowed_bookID, user.user_school_id, CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname, books.title, category.category_name, books.accession_no, borrowed_books.date_issued FROM (((borrowed_books INNER JOIN books ON borrowed_books.bookID = books.bookID) INNER JOIN user ON borrowed_books.userID = user.userID) INNER JOIN category ON books.categoryID = category.categoryID) ORDER BY borrowed_books.borrowed_bookID DESC")
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

           
            for book in books:
                # Check if the date is already a string
                if isinstance(book[6], str):
                    date_issued = datetime.strptime(book[6], "%Y-%m-%d %H:%M:%S")
                else:
                    date_issued = book[6]
                    
                # Format the date
                formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                
                treeview.insert("", "end", values=(book[1], book[2], book[3], book[4], book[5], formatted_date))
                
                
def filter_by_date(treeview, date_entry):
            date = date_entry.get().strip()

            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()

                if date == "All":
                    query = """
                        SELECT returned_books.returned_bookID, CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname, books.title, category.category_name, books.accession_no, returned_books.date_issued, returned_books.date_returned FROM (((returned_books INNER JOIN books ON returned_books.bookID = books.bookID) INNER JOIN user ON returned_books.userID = user.userID) INNER JOIN category ON books.categoryID = category.categoryID) 
                        ORDER BY returned_books.returned_bookID DESC
                    """
                    cursor.execute(query)
                else:
                    current_year = datetime.datetime.now().year
                    query = """
                        SELECT returned_books.returned_bookID, CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname, books.title, category.category_name, books.accession_no, returned_books.date_issued, returned_books.date_returned 
                        FROM (((returned_books INNER JOIN books ON returned_books.bookID = books.bookID) 
                        INNER JOIN user ON returned_books.userID = user.userID) 
                        INNER JOIN category ON books.categoryID = category.categoryID) 
                        WHERE MONTHNAME(returned_books.date_returned) = %s AND YEAR(returned_books.date_returned) = %s
                        ORDER BY returned_books.returned_bookID DESC
                    """
                    values = (date, current_year)
                    cursor.execute(query, values)


                books = cursor.fetchall()
                conn.close()

                # Clear existing items in the Treeview
                treeview.delete(*treeview.get_children())

                # Insert filtered books into the Treeview
                id_counter = 1
                for book in books:
                    if isinstance(book[5], str) or isinstance(book[6], str):
                        date_issued = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
                        date_returned = datetime.strptime(book[6], "%Y-%m-%d %H:%M:%S")
                    else:
                        date_issued = book[5]
                        date_returned = book[6]
                        
                    # Format the date
                    formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                    formatted_date2 = date_returned.strftime("%b. %d, %Y %I:%M %p")
                    treeview.insert("", "end", text=id_counter, values=(book[1], book[2], book[3], book[4], formatted_date, formatted_date2))
                    id_counter += 1
                    
                    
def show_admin(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT adminID, CONCAT(last_name, ', ', first_name, ' ', middle_initial) as fullname, username, user_type FROM admin")
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

           
            for book in books:
                treeview.insert("", "end", values=(book[1], book[2], book[3]))
                
def show_user(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userID, CONCAT(last_name, ', ', first_name, ' ', middle_initial) as fullname, username, user_school_id FROM user")
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

            id_counter = 1
            for book in books:
                treeview.insert("", "end", text=id_counter, values=(book[1], book[2], book[3]))
                id_counter += 1
                

def show_remarks(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT returned_books.returned_bookID, 
            user.user_school_id, 
            CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname, 
            books.title, books.accession_no, 
            returned_books.book_condition, 
            returned_books.remarks
            FROM returned_books
            INNER JOIN user ON returned_books.userID = user.userID
            INNER JOIN books ON returned_books.bookID = books.bookID
            WHERE returned_books.remarks <> '' OR returned_books.book_condition = 'Bad'
            ORDER BY returned_books.returned_bookID DESC;
            """)
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())
     
            for book in books:
                treeview.insert("", "end", values=(book[1], book[2], book[3], book[4], book[5], book[6]))
      
                
def search_remarks(search_entry, returned_books_frame, tree):
        search = search_entry.get().strip()
        returned_books_frame.focus()
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT
                    returned_books.returned_bookID,
                    user.user_school_id,
                    CONCAT(user.last_name, ', ', user.first_name, ' ', user.middle_initial) AS fullname,
                    books.title,
                    books.accession_no,
                    returned_books.book_condition,
                    returned_books.remarks
                FROM
                    returned_books
                    INNER JOIN user ON returned_books.userID = user.userID
                    INNER JOIN books ON returned_books.bookID = books.bookID
                WHERE
                    (returned_books.remarks <> '' OR returned_books.book_condition = 'Bad')
                    AND (books.title LIKE %s
                        OR CONCAT(user.last_name, ', ', user.first_name) LIKE %s
                        OR books.accession_no LIKE %s
                        OR user.user_school_id LIKE %s)
                ORDER BY
                    returned_books.returned_bookID DESC;

            """
            values = ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%')
            cursor.execute(query, values)
            books = cursor.fetchall()
            conn.close()


            # Clear existing items in the Treeview
            tree.delete(*tree.get_children())

            for book in books:
                tree.insert("", "end", values=(book[1], book[2],book[3], book[4], book[5], book[6]))
                
                
def show_reports(treeview):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports ORDER BY reportID DESC")
            books = cursor.fetchall()
            conn.close()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

           
            for book in books:
                # Check if the date is already a string
                if isinstance(book[5], str) or isinstance(book[1], str) or isinstance(book[2], str):
                    date_issued = datetime.strptime(book[5], "%Y-%m-%d %H:%M:%S")
                    from_date = datetime.strptime(book[1], "%B %d, %Y")
                    to_date = datetime.strptime(book[2], "%B %d, %Y")
                else:
                    date_issued = book[5]
                    from_date = book[1]
                    to_date = book[2]
                    
                # Format the date
                formatted_date = date_issued.strftime("%b. %d, %Y %I:%M %p")
                formatted_date2 = from_date.strftime("%B %d, %Y")
                formatted_date3 = to_date.strftime("%B %d, %Y")
                
                treeview.insert("", "end", values=(formatted_date2, formatted_date3, book[3], book[4], formatted_date))