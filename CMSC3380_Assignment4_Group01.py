"""
CMSC3380_Assignment4_Group01.py
Group 01 - GUI Book Manager
Members: [Your Names Here]
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATABASE SETUP ---
conn = sqlite3.connect("CMSC3380_Assignment4_Group01.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')
conn.commit()

# --- FUNCTIONS ---
def add_book():
    try:
        cursor.execute("INSERT INTO books (id, title, authors, category) VALUES (?, ?, ?, ?)",
                       (int(entry_id.get()), entry_title.get(), entry_authors.get(), category_var.get()))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "ID already exists.")
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a number.")

def update_book():
    try:
        cursor.execute("UPDATE books SET title=?, authors=?, category=? WHERE id=?",
                       (entry_title.get(), entry_authors.get(), category_var.get(), int(entry_id.get())))
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a number.")

def delete_book():
    try:
        cursor.execute("DELETE FROM books WHERE id=?", (int(entry_id.get()),))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a number.")

def list_books():
    list_window = tk.Toplevel(root)
    list_window.title("All Books")
    tree = ttk.Treeview(list_window, columns=("ID", "Title", "Authors", "Category"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Authors", text="Authors")
    tree.heading("Category", text="Category")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Book Manager")

# Labels and Entries
tk.Label(root, text="ID:").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Title:").grid(row=1, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=1, column=1)

tk.Label(root, text="Authors:").grid(row=2, column=0)
entry_authors = tk.Entry(root)
entry_authors.grid(row=2, column=1)

# Radio Buttons for Category
category_var = tk.StringVar()
tk.Label(root, text="Category:").grid(row=3, column=0)
tk.Radiobutton(root, text="Gothic Fiction", variable=category_var, value="Gothic Fiction").grid(row=3, column=1, sticky='w')
tk.Radiobutton(root, text="Science Fiction", variable=category_var, value="Science Fiction").grid(row=4, column=1, sticky='w')
tk.Radiobutton(root, text="Tragedy", variable=category_var, value="Tragedy").grid(row=5, column=1, sticky='w')
tk.Radiobutton(root, text="Fiction", variable=category_var, value="Fiction").grid(row=6, column=1, sticky='w')

# Buttons
tk.Button(root, text="Add Book", command=add_book).grid(row=7, column=0)
tk.Button(root, text="Update Book", command=update_book).grid(row=7, column=1)
tk.Button(root, text="Delete Book", command=delete_book).grid(row=8, column=0)
tk.Button(root, text="List All Books", command=list_books).grid(row=8, column=1)

root.mainloop()
conn.close()
