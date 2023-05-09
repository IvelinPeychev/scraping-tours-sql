import sqlite3


# ESTABLISH CONNECTION
connection = sqlite3.connect('data.db')
# Creating object that can execute SQL queries
cursor = connection.cursor()


# QUERY DATA

# cursor will be a list of tuples that will contain the result
cursor.execute('SELECT * FROM events WHERE date = "2088.10.15" OR date = "2099.10.10"')
# fetching all rows with results
rows = cursor.fetchall()
print(rows)

# Insert new (multiple) rows
new_rows = [('Cats', 'Cats City', '2088.10.17'),
            ('Hens', 'Hens City', '2088.10.17')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)

# Save the results in the database, same as pressing WRITE CHANGES
connection.commit()
