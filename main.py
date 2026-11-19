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
        self.is_dark = False

        self.length = tk.IntVar(value=16)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#ffffff", foreground="#172033", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 21, "bold"), foreground="#172033")
        self.style.configure("Muted.TLabel", foreground="#687386", font=("Segoe UI", 10))
        self.style.configure("TCheckbutton", background="#ffffff", foreground="#283449", font=("Segoe UI", 10))
        self.style.map("TCheckbutton", background=[("active", "#ffffff")])
        self.style.configure(
            "Generate.TButton",
            background="#4263eb",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
            padding=(12, 11),
            borderwidth=0,
        )
        self.style.map("Copy.TButton", background=[("active", "#e0e7ff")])

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

        #change theme = lightmode / darkmode
        self.theme_button = ttk.Button(
            outer,
            text="Switch to dark mode",
            style="Copy.TButton",
            command=self.change_theme,
        )
        self.theme_button.pack(fill="x", pady=(10, 0))

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

    def change_theme(self) -> None:
        self.is_dark = not self.is_dark
        if self.is_dark:
            window_bg = "#111827"
            surface = "#1f2937"
            foreground = "#f9fafb"
            muted = "#aab4c3"
            field_bg = "#111827"
            copy_bg = "#374151"
            copy_active = "#4b5563"
        else:
            window_bg = "#f3f5f9"
            surface = "#ffffff"
            foreground = "#172033"
            muted = "#687386"
            field_bg = "#ffffff"
            copy_bg = "#ffffff"
            copy_active = "#e0e7ff"

        self.root.configure(bg=window_bg)
        self.style.configure("TFrame", background=surface)
        self.style.configure("TLabel", background=surface, foreground=foreground)
        self.style.configure("Title.TLabel", foreground=foreground)
        self.style.configure("Muted.TLabel", foreground=muted)
        self.style.configure("TCheckbutton", background=surface, foreground=foreground)
        self.style.map("TCheckbutton", background=[("active", surface)])
        self.style.configure("TEntry", fieldbackground=field_bg, foreground=foreground)
        self.style.configure("TSpinbox", fieldbackground=field_bg, foreground=foreground)
        self.style.configure("Copy.TButton", background=copy_bg, foreground=foreground)
        self.style.map("Copy.TButton", background=[("active", copy_active)])
        self.theme_button.configure(
            text="Switch to light mode" if self.is_dark else "Switch to dark mode"
        )

def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()