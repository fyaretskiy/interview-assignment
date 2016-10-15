import unittest
from unittest.mock import patch

from parsers import Parsers, get_payload, Output


class TestParser(unittest.TestCase):

    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    NUMBER = '(703)-742-0996'
    CLEAN_NUMBER = '7037420996'
    BAD_NUMBER = '1324152151352625'
    COLOR = 'RED'
    ZIPCODE = '10013'
    BAD_ZIP = '121311'

    LINE_TYPE_A = '{}, {}, {}, {}, {}'.format(LAST_NAME, FIRST_NAME,
                                              NUMBER, COLOR, ZIPCODE)
    LINE_TYPE_B = '{} {}, {}, {}, {}'.format(FIRST_NAME, LAST_NAME,
                                             COLOR, ZIPCODE, NUMBER)
    LINE_TYPE_C = '{}, {}, {}, {}, {}'.format(FIRST_NAME, LAST_NAME,
                                              ZIPCODE, NUMBER, COLOR)
    BAD_NUMBER_TYPE_A = '{}, {}, {}, {}, {}'.format(LAST_NAME, FIRST_NAME,
                                                    BAD_NUMBER, COLOR, ZIPCODE)
    BAD_ZIP_A = '{}, {}, {}, {}, {}'.format(LAST_NAME, FIRST_NAME,
                                            NUMBER, COLOR, BAD_ZIP)

    def test_format_a(self):
        p = Parsers(self.LINE_TYPE_A)
        data = p.get_data()

        self.assertEqual(data['first_name'], self.FIRST_NAME)
        self.assertEqual(data['last_name'], self.LAST_NAME)
        self.assertEqual(data['phone_number'], self.CLEAN_NUMBER)
        self.assertEqual(data['color'], self.COLOR)
        self.assertEqual(data['zip_code'], self.ZIPCODE)

    def test_format_b(self):
        p = Parsers(self.LINE_TYPE_B)
        data = p.get_data()

        self.assertEqual(data['first_name'], self.FIRST_NAME)
        self.assertEqual(data['last_name'], self.LAST_NAME)
        self.assertEqual(data['phone_number'], self.CLEAN_NUMBER)
        self.assertEqual(data['color'], self.COLOR)
        self.assertEqual(data['zip_code'], self.ZIPCODE)

    def test_format_c(self):
        p = Parsers(self.LINE_TYPE_C)
        data = p.get_data()

        self.assertEqual(data['first_name'], self.FIRST_NAME)
        self.assertEqual(data['last_name'], self.LAST_NAME)
        self.assertEqual(data['phone_number'], self.CLEAN_NUMBER)
        self.assertEqual(data['color'], self.COLOR)
        self.assertEqual(data['zip_code'], self.ZIPCODE)

    @patch('parsers.logging.log')
    def test_format_a_bad_number(self, log):
        p = Parsers(self.BAD_NUMBER_TYPE_A)

        self.assertEqual(p.get_data(), {})
        self.assertTrue(p.invalid)

        self.assertEqual(
            log.call_args[0][1],
            'Phone number doesn\'t meet requirements: '
            'last_name, first_name, 1324152151352625, RED, 10013.'
        )

    @patch('parsers.logging.log')
    def test_bad_zip_code_type_a(self, log):
        p = Parsers(self.BAD_ZIP_A)

        self.assertEqual(p.get_data(), {})
        self.assertTrue(p.invalid)

        self.assertEqual(
            log.call_args[0][1],
            'Zip code not found in data: '
            'last_name, first_name, (703)-742-0996, RED, 121311.'

        )


test_get_payload_expect_response = """{
  "entries": [
    {
      "color": "yellow",
      "firstname": "James",
      "lastname": "Murphy",
      "phonenumber": "018-154-6474",
      "zipecode": "83880"
    },
    {
      "color": "yellow",
      "firstname": "Booker T.",
      "lastname": "Washington",
      "phonenumber": "373-781-7380",
      "zipecode": "87360"
    }
  ],
  "errors": [
    1,
    3
  ]
}"""


class TestParsersMethods(unittest.TestCase):

    lines = """Booker T., Washington, 87360, 373 781 7380, yellow
    Chandler, Kerri, (623)-668-9293, pink, 123123121
    James Murphy, yellow, 83880, 018 154 6474
    asdfawefawea
    """

    def test_get_payload(self):
        response = get_payload(self.lines)

        self.assertEqual(
            response,
            test_get_payload_expect_response
        )


class TestOutput(unittest.TestCase):
    sample_data = [
        {
            'last_name': 'Doe',
            'first_name': 'John',
            'zip_code': '10013',
            'color': 'blue',
            'phone_number': '2121234567'
        },
        {
            'last_name': 'Doe',
            'first_name': 'Jane',
            'zip_code': '10013',
            'color': 'red',
            'phone_number': '2121234567'
        }
    ]

    def test_get_response(self):
        output = Output(self.sample_data)
        response = output.get_response()

        self.assertEqual(
            response[0]['firstname'],
            'Jane'
        )

        self.assertEqual(
            response[1]['firstname'],
            'John'
        )


if __name__ == '__main__':
    unittest.main()
