from django.test import TestCase

from .generator_code.text_preprocessing import basic_preprocessing


def generate_basic_strings_for_preprocessing():
  # returns list of pairs of input strings and target preprocessed strings
  strings = [('  Oi, ohhOhOh ', 'oi, ohhohoh'),
             ('Hei! ', 'hei!'),
             ]

  return strings


class PreprocessingTests(TestCase):

  def test_basic_preprocessing(self):
    """
    basic_preprocessing(text) properly performs basic preprocessing.
    """
    strings = generate_basic_strings_for_preprocessing()

    for input_str, target_str in strings:
      processed = basic_preprocessing(input_str)
      self.assertEqual(processed, target_str)
