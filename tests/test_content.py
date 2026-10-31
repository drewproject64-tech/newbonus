import unittest

from content import BOT_NAME, BOT_USERNAME, SHORT_DESCRIPTION, DESCRIPTION, CHECK_QUESTIONS, TIPS


class PublicContentTest(unittest.TestCase):
    def test_expected_destination(self):
        self.assertEqual(BOT_NAME, 'Especialista')
        self.assertEqual(BOT_USERNAME, 'Bonus_Specialist_Bot')

    def test_telegram_profile_limits(self):
        self.assertLessEqual(len(BOT_NAME), 64)
        self.assertLessEqual(len(SHORT_DESCRIPTION), 120)
        self.assertLessEqual(len(DESCRIPTION), 512)

    def test_three_function_content(self):
        self.assertEqual(len(CHECK_QUESTIONS), 4)
        self.assertGreaterEqual(len(TIPS), 3)


if __name__ == '__main__':
    unittest.main()
