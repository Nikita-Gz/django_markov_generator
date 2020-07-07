from django.test import TestCase

from .generator_code.text_preprocessing import normal_preprocessing
from .generator_code.generator_functions import fix_generated_punctuation


def generate_strings_for_default_preprocessing():
  """
  returns list of pairs of input strings and target preprocessed strings
  (with replaced numbers)
  """
  strings = [('  Oi,   ohh\nOhOh ', ['oi', ',', 'ohh', '.', 'ohoh']),
             ('Hey! ', ['hey', '!']),
             ('Hey!! ! How are you??', ['hey', '!', 'how', 'are', 'you', '?']),
             ('oh... weird..', ['oh', '.', 'weird', '.']),
             ('Its 1.23*10^-34km away. 5th', ['its', 'NUMBER', 'away', '.', 'NUMBER']),
             ('That will be 5.99$, please', ['that', 'will', 'be', 'NUMBER', ',', 'please'])
             ]

  return strings


# todo: maybe add more generator tests
class GeneratorFunctionsTests(TestCase):

  def test_fixing_generated_punctuation(self):
    """ tests fixing strings like 'hello , friend' to 'hello, friend' """

    strings = [('hello , friend', 'hello, friend'),
               ('well . how about 700 ?', 'well. how about 700?'),
               ('hai ! how are you ? "good"', 'hai! how are you? "good"')]

    for input_string, target_string in strings:
      fixed_string = fix_generated_punctuation(input_string)
      self.assertEqual(fixed_string, target_string)


class PreprocessingTests(TestCase):

  def test_default_preprocessing(self):
    """ test preprocessing with default arguments """
    strings = generate_strings_for_default_preprocessing()

    for input_str, target_str in strings:
      processed = normal_preprocessing(input_str)
      self.assertEqual(processed, target_str)

  def test_preprocessing_without_punctuation_split(self):
    """
    test preprocessing without punctuation splitting
    relies on test test_fixing_generated_punctuation() to be successful
    """
    input_strings, target_strings = zip(*generate_strings_for_default_preprocessing())
    input_strings, target_strings = list(input_strings), list(target_strings)

    # changes target strings to be without punctuation spacing
    for i, words in enumerate(target_strings):
      s = fix_generated_punctuation(' '.join(words)).split()
      target_strings[i] = s

    for input_str, target_str in zip(input_strings, target_strings):
      processed = normal_preprocessing(input_str, split_by_punctuation=False)
      self.assertEqual(processed, target_str)
