import random

from collections import defaultdict
from .rules import PREFERRED_PREPROCESSING

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
def generate(table, prompt, max_text_length, max_key_length, split_by_punctuation):
  # create prompt if there is none, use it if there is one
  if prompt == '':
    prompt = PREFERRED_PREPROCESSING(random.choice(list(table)), split_by_punctuation)
  else:
    prompt = PREFERRED_PREPROCESSING(prompt, split_by_punctuation)
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

  generated_words = ' '.join(generated_words)
  prompt = ' '.join(prompt)
  return generated_words, prompt, 'Reached the text length limit'
