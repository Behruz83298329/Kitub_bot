import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("ALTER TABLE books ADD COLUMN tgid TEXT")

conn.commit()
conn.close()

print("tgid ustuni qo‘shildi.")