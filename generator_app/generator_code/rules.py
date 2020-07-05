MIN_PROMPT_TEXT_LENGTH_REQUIREMENT = 50
MAX_KEY_LENGTH = 4

error_descriptions = {
  'bad_input': ('Please enter some long text (at least {} words).'
                .format(MIN_PROMPT_TEXT_LENGTH_REQUIREMENT)),
  'bad_file': 'Error reading file. Check if the file is of correct format (raw text)',
}
