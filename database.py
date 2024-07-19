import sqlite3

# Constants for SQL queries
CREATE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    qty INTEGER NOT NULL
)
'''
INSERT_BOOK_QUERY = 'INSERT INTO book (title, author, qty) VALUES (?, ?, ?)'
INSERT_INITIAL_BOOKS_QUERY = 'INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)'
UPDATE_BOOK_TITLE_QUERY = 'UPDATE book SET title = ? WHERE id = ?'
UPDATE_BOOK_AUTHOR_QUERY = 'UPDATE book SET author = ? WHERE id = ?'
UPDATE_BOOK_QTY_QUERY = 'UPDATE book SET qty = ? WHERE id = ?'
DELETE_BOOK_QUERY = 'DELETE FROM book WHERE id = ?'
SEARCH_BOOKS_QUERY = 'SELECT * FROM book WHERE title LIKE ? OR author LIKE ?'

# Connect to SQLite database (it will create it if it doesn't exist)
conn = sqlite3.connect('ebookstore.db')
c = conn.cursor()

# Create the book table if it doesn't exist
c.execute(CREATE_TABLE_QUERY)

# Function to populate the table with initial data
def populate_initial_data():
    initial_books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    # Insert initial data
    c.executemany(INSERT_INITIAL_BOOKS_QUERY, initial_books)
    conn.commit()

# Function to add a new book
def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    qty = int(input("Enter the quantity: "))
    c.execute(INSERT_BOOK_QUERY, (title, author, qty))
    conn.commit()
    print("Book added successfully!")

# Function to update a book's information
def update_book():
    id = int(input("Enter the book ID to update: "))
    title = input("Enter the new title (or press Enter to keep current): ")
    author = input("Enter the new author (or press Enter to keep current): ")
    qty = input("Enter the new quantity (or press Enter to keep current): ")
    if title:
        c.execute(UPDATE_BOOK_TITLE_QUERY, (title, id))
    if author:
        c.execute(UPDATE_BOOK_AUTHOR_QUERY, (author, id))
    if qty:
        c.execute(UPDATE_BOOK_QTY_QUERY, (qty, id))
    conn.commit()
    print("Book updated successfully!")

# Function to delete a book
def delete_book():
    id = int(input("Enter the book ID to delete: "))
    c.execute(DELETE_BOOK_QUERY, (id,))
    conn.commit()
    print("Book deleted successfully!")

# Function to search for a book
def search_books():
    keyword = input("Enter a keyword to search for (title/author): ")
    c.execute(SEARCH_BOOKS_QUERY, ('%' + keyword + '%', '%' + keyword + '%'))
    results = c.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")
    else:
        print("No books found.")

# Function to display the menu
def display_menu():
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

# Function to handle user's menu choice
def handle_choice(choice):
    if choice == '1':
        add_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        print("Goodbye!")
        return False
    else:
        print("Invalid choice! Please select a valid option.")
    return True

# Main program loop
def main():
    populate_initial_data()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if not handle_choice(choice):
            break

if __name__ == "__main__":
    main()

# Close the connection when done
conn.close()
