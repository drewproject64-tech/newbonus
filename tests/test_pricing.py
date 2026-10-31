import unittest
from decimal import Decimal
from pricing import parse_eur, format_eur, calculate_discount


class PricingTest(unittest.TestCase):
    def test_prices(self):
        for text in ('19,99', '19.99', '19,99 €', '€ 19.99'):
            self.assertEqual(parse_eur(text), Decimal('19.99'))
        self.assertEqual(parse_eur('1.234,50'), Decimal('1234.50'))
        self.assertEqual(parse_eur('1,234.50'), Decimal('1234.50'))

    def test_invalid(self):
        for text in ('0', '-2', 'abc', '1e6', '2.333.2', '1000000000'):
            with self.assertRaises(ValueError, msg=text):
                parse_eur(text)

    def test_discount(self):
        saved, percent = calculate_discount(parse_eur('79,90'), parse_eur('59,90'))
        self.assertEqual(saved, Decimal('20.00'))
        self.assertEqual(percent, Decimal('25.03'))
        self.assertEqual(format_eur(saved), '20,00 €')
        with self.assertRaises(ValueError):
            calculate_discount(Decimal('50'), Decimal('75'))


if __name__ == '__main__':
    unittest.main()
