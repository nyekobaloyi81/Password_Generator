import secrets
import tkinter as tk
from tkinter import messagebox, ttk

CHARACTER_SETS = {
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "numbers": "0123456789",
    "symbols": "!@#$%^&*()-_=+[]{};:,.?/|~",
}

def generate_password(length: int) -> str:
    characters = "".join(CHARACTER_SETS.values())
    return "".join(secrets.choice(characters) for _ in range(length))


class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("480x590")
        self.root.minsize(440, 550)
        self.root.configure(bg="#f3f5f9")

        self.length = tk.IntVar(value=16)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#172033", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 21, "bold"), foreground="#172033")
        style.configure("Muted.TLabel", foreground="#687386", font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#ffffff", foreground="#283449", font=("Segoe UI", 10))
        style.map("TCheckbutton", background=[("active", "#ffffff")])
        style.configure(
            "Generate.TButton",
            background="#4263eb",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
            padding=(12, 11),
            borderwidth=0,
        )
        style.map("Copy.TButton", background=[("active", "#e0e7ff")])

        outer = ttk.Frame(root, padding=24)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        ttk.Label(outer, text="Password Generator", style="Title.TLabel").pack(anchor="w", pady=(2, 4))
        ttk.Label(outer, text="Create a strong password in seconds.", style="Muted.TLabel").pack(anchor="w")
        length_row = ttk.Frame(outer)
        length_row.pack(fill="x", pady=(20, 0))
        ttk.Label(length_row, text="Password length").pack(side="left")
        ttk.Spinbox(length_row, from_=4, to=24, textvariable=self.length, width=8).pack(side="right")

        #Password Box
        password_box = ttk.Frame(outer, padding=16)
        password_box.pack(fill="x", pady=(26, 22))
        ttk.Label(password_box, text="YOUR PASSWORD", style="Muted.TLabel").pack(anchor="w", pady=(0, 9))
        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_box,
            textvariable=self.password,
            state="readonly",
            font=("Consolas", 14),
            justify="center",
        )
        self.password_entry.pack(fill="x", ipady=10)

        #Generate Password button
        ttk.Button(
            outer,
            text="Generate password",
            style="Generate.TButton",
            command=self.generate,
        ).pack(fill="x")

        #Copy Password button
        ttk.Button(
            password_box, 
            text="Copy password", 
            style="Copy.TButton", 
            command=self.copy_password,
            ).pack(fill="x")

        self.status = ttk.Label(outer, text="Your password is generated securely on this device.", style="Muted.TLabel")
        self.status.pack(anchor="center", pady=(12, 0))

        self.generate()

    def generate(self) -> None:
        try:
            user_length = self.length.get()
        except tk.TclError:
            messagebox.showerror("Invalid length", "Enter a whole number between 4 and 24.")
            return

        if not 4 <= user_length <= 24:
            messagebox.showerror("Invalid length", "Password length must be between 4 and 24.")
            return

        self.password.set(generate_password(user_length))

    def copy_password(self) -> None:
        value = self.password.get()
        if not value:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.status.configure(text="Password copied to clipboard.")

def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()