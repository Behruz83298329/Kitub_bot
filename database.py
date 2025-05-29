import sqlite3

def init_db(): 
 conn = sqlite3.connect("books.db") 
 cur = conn.cursor() 
 cur.execute(""" 
CREATE TABLE IF NOT EXISTS books (
 user_id INTEGER, 
            file_name TEXT, 
            book_name TEXT, 
            author_name TEXT, 
            private INTEGER DEFAULT 0 ,
            tgid INTEGER
            ) 
            """)
 conn.commit() 
 conn.close()

def save_book(user_id, file_name, book_name, author_name, tgid): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("INSERT INTO books (user_id, file_name, book_name, author_name, tgid) VALUES (?, ?, ?, ?, ?)", 
    (user_id, file_name, book_name, author_name, tgid)) 
    conn.commit() 
    conn.close()

def get_user_books(user_id): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("SELECT file_name, book_name, author_name FROM books WHERE user_id = ?", (user_id,)) 
    results = cur.fetchall() 
    conn.close() 
    return results

def set_privacy(user_id, privacy_status): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("UPDATE books SET private = ? WHERE user_id = ?", 
    (privacy_status, user_id)) 
    conn.commit() 
    conn.close()

def search_books_by_author(author_name): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("SELECT file_name, book_name, author_name FROM books WHERE author_name LIKE ? AND private = 0", (f"%{author_name}%",)) 
    results = cur.fetchall() 
    conn.close() 
    return results

def update_book_name(old_name, new_name): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("UPDATE books SET book_name = ? WHERE book_name = ?", (new_name, old_name)) 
    conn.commit() 
    conn.close()

def update_book_author(book_name, new_author): 
    conn = sqlite3.connect("books.db") 
    cur = conn.cursor() 
    cur.execute("UPDATE books SET author_name = ? WHERE book_name = ?", (new_author, book_name)) 
    conn.commit() 
    conn.close()

def delete_book_by_name(book_name, tgid): 
    conn = sqlite3.connect("books.db") 
    print(book_name, tgid)
    cur = conn.cursor() 
    cur.execute("DELETE FROM books WHERE book_name = ? AND user_id = ?", (book_name, tgid)) 
    conn.commit() 
    conn.close()
    print("Fynksiya ishladi")
    