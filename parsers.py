import copy
import json
import logging
from collections import OrderedDict


class Parsers(object):
    """
    Available formats:
    Format A:
    Lastname, Firstname, (703)-742-0996, Blue, 10013

    Format B normalized:
    Firstname, Lastname, Red, 11237, 703 955 0373
    Format B raw:
    Firstname Lastname, Red, 11237, 703 955 0373

    Format C:
    Firstname, Lastname, 10013, 646 111 0101, Green

    Usage:
    p = Parser(line)
    data = p.get_data()

    :arg line: String of format types A, B, C.
    """

    # Maps of item to index of the list
    FORMAT_A_KEY_TO_INDEX = {
        'first_name': 1,
        'last_name': 0,
        'phone_number': 2,
        'color': 3,
        'zip_code': 4
    }

    FORMAT_B_KEY_TO_INDEX = {
        'first_name': 0,
        'last_name': 1,
        'phone_number': 4,
        'color': 2,
        'zip_code': 3
    }

    FORMAT_C_KEY_TO_INDEX = {
        'first_name': 0,
        'last_name': 1,
        'phone_number': 3,
        'color': 4,
        'zip_code': 2
    }

    # Maps index of zip code in line to the format type.
    INDEX_ZIP_TO_FORMAT_KEY_INDEX = {
        FORMAT_A_KEY_TO_INDEX['zip_code']: FORMAT_A_KEY_TO_INDEX,
        FORMAT_B_KEY_TO_INDEX['zip_code']: FORMAT_B_KEY_TO_INDEX,
        FORMAT_C_KEY_TO_INDEX['zip_code']: FORMAT_C_KEY_TO_INDEX
    }

    def __init__(self, line):
        self.line = line
        self.data = {
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'color': '',
            'zip_code': ''
        }
        self.invalid = False

    @staticmethod
    def normalize_format_b(data):
        """
        Standardize B format to 5 comma delimited items.
        """
        name = data.pop(0)
        f_name, l_name = name.split(' ')

        return [f_name, l_name] + data

    def get_data(self):
        """
        Returns line information in a dictionary, or empty dict if the line
        does not match the patterns.
        """
        data = self.line.split(',')

        # Convert format B to the standardized 5 item list.
        if len(data) == 4:
            data = self.normalize_format_b(data)

        data = [item.strip() for item in data]

        # Find format type by the location of the zip code.
        parser_type = None
        for item in data:

            if item.isdigit() and len(list(item)) == 5:
                zip_index = data.index(item)
                parser_type = self.INDEX_ZIP_TO_FORMAT_KEY_INDEX.get(zip_index)

        if not parser_type:
            logging.log(logging.WARNING,
                        'Zip code not found in data: {}.'.format(self.line))
            self.invalid = True
            return {}

        # First Name
        first_name = data[parser_type['first_name']]
        self.update_first_name(first_name)

        # Last Name
        last_name = data[parser_type['last_name']]
        self.update_last_name(last_name)

        # Phone Number
        phone_number = data[parser_type['phone_number']]
        self.update_phone_number(phone_number)

        # Zip Code
        zip_code = data[parser_type['zip_code']]
        self.update_zip_code(zip_code)

        # Color
        color = data[parser_type['color']]
        self.update_color(color)

        return self.data if not self.invalid else {}

    def update_first_name(self, f_name):
        # Space for validation
        self.data.update({'first_name': f_name})

    def update_last_name(self, l_name):
        # Space for validation
        self.data.update({'last_name': l_name})

    def update_phone_number(self, number):
        # Clean extraneous characters from phone number string.
        clean_number = ''.join(
            [i for i in list(number) if i.isdigit()]
        )

        if len(list(clean_number)) != 10:
            logging.log(logging.WARNING,
                        'Phone number doesn\'t'
                        ' meet requirements: {}.'.format(self.line))
            self.invalid = True
        self.data.update({'phone_number': clean_number})

    def update_zip_code(self, zip_code):
        # Space for validation
        self.data.update({'zip_code': zip_code})

    def update_color(self, color):
        # Space for validation
        self.data.update({'color': color})


def process_input(lines):
    lines = lines.split('\n')
    lines = [line.strip() for line in lines]

    # Remove empty lines
    lines = [l for l in lines if l]

    results = []
    errors = []
    for line in lines:
        data = Parsers(line).get_data()

        if data:
            results.append(data)

        else:
            errors.append(lines.index(line))

    results = Output(results).get_response()

    return results, errors


def get_payload(lines):

    results, errors = process_input(lines)
    payload = OrderedDict.fromkeys(['entries', 'errors'])
    payload.update({
        'entries': results,
        'errors': errors
    })

    return json.dumps(payload, indent=2)


class Output(object):
    """
    Takes a list of dictionary objects into the constructor.

    Usage:
    output = Output(array_of_data_dictionaries)
    ordered_dict = output.get_response()

    Returns array of ordered dictionary objects, sorted for output.
    """
    def __init__(self, data):
        self.data = copy.deepcopy(data)
        self.response = []

    def get_response(self):
        for datum in self.data:
            self.response.append(self.get_ordered_item(datum))
        self.response = sorted(self.response,
                               key=lambda x: (x['lastname'], x['firstname']))

        return self.response

    @staticmethod
    def get_ordered_item(item):
        """ Places data into an OrderedDict. Also formats the formats the
        number for display.
        """
        d = OrderedDict.fromkeys(['color', 'firstname', 'lastname',
                                  'phonenumber', 'zipecode'])

        number = item['phone_number']
        number = '{}-{}-{}'.format(number[:3], number[3:6], number[6:])

        d.update({
            'color': item['color'],
            'firstname': item['first_name'],
            'lastname': item['last_name'],
            'phonenumber': number,
            'zipecode': item['zip_code']})
        return d
