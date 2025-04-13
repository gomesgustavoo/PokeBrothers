# user_crud_customtkinter.py
"""
User Management (CRUD) GUI using customtkinter and SQLite.

Requirements
------------
pip install customtkinter

Usage
-----
python user_crud_customtkinter.py
"""

import customtkinter as ctk
import sqlite3
from tkinter import messagebox

DB_NAME = "users.db"


def init_db():
    """Create the users table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name  TEXT NOT NULL,
            email      TEXT UNIQUE NOT NULL,
            username   TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# ---------- Data‑access helpers ---------- #

def add_user(fn: str, ln: str, email: str, uname: str, pwd: str):
    """Insert a new user; returns (success: bool, message: str)."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users(first_name, last_name, email, username, password)
                   VALUES (?,?,?,?,?)""",
            (fn, ln, email, uname, pwd),
        )
        conn.commit()
        return True, "User added successfully."
    except sqlite3.IntegrityError as err:
        return False, str(err)
    finally:
        conn.close()


def get_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_user(uid: int, fn: str, ln: str, email: str, uname: str, pwd: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """UPDATE users
               SET first_name=?, last_name=?, email=?, username=?, password=?
             WHERE id=?""",
        (fn, ln, email, uname, pwd, uid),
    )
    conn.commit()
    conn.close()


def delete_user(uid: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
    conn.close()


# ---------- UI ---------- #
class UserApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("User Management")
        self.geometry("900x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # form variables
        self.record_id = None
        self.var_fn = ctk.StringVar()
        self.var_ln = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_uname = ctk.StringVar()
        self.var_pwd = ctk.StringVar()

        self._build_layout()
        self.populate_users()

    # ----- layout helpers ----- #
    def _build_layout(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        # --- form --- #
        fields = [
            ("First Name", self.var_fn),
            ("Last Name", self.var_ln),
            ("Email", self.var_email),
            ("Username", self.var_uname),
            ("Password", self.var_pwd),
        ]

        for idx, (label, var) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=idx, column=0, pady=6, padx=(10, 2), sticky="e")
            ctk.CTkEntry(form_frame, textvariable=var, width=180).grid(row=idx, column=1, pady=6, padx=(2, 10))

        # --- buttons --- #
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15, 5))

        ctk.CTkButton(btn_frame, text="Add", width=80, command=self.add_user).grid(row=0, column=0, padx=4)
        ctk.CTkButton(btn_frame, text="Update", width=80, command=self.update_user).grid(row=0, column=1, padx=4)
        ctk.CTkButton(btn_frame, text="Delete", width=80, command=self.delete_user).grid(row=0, column=2, padx=4)
        ctk.CTkButton(btn_frame, text="Clear", width=80, command=self.clear_form).grid(row=0, column=3, padx=4)

        # --- user list --- #
        self.user_list = ctk.CTkScrollableFrame(list_frame, corner_radius=12)
        self.user_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # ----- CRUD operations ----- #
    def populate_users(self):
        for widget in self.user_list.winfo_children():
            widget.destroy()

        for row in get_users():
            uid, fn, ln, email, uname, _ = row
            label_text = f"{uid:>3} | {fn} {ln} | {email} | {uname}"
            item_btn = ctk.CTkButton(
                self.user_list,
                text=label_text,
                anchor="w",
                fg_color="transparent",
                hover_color="#eeeeee",
                text_color="#333333",
                command=lambda r=row: self.load_user(r),
            )
            item_btn.pack(fill="x", pady=1, padx=2)

    def load_user(self, row):
        uid, fn, ln, email, uname, pwd = row
        self.record_id = uid
        self.var_fn.set(fn)
        self.var_ln.set(ln)
        self.var_email.set(email)
        self.var_uname.set(uname)
        self.var_pwd.set(pwd)

    def add_user(self):
        ok, msg = add_user(
            self.var_fn.get(),
            self.var_ln.get(),
            self.var_email.get(),
            self.var_uname.get(),
            self.var_pwd.get(),
        )
        messagebox.showinfo("Add User", msg)
        if ok:
            self.clear_form()
            self.populate_users()

    def update_user(self):
        if self.record_id is None:
            messagebox.showwarning("Update", "Select a user first.")
            return
        update_user(
            self.record_id,
            self.var_fn.get(),
            self.var_ln.get(),
            self.var_email.get(),
            self.var_uname.get(),
            self.var_pwd.get(),
        )
        messagebox.showinfo("Update", "User updated.")
        self.clear_form()
        self.populate_users()

    def delete_user(self):
        if self.record_id is None:
            messagebox.showwarning("Delete", "Select a user first.")
            return
        delete_user(self.record_id)
        messagebox.showinfo("Delete", "User deleted.")
        self.clear_form()
        self.populate_users()

    def clear_form(self):
        self.record_id = None
        for var in (self.var_fn, self.var_ln, self.var_email, self.var_uname, self.var_pwd):
            var.set("")
        self.focus()


if __name__ == "__main__":
    init_db()
    app = UserApp()
    app.mainloop()