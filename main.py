import uuid
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from pages.navbar import NavBar
from pages.profile import ProfilePage
from pages.search_cards import SearchCardsPage
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.Inventario import InventarioPage
from pages.simulacao import SimulacaoTrocaPage
from models.Colecionador import Colecionador
from pages.lista_desejos import ListaDesejosPage

DB_NAME = "colecionadores.db"
INVENTARIO_DB = "inventario.db"

# ———————— DATA LAYER ————————
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS colecionadores (
            id    TEXT PRIMARY KEY,
            nome  TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
        """
    )
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
        if 'conn' in locals() and conn:
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


def init_inventario_db():
    conn = sqlite3.connect(INVENTARIO_DB)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventario (
            id TEXT PRIMARY KEY,
            colecionador_id TEXT NOT NULL,
            carta_id TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def init_lista_desejos_db():
    conn = sqlite3.connect(INVENTARIO_DB)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lista_desejos (
            id TEXT PRIMARY KEY,
            colecionador_id TEXT NOT NULL,
            carta_id TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# ———————— APPLICATION ————————
class UserApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PokeBrothers")
        self.geometry("1300x800")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.record_id = None
        self.current_name = ""
        self.current_email = ""
        self.colecionador = Colecionador(
            nome=self.current_name,
            email=self.current_email,
            senha="",  # Senha será definida no login/cadastro
            id=self.record_id,
            inventario=[]
        )

        init_db()

        # Frames de login e cadastro
        self.login_frame = LoginPage(self, on_login_success=self._on_login, show_register_callback=self.show_register)
        self.register_frame = RegisterPage(self, on_register_callback=self._on_register, show_login_callback=self.show_login)
        self.show_login()

    def show_login(self):
        self.register_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame.clear_fields()

    def show_register(self):
        self.login_frame.place_forget()
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.register_frame.clear_fields()

    def _on_login(self, user_id):
        self.record_id = user_id
        # Carrega nome e email do usuário
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT nome, email FROM colecionadores WHERE id=?", (self.record_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Login", "Erro ao carregar dados do usuário.")
            return
        self.current_name, self.current_email = row
        self.colecionador = Colecionador.from_db(self.record_id)
        self.login_frame.place_forget()
        self._build_main_ui()

    def _on_register(self, name, email, password):
        ok, msg = add_colecionador(name, email, password)
        messagebox.showinfo("Cadastro", msg)
        if ok:
            self.show_login()

    def logout(self):
        if hasattr(self, 'nav_frame'):
            self.nav_frame.destroy()
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        self.record_id = None
        self.current_name = ""
        self.current_email = ""
        self.colecionador = None
        self.show_login()

    def _on_profile_update(self, new_name: str):
        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("UPDATE colecionadores SET nome=? WHERE id=?", (new_name, self.record_id))
            conn.commit()
            conn.close()
            self.current_name = new_name
            if self.colecionador:
                self.colecionador.set_nome(new_name)
            messagebox.showinfo("Perfil", "Nome atualizado com sucesso.")
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Perfil", f"Erro ao atualizar nome: {e}")

    def _on_delete_account(self):
        resp = messagebox.askyesno("Excluir Conta", "Tem certeza que deseja excluir sua conta?")
        if not resp:
            return
        try:
            # Remove inventário e lista de desejos do usuário
            conn_inv = sqlite3.connect(INVENTARIO_DB)
            cur_inv = conn_inv.cursor()
            cur_inv.execute("DELETE FROM inventario WHERE colecionador_id=?", (self.record_id,))
            cur_inv.execute("DELETE FROM lista_desejos WHERE colecionador_id=?", (self.record_id,))
            conn_inv.commit()
            conn_inv.close()

            # Remove o colecionador do banco principal
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("DELETE FROM colecionadores WHERE id=?", (self.record_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Conta Excluída", "Sua conta foi excluída com sucesso.")
            self.logout()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir conta: {e}")

    def _build_main_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        commands = [
            ("Perfil", self.show_profile),
            ("Pesquisar cartas", self.show_search_cards),
            ("Inventário", self.show_inventario),
            ("Lista de Desejos", self.show_desejos),
            ("Simular Troca", self.show_simulacao),
            ("Sair", self.logout)
        ]
        self.nav_frame = NavBar(self, commands)
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.content_frame = ctk.CTkFrame(self, corner_radius=12)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_profile()

    def _show_page(self, page_class, *args):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        page = page_class(self.content_frame, *args)
        page.pack(fill="both", expand=True)

    def show_profile(self):
        self._show_page(ProfilePage, self.record_id, self.current_name, self.current_email, self._on_profile_update, self._on_delete_account, self.logout)

    def show_inventario(self):
        self._show_page(InventarioPage, self.colecionador)

    def show_search_cards(self):
        self._show_page(SearchCardsPage)

    def show_simulacao(self):
        self._show_page(SimulacaoTrocaPage, self.colecionador)

    def show_desejos(self):
        self._show_page(ListaDesejosPage, self.colecionador)


if __name__ == "__main__":
    init_db()
    init_inventario_db()
    init_lista_desejos_db()
    app = UserApp()
    app.mainloop()

