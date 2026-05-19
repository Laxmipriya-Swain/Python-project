import re
import tkinter as tk
from tkinter import ttk

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def login(email: str, password: str) -> dict:
    """Simulate an API login request.

    Replace this stub with a real HTTP request to your authentication backend.
    """
    email = (email or "").strip()
    password = password or ""

    if not email or not password:
        return {"success": False, "message": "Email and password are required."}

    if not EMAIL_REGEX.match(email):
        return {"success": False, "message": "Enter a valid email address."}

    # Mock response: replace with actual API logic.
    if email.lower().endswith("@gmail.com") and len(password) >= 6:
        return {
            "success": True,
            "token": "fake-jwt-token",
            "message": "Login successful.",
        }

    return {
        "success": False,
        "message": "This demo accepts only valid Gmail addresses with a password of at least 6 characters.",
    }


class LoginPage:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("420x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f7")

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.is_loading = False

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#f4f4f7", foreground="#222222", font=("Segoe UI", 16, "bold"))
        style.configure("Field.TLabel", background="#ffffff", foreground="#333333", font=("Segoe UI", 10))
        style.configure("Error.TLabel", background="#ffffff", foreground="#d93025", font=("Segoe UI", 9, "bold"))
        style.configure("Status.TLabel", background="#f4f4f7", foreground="#1a73e8", font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def create_widgets(self) -> None:
        container = ttk.Frame(self.root, style="Card.TFrame", padding=(20, 20, 20, 20))
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = ttk.Label(container, text="Sign in to your account", style="Title.TLabel")
        title.pack(anchor="w", pady=(0, 16))

        email_label = ttk.Label(container, text="Email", style="Field.TLabel")
        email_label.pack(anchor="w", pady=(0, 6))
        self.email_entry = tk.Entry(
            container,
            textvariable=self.email_var,
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#4d90fe",
            width=36,
        )
        self.email_entry.pack(fill="x", pady=(0, 12))

        password_label = ttk.Label(container, text="Password", style="Field.TLabel")
        password_label.pack(anchor="w", pady=(0, 6))
        self.password_entry = tk.Entry(
            container,
            textvariable=self.password_var,
            show="*",
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#4d90fe",
            width=36,
        )
        self.password_entry.pack(fill="x", pady=(0, 12))

        self.error_label = ttk.Label(container, textvariable=self.error_var, style="Error.TLabel")
        self.error_label.pack(anchor="w", pady=(0, 10))

        self.login_button = tk.Button(
            container,
            text="Login",
            command=self.on_submit,
            font=("Segoe UI", 10, "bold"),
            bg="#1a73e8",
            fg="#ffffff",
            activebackground="#1669c1",
            activeforeground="#ffffff",
            bd=0,
            relief="raised",
            width=34,
            cursor="hand2",
        )
        self.login_button.pack(pady=(0, 14))

        self.status_label = ttk.Label(container, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor="w")

    def set_loading(self, loading: bool) -> None:
        self.is_loading = loading
        state = "disabled" if loading else "normal"
        self.login_button.config(state=state)
        self.email_entry.config(state=state)
        self.password_entry.config(state=state)
        self.status_var.set("Logging in..." if loading else "")

    def clear_error(self) -> None:
        self.error_var.set("")
        self.email_entry.config(highlightbackground="#cccccc")
        self.password_entry.config(highlightbackground="#cccccc")

    def show_error(self, message: str) -> None:
        self.error_var.set(message)
        self.status_var.set("")

    def validate_inputs(self) -> bool:
        email = self.email_var.get().strip()
        password = self.password_var.get()

        if not email or not password:
            self.show_error("Email and password are required.")
            if not email:
                self.email_entry.config(highlightbackground="#d93025")
            if not password:
                self.password_entry.config(highlightbackground="#d93025")
            return False

        if not EMAIL_REGEX.match(email):
            self.show_error("Please enter a valid email address.")
            self.email_entry.config(highlightbackground="#d93025")
            return False

        return True

    def on_submit(self) -> None:
        if self.is_loading:
            return

        self.clear_error()

        if not self.validate_inputs():
            return

        email = self.email_var.get().strip()
        password = self.password_var.get()
        self.set_loading(True)
        self.root.after(800, lambda: self.perform_login(email, password))

    def perform_login(self, email: str, password: str) -> None:
        result = login(email, password)
        self.set_loading(False)

        if result.get("success"):
            self.status_var.set(result.get("message", "Login successful."))
            self.error_var.set("")
        else:
            self.show_error(result.get("message", "Login failed."))


if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
