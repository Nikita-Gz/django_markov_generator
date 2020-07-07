import re

allowed_punctuations = ['!', '?', '.', ',', '(', ')', '"']


def lower_text(s: str) -> str:
  return s.lower()


# matches non-word, non-digit, non-allowed punctuation symbols
r = r'[^\w\d\s{}]'
r = r.format(''.join('\\' + char for char in allowed_punctuations))
special_symbol_matcher = re.compile(r)
def remove_special_symbols(s: str) -> str:
  s = special_symbol_matcher.sub('', s)
  return s


# matches numbers in different forms (including "2nd", "5$", '8.3*10e-9s')
r = r'(\d+(?:[.,]\d+)*[\w\d\*\^\+\-\/]*(?:[$€£¥])*)'
number_matcher = re.compile(r)
def replace_digits(s: str) -> str:
  s = number_matcher.sub('NUMBER', s)
  return s


# replaces newlines with dots, shrinks multiple whitespaces
newline_matcher = re.compile(r'\s*\n+\s*')
repeating_whitespaces_matcher = re.compile(r'\s{2,}')
def fix_multiple_whitespaces(s: str) -> str:
  """ changes newlines to full stops, changes multiple spaces to single space """
  s = newline_matcher.sub('. ', s)
  s = repeating_whitespaces_matcher.sub(' ', s)
  return s


dotdotdot_matcher = re.compile(r'\.{2,}')
def shrink_dotdotdots(s: str) -> str:
  """ replaces several dots into one dot """
  s = dotdotdot_matcher.sub('.', s)
  return s


# matches patterns like "!!!", "..", or " ?? ?"
repeating_punctuation_template = '(?<!\%s)((?:\s*\%s){2,})(?!\%s)'
def unrepeat_punctuation(s: str) -> str:
  """ removes repeating punctuation symbols """

  for p in allowed_punctuations:
    r = repeating_punctuation_template % (p, p, p)
    matcher = re.compile(r)
    s = matcher.sub(p, s)

  return s


# matches any punctuation
punctuation_template = r'(\{})'
r = '|'.join([punctuation_template.format(p) for p in allowed_punctuations])
punctuation_matcher = re.compile(r)
def separate_punctuations(s: str) -> str:
  """ separates punctuation from words with a whitespace """
  def punctuation_spacer(match):
    return ' ' + match.group() + ' '

  s = punctuation_matcher.sub(punctuation_spacer, s)
  return s


def strip(s: str) -> str:
  return s.strip()


# todo: consider removing unnecessary preprocessing steps
def normal_preprocessing(s: str,
                         remove_numbers=True,
                         split_by_punctuation=True) -> list:
  """
  Performs text preprocessing, returns list of words.
  Optionally considers punctuations as a word
  """
  s = lower_text(s)
  s = remove_special_symbols(s)

  if remove_numbers:
    s = replace_digits(s)

  s = fix_multiple_whitespaces(s)
  s = shrink_dotdotdots(s)
  s = unrepeat_punctuation(s)

  if split_by_punctuation:
    s =  separate_punctuations(s)

  # remove repeating spaces just in case
  s = fix_multiple_whitespaces(s)

  s = strip(s)

  s = s.split()
  return s
