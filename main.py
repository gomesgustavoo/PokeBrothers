import uuid
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from services.pokeapi_service import import_card_to_db
from pages.navbar import NavBar
from pages.profile import ProfilePage
from pages.search_cards import SearchCardsPage

DB_NAME = "colecionadores.db"


# ———————— DATA LAYER ————————
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS colecionadores (
            id    TEXT PRIMARY KEY,
            nome  TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_colecionador(nome, email, senha):
    novo_id = str(uuid.uuid4())
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO colecionadores(id,nome,email,senha) VALUES (?,?,?,?)",
            (novo_id, nome, email, senha)
        )
        conn.commit()
        return True, "Colecionador registrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este email já está cadastrado."
    finally:
        conn.close()


def check_login(email, senha):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nome FROM colecionadores WHERE email=? AND senha=?",
        (email, senha)
    )
    row = cur.fetchone()
    conn.close()
    return (True, row) if row else (False, None)


# ———————— APPLICATION ————————
class UserApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PokeBrothers")
        self.geometry("900x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # variáveis de estado / formulário
        self.var_email = ctk.StringVar()
        self.var_pwd = ctk.StringVar()
        self.var_name = ctk.StringVar()
        self.var_pwd_confirm = ctk.StringVar()

        self.record_id = None
        self.current_name = ""
        self.current_email = ""

        init_db()
        self._build_login_frame()
        self._build_register_frame()
        self.register_frame.place_forget()
        self.show_login()

    # —— Login & Registro ——
    def _build_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, corner_radius=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.login_frame, text="Login", font=ctk.CTkFont(size=18)) \
            .grid(row=0, column=0, columnspan=2, pady=(20, 10))
        ctk.CTkLabel(self.login_frame, text="Email:") \
            .grid(row=1, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.login_frame, width=200, textvariable=self.var_email) \
            .grid(row=1, column=1, pady=5)
        ctk.CTkLabel(self.login_frame, text="Senha:") \
            .grid(row=2, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.login_frame, width=200, show="*", textvariable=self.var_pwd) \
            .grid(row=2, column=1, pady=5)

        ctk.CTkButton(
            self.login_frame, text="Entrar", width=250, command=self._on_login
        ).grid(row=3, column=0, columnspan=2, pady=(15, 5))

        rodape = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        rodape.grid(row=4, column=0, columnspan=2, pady=(10, 20))
        ctk.CTkLabel(rodape, text="Não registrado?") \
            .grid(row=0, column=0)
        ctk.CTkButton(
            rodape, text="Registrar", width=80, command=self.show_register
        ).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(self.login_frame, text="Esqueceu sua senha?") \
            .grid(row=5, column=0, columnspan=2, pady=(5,10))

    def _build_register_frame(self):
        self.register_frame = ctk.CTkFrame(self, corner_radius=20)
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.register_frame, text="Registro de Colecionador",
            font=ctk.CTkFont(size=18)
        ).grid(row=0, column=0, columnspan=2, pady=(20,10))
        ctk.CTkLabel(self.register_frame, text="Nome:") \
            .grid(row=1, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.register_frame, width=200, textvariable=self.var_name) \
            .grid(row=1, column=1, pady=5)
        ctk.CTkLabel(self.register_frame, text="Email:") \
            .grid(row=2, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.register_frame, width=200, textvariable=self.var_email) \
            .grid(row=2, column=1, pady=5)
        ctk.CTkLabel(self.register_frame, text="Senha:") \
            .grid(row=3, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.register_frame, width=200, show="*", textvariable=self.var_pwd) \
            .grid(row=3, column=1, pady=5)
        ctk.CTkLabel(self.register_frame, text="Confirme Senha:") \
            .grid(row=4, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self.register_frame, width=200, show="*", textvariable=self.var_pwd_confirm) \
            .grid(row=4, column=1, pady=5)

        ctk.CTkButton(
            self.register_frame, text="Registre-se", width=250,
            command=self._on_register
        ).grid(row=5, column=0, columnspan=2, pady=(15, 5))

        rodape = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        rodape.grid(row=6, column=0, columnspan=2, pady=(10,20))
        ctk.CTkLabel(rodape, text="Já possui conta?") \
            .grid(row=0, column=0)
        ctk.CTkButton(
            rodape, text="Login", width=80, command=self.show_login
        ).grid(row=0, column=1, padx=5)

    def show_login(self):
        self.register_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_register(self):
        self.login_frame.place_forget()
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

    def _on_login(self):
        ok, row = check_login(self.var_email.get().strip(), self.var_pwd.get().strip())
        if not ok:
            messagebox.showerror("Login", "Credenciais incorretas.")
            return
        self.record_id, self.current_name = row
        self.current_email = self.var_email.get().strip()
        self.login_frame.place_forget()
        self.register_frame.place_forget()
        self._build_main_ui()

    def _on_register(self):
        if self.var_pwd.get().strip() != self.var_pwd_confirm.get().strip():
            messagebox.showwarning("Cadastro", "As senhas não coincidem.")
            return
        ok, msg = add_colecionador(
            self.var_name.get().strip(),
            self.var_email.get().strip(),
            self.var_pwd.get().strip()
        )
        messagebox.showinfo("Cadastro", msg)
        if ok:
            self.var_name.set("")
            self.var_email.set("")
            self.var_pwd.set("")
            self.var_pwd_confirm.set("")
            self.show_login()

    # —— NAVBAR & PAGES ——
    def _build_main_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        commands = [
            ("Perfil", self.show_profile),
            ("Pesquisar cartas", self.show_search_cards),
            ("Inventário", lambda: None),
            ("Lista de Desejos", lambda: None),
            ("Simular Troca", lambda: None),
            ("Histórico de Troca", lambda: None)
        ]
        self.nav_frame = NavBar(self, commands)
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.content_frame = ctk.CTkFrame(self, corner_radius=12)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_profile()

    def _show_page(self, page_class, *args):
        for w in self.content_frame.winfo_children():
            w.destroy()
        page = page_class(self.content_frame, *args)
        page.pack(fill="both", expand=True)

    def show_profile(self):
        self._show_page(ProfilePage, self.current_name, self.current_email)

    def show_search_cards(self):
        self._show_page(SearchCardsPage)


if __name__ == "__main__":
    init_db()
    app = UserApp()
    app.mainloop()
