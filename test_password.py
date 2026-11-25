import unittest

from password import CHARACTER_SETS, estimate_entropy, generate_password


class PasswordTests(unittest.TestCase):
    def test_default_password_uses_all_character_categories(self) -> None:
        password = generate_password(16)

        self.assertEqual(len(password), 16)
        for category in CHARACTER_SETS:
            self.assertTrue(
                any(character in CHARACTER_SETS[category] for character in password),
                category,
            )

    def test_selected_categories_only(self) -> None:
        password = generate_password(20, ("lowercase", "numbers"))
        allowed = CHARACTER_SETS["lowercase"] + CHARACTER_SETS["numbers"]

        self.assertEqual(len(password), 20)
        self.assertTrue(all(character in allowed for character in password))
        self.assertTrue(any(character in CHARACTER_SETS["lowercase"] for character in password))
        self.assertTrue(any(character in CHARACTER_SETS["numbers"] for character in password))

    def test_requires_category(self) -> None:
        with self.assertRaises(ValueError):
            generate_password(16, ())

    def test_length_must_fit_selected_categories(self) -> None:
        with self.assertRaises(ValueError):
            generate_password(2, ("lowercase", "uppercase", "symbols"))

    def test_entropy_is_positive(self) -> None:
        entropy = estimate_entropy(16, ("lowercase", "uppercase", "numbers", "symbols"))

        self.assertGreater(entropy, 100)


if __name__ == "__main__":
    unittest.main()
