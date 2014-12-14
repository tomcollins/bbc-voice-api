import unittest

from language import Parser

class NlpTests(unittest.TestCase):

    def test_find_time_falls_within_range():
        data = load_test_data()
        for item in data:
            sentence = item[3]
            parsed = parser.parse(sentence)
            found_time = parser.find_time(parsed)

    def load_test_data(self):
        data = []
        data_file = open('test_time.txt', 'r')
        line = data_file.readline()
        while line:
            if line.strip() != '' and not line.strip().startswith('#'):
                parts = line.split('|')
                date_from = parts[0].strip()
                date_to = parts[1].strip()
                sentence = parts[2].strip()
                data.append((date_from, date_to, sentence))
            line = data_file.readline()
        data_file.close()

        return data
