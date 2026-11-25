import tkinter as tk
from tkinter import messagebox, ttk

from password import estimate_entropy, generate_password


class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("520x660")
        self.root.minsize(460, 600)
        self.is_dark = False
        self.clipboard_clear_job = None
        self.copied_password = ""

        self.length = tk.IntVar(value=16)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        outer = ttk.Frame(root, padding=30, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer, style="App.TFrame")
        header.pack(fill="x", pady=(0, 28))
        self.theme_button = ttk.Button(
            header,
            text="Dark mode",
            style="Theme.TButton",
            command=self.change_theme,
        )
        self.theme_button.pack(side="right")

        ttk.Label(outer, text="Password generator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Create a strong, unique password in seconds.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(5, 24))

        password_box = ttk.Frame(
            outer,
            padding=22,
            style="Card.TFrame",
            relief="solid",
            borderwidth=1,
        )
        password_box.pack(fill="x", pady=(0, 18))

        length_row = ttk.Frame(password_box, style="Card.TFrame")
        length_row.pack(fill="x")
        ttk.Label(length_row, text="Password length", style="FieldLabel.TLabel").pack(side="left")
        ttk.Spinbox(
            length_row,
            from_=4,
            to=128,
            textvariable=self.length,
            width=7,
            justify="center",
            style="Field.TSpinbox",
        ).pack(side="right")

        ttk.Separator(password_box).pack(fill="x", pady=20)
        ttk.Label(password_box, text="Character types", style="Eyebrow.TLabel").pack(
            anchor="w",
            pady=(0, 8),
        )
        category_row = ttk.Frame(password_box, style="Card.TFrame")
        category_row.pack(fill="x", pady=(0, 10))
        ttk.Checkbutton(
            category_row,
            text="A-Z",
            variable=self.include_uppercase,
            style="Category.TCheckbutton",
        ).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(
            category_row,
            text="a-z",
            variable=self.include_lowercase,
            style="Category.TCheckbutton",
        ).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(
            category_row,
            text="0-9",
            variable=self.include_numbers,
            style="Category.TCheckbutton",
        ).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(
            category_row,
            text="Symbols",
            variable=self.include_symbols,
            style="Category.TCheckbutton",
        ).pack(side="left")

        ttk.Label(password_box, text="Generated Password", style="Eyebrow.TLabel").pack(
            anchor="w",
            pady=(0, 10),
        )
        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_box,
            textvariable=self.password,
            state="readonly",
            font=("Consolas", 17),
            style="Password.TEntry",
        )
        self.password_entry.pack(fill="x", ipady=12)

        ttk.Button(
            outer,
            text="Generate new password",
            style="Generate.TButton",
            command=self.generate,
        ).pack(fill="x", ipady=3)

        ttk.Button(
            outer,
            text="Copy to clipboard",
            style="Copy.TButton",
            command=self.copy_password,
        ).pack(fill="x", pady=(10, 0))

        self.status = ttk.Label(
            outer,
            text="Generated locally. Nothing is stored.",
            style="Status.TLabel",
        )
        self.status.pack(anchor="center", pady=(24, 0))

        self._apply_theme()
        self.generate()
        self.root.bind("<Control-g>", self._generate_shortcut)
        self.root.bind("<Control-Shift-C>", self._copy_shortcut)

    def _generate_shortcut(self, event: tk.Event) -> str:
        del event
        self.generate()
        return "break"

    def _copy_shortcut(self, event: tk.Event) -> str:
        del event
        self.copy_password()
        return "break"

    def generate(self) -> None:
        try:
            user_length = self.length.get()
        except tk.TclError:
            messagebox.showerror("Invalid length", "Enter a whole number between 4 and 128.")
            return

        if not 4 <= user_length <= 128:
            messagebox.showerror("Invalid length", "Password length must be between 4 and 128.")
            return

        categories = []
        if self.include_lowercase.get():
            categories.append("lowercase")
        if self.include_uppercase.get():
            categories.append("uppercase")
        if self.include_numbers.get():
            categories.append("numbers")
        if self.include_symbols.get():
            categories.append("symbols")

        if not categories:
            messagebox.showerror("No character types", "Select at least one character type.")
            return
        if user_length < len(categories):
            messagebox.showerror(
                "Invalid length",
                f"Use at least {len(categories)} characters to include every selected type.",
            )
            return

        try:
            value = generate_password(user_length, categories)
        except ValueError as error:
            messagebox.showerror("Unable to generate password", str(error))
            return

        self.password.set(value)
        entropy = estimate_entropy(user_length, categories)
        self.status.configure(text=f"Generated locally. Estimated entropy: {entropy:.0f} bits.")

    def copy_password(self) -> None:
        value = self.password.get()
        if not value:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.copied_password = value
        self.status.configure(text="Password copied to clipboard.")
        if self.clipboard_clear_job is not None:
            self.root.after_cancel(self.clipboard_clear_job)
        self.clipboard_clear_job = self.root.after(60_000, self.clear_clipboard)

    def clear_clipboard(self) -> None:
        try:
            current = self.root.clipboard_get()
            if current == self.copied_password:
                self.root.clipboard_clear()
                self.status.configure(text="Password cleared from the clipboard.")
                self.copied_password = ""
        except tk.TclError:
            pass
        finally:
            self.clipboard_clear_job = None

    def change_theme(self) -> None:
        self.is_dark = not self.is_dark
        self._apply_theme()

    def _apply_theme(self) -> None:
        if self.is_dark:
            window_bg = "#111827"
            surface = "#1b2638"
            foreground = "#f9fafb"
            muted = "#a8b3c5"
            border = "#334155"
            field_bg = "#111827"
            field_muted = "#94a3b8"
            copy_bg = "#263449"
            copy_active = "#33445d"
            accent = "#818cf8"
            accent_active = "#6366f1"
        else:
            window_bg = "#f4f6fb"
            surface = "#ffffff"
            foreground = "#172033"
            muted = "#667085"
            border = "#e4e7ec"
            field_bg = "#f8fafc"
            field_muted = "#667085"
            copy_bg = "#eef2ff"
            copy_active = "#e0e7ff"
            accent = "#4f46e5"
            accent_active = "#4338ca"

        self.root.configure(bg=window_bg)
        self.style.configure("App.TFrame", background=window_bg)
        self.style.configure(
            "Card.TFrame",
            background=surface,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
        )
        self.style.configure("Title.TLabel", background=window_bg, foreground=foreground, font=("Segoe UI", 25, "bold"))
        self.style.configure("Subtitle.TLabel", background=window_bg, foreground=muted, font=("Segoe UI", 10))
        self.style.configure("Eyebrow.TLabel", background=surface, foreground=muted, font=("Segoe UI", 9, "bold"))
        self.style.configure("FieldLabel.TLabel", background=surface, foreground=foreground, font=("Segoe UI", 10, "bold"))
        self.style.configure(
            "Category.TCheckbutton",
            background=surface,
            foreground=foreground,
            font=("Segoe UI", 9),
        )
        self.style.configure("Status.TLabel", background=window_bg, foreground=muted, font=("Segoe UI", 9))
        self.style.configure("TSeparator", background=border)
        self.style.configure(
            "Password.TEntry",
            fieldbackground=field_bg,
            foreground=foreground,
            insertcolor=foreground,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
            padding=10,
        )
        self.style.map(
            "Password.TEntry",
            fieldbackground=[("readonly", field_bg)],
            foreground=[("readonly", foreground)],
        )
        self.style.configure(
            "Field.TSpinbox",
            fieldbackground=field_bg,
            foreground=foreground,
            arrowcolor=muted,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
            padding=5,
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Generate.TButton",
            background=accent,
            foreground="#ffffff" if not self.is_dark else "#111827",
            font=("Segoe UI", 11, "bold"),
            padding=(14, 12),
            borderwidth=0,
        )
        self.style.map("Generate.TButton", background=[("active", accent_active)])
        self.style.configure(
            "Copy.TButton",
            background=copy_bg,
            foreground=foreground,
            font=("Segoe UI", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
        )
        self.style.map("Copy.TButton", background=[("active", copy_active)])
        self.style.configure(
            "Theme.TButton",
            background=surface,
            foreground=field_muted,
            font=("Segoe UI", 9, "bold"),
            padding=(10, 6),
            borderwidth=1,
        )
        self.style.map("Theme.TButton", background=[("active", copy_active)])
        self.theme_button.configure(text="Light mode" if self.is_dark else "Dark mode")

def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()