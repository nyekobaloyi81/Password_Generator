# Password Generator

A desktop password generator built with Python and Tkinter. It uses
`secrets` and the operating system cryptographic random source to generate
passwords locally.

## Run

```powershell
python main.py
```

## Features

- Secure cryptographic password generation
- Selectable character categories
- Guaranteed inclusion of each selected category
- Password length from 4 to 128 characters
- Light and dark themes
- Estimated entropy
- Automatic clipboard clearing after 60 seconds
- Keyboard shortcuts: `Ctrl+G` to generate and `Ctrl+Shift+C` to copy

## Test

```powershell
python -m unittest test_password.py
```
