import random
import re

from collections import defaultdict
from .text_preprocessing import normal_preprocessing

def create_frequency_table(words, max_key_length, use_all_key_lengths):
  # use defaultdict to create dicts on access
  table = defaultdict(dict)

  if use_all_key_lengths:
    key_lengths = [i + 1 for i in range(max_key_length)]
  else:
    key_lengths = [max_key_length]

  for length in key_lengths:
    for position, _ in enumerate(words[:-length]):
      key = ' '.join(words[position: position + length])
      next_word = words[position + length]

      # strip just in case
      next_word = next_word.strip()

      next_word_occurances = table[key].get(next_word, 0)
      table[key][next_word] = next_word_occurances + 1

  table = dict(table)

  return table


# returns generated text, selected prompt, and a reason for stopping generation
def generate(table, prompt, max_text_length, max_key_length,
             remove_numbers, split_by_punctuation):
  # create prompt if there is none, use it if there is one
  if prompt == '':
    # for prompt, select keys of maximum key lengths, then make a weighted choice
    keys = [key for key in table if len(key.split()) == max_key_length]
    prompt = normal_preprocessing(random.choice(keys),
                                  remove_numbers,
                                  split_by_punctuation)
  else:
    prompt = normal_preprocessing(prompt,
                                  remove_numbers,
                                  split_by_punctuation)
    if prompt == '':
      raise Exception('Bad prompt!')

  key = ' '.join(prompt)
  generated_words = prompt.copy()
  for i in range(max_text_length):

    # shorten the key until it is either present in table or is too short
    while key not in table:
      key = ' '.join(key.split()[1:])
      if key == '':
        return (' '.join(generated_words),
                ' '.join(prompt),
                'No next words could be generated')

    next_word = random.choices(list(table[key]), table[key].values())
    generated_words.append(next_word[0])

    # update key to use the next set of words
    # print(generated_words)
    key = ' '.join(generated_words[-max_key_length:])

  generated_words = fix_generated_punctuation(' '.join(generated_words))
  prompt = fix_generated_punctuation(' '.join(prompt))
  return generated_words, prompt, 'Reached the text length limit'


# matches space and punctuation in "hello , friend"
r = r'\s[^\w\"\(\)]'
matcher = re.compile(r)
def fix_generated_punctuation(s):
  """ fixes strings like 'hello , friend' to 'hello, friend' """

  def replacer(match):
    return match.group().strip()

  s = matcher.sub(replacer, s)
  return s
