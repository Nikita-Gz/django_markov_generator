import re

punctuations = ['!', '?', '.', ',', '(', ')', '"']

# performs basic preprocessing and split by punctuation
# returns list of words
def basic_preprocessing(string, split_by_punctuation) -> list:
  string = string.strip().lower()

  # creates regex to split text with punctuations
  punctuation_template = '(\{})'
  r = '|'.join([punctuation_template.format(punctuation) for punctuation
                in punctuations])
  punctuation_matcher = re.compile(r)

  def punctuation_spacer(match):
    return ' ' + match.group() + ' '

  if split_by_punctuation:
    string = punctuation_matcher.sub(punctuation_spacer, string)

  string = string.split()

  # string = string.split(',')
  return string
