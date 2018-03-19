"""
file: sqlite_play.py

A quick test of sqlite using python following direction on python manual.

author: Xueman Mou
date: 2018/3/9
version: 1.0.0
modified: 2018/3/9 8:57:00 GMT+800

development env: python 3.6.3
dependencies: sqlite3
ref: https://docs.python.org/3/library/sqlite3.html
"""

# import sqlite3

# conn = sqlite3.connect('example.db')

# c = conn.cursor()

# Create Table
# c.execute('''CREATE TABLE IF NOT EXISTS stocks
# 			(date text, trans text, symbol text, qty real, price real)''')	

# Insert a row of data
# c.execute('''INSERT INTO stocks VALUES ('2016-1-1', 'BUY', 'RHAT', 100, 35.14)''')

# Save (commit) the changes
# conn.commit()

# NEVER do this!
# symbol = 'RHAT'
# c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# DO this instead
# t = ('RHAT',)
# c.execute('SELECT * FROM stocks WHERE symbol = ?', t)
# print(c.fetchone())

# Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

# for row in c.execute('SELECT * FROM stocks ORDER BY price'):
# 	print(row)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
# conn.close()

#######################################
# A minimal SQLite shell for experiments
# conn = sqlite3.connect(':memory')
# conn.isolation_level = None
# c = conn.cursor()

# buffer = ""

# print("Enter your SQL comands to execute in sqlite3.")
# print("Enter a blank line to exit.")

# while True:
# 	line = input()
# 	if line == "":
# 		break
# 	buffer += line
# 	if sqlite3.complete_statement(buffer):
# 		try:
# 			buffer = buffer.strip()
# 			cur.execute(buffer)

# 			if buffer.lstrip.upper().startswith("SELECT"):
# 				print(cur.fetchall())
# 		except sqlite3.ERROR as e:
# 			print("An error occurred:", e.args[0])

# 		buffer = ""
# conn.close()

#########################################
# A SQLite Connection's create_function
# import sqlite3
# import hashlib

# def md5sum(t):
# 	return hashlib.md5(t).hexdigest()

# con = sqlite3.connect(":memory:")
# con.create_function("md5", 1, md5sum)
# cur = con.cursor()
# cur.execute("select md5(?)", (b"foo",))
# print(cur.fetchone()[0])
