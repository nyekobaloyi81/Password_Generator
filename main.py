import secrets


CHARACTER_SETS = {
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "numbers": "0123456789",
    "symbols": "!@#$%^&*()-_=+[]{};:,.?/|~",
}

def generate_password(length: int) -> str:
    characters = "".join(CHARACTER_SETS.values())
    return "".join(secrets.choice(characters) for _ in range(length))


def user_input() -> int:
    y = True
    while y == True:
        number = input("Enter length of password: ")
        try:
            number = int(number)

            if not 4 <= number <= 24:
                print("Password length must be between 4 and 24.")
                continue

            y = False
        except:
            print("Invalid input, please try again.")

    return number


def main():
    user_length = user_input()

    print(f"Thank you! generating password of length: {user_length}")

    password = generate_password(user_length)
    print(f"Generated password: {password}")


if __name__ == "__main__":
    main()