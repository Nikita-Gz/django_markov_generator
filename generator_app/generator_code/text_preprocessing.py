import re

punctuations = ['!', '?', '.', ',', '(', ')', '"']


def lower_text(s: str) -> str:
  return s.lower()


# matches non-word, non-digit and non-specified punctuation symbols
r = r'[^\w\d\s{}]'
r = r.format(''.join('\\' + char for char in punctuations))
special_symbol_matcher = re.compile(r)
def remove_special_symbols(s: str) -> str:
  """ removes non-word, non-digit and non-specified punctuation symbols """
  s = special_symbol_matcher.sub('', s)
  return s


# matches digits in different forms (including "2nd", "5$", '8.3*10e-9s')
r = r'(\d+(?:[.,]\d+)*[\w\d\*\^\+\-\/]*(?:[$€£¥])*)'
digit_matcher = re.compile(r)
def remove_digits(s: str) -> str:
  """ removes digits and replaces them """
  s = digit_matcher.sub('NUMBER', s)
  return s


# replaces newlines with dots, shrinks multiple whitespaces
def fix_multiple_whitespaces(s: str) -> str:
  """ changes newlines to full stops, changes multiple spaces to single space """
  s = re.sub(r'\s*\n+\s*', '. ', s)
  s = re.sub(r'\s{2,}', ' ', s)
  return s


def shrink_dotdotdots(s: str) -> str:
  """ replaces several dots into one dot """
  s = re.sub(r'\.{2,}', '.', s)
  return s


# matches patterns like "!!!" or " ?? ?"
repeating_punctuation_template = '(?<!\%s)((?:\s*\%s){2,})(?!\%s)'
def unrepeat_punctuation(s: str) -> str:
  """ removes repeating punctuation symbols """

  for p in punctuations:
    r = repeating_punctuation_template % (p, p, p)
    matcher = re.compile(r)
    s = matcher.sub(p, s)

  return s


punctuation_template = r'(\{})'
r = '|'.join([punctuation_template.format(p) for p in punctuations])
punctuation_matcher = re.compile(r)
def separate_punctuations(s: str) -> str:
  """ separates punctuation from words with a whitespace """
  def punctuation_spacer(match):
    return ' ' + match.group() + ' '

  s = punctuation_matcher.sub(punctuation_spacer, s)
  return s


def strip(s: str) -> str:
  return s.strip()


# performs basic preprocessing and split by punctuation
# returns list of words
def normal_preprocessing(s: str,
                         remove_numbers=True,
                         split_by_punctuation=True) -> list:
  """ performs text preprocessing, returns list of words """
  s = lower_text(s)
  s = remove_special_symbols(s)

  if remove_numbers:
    s = remove_digits(s)

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
