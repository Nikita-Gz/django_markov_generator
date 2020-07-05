from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse

from .generator_code.rules import *
from .generator_code.generator_functions import create_frequency_table, generate
from .generator_code.text_preprocessing import normal_preprocessing

def homepage(request: HttpRequest):
  # todo: make it a proper homepage maybe
  return HttpResponseRedirect(reverse('generator_app:text_input'))

def text_input(request: HttpRequest):
  context = {
    'entered_text_start': request.session.get('entered_text_start', ''),
    'coma_cbox_status': request.session.get('coma_cbox_status', ''),
    'numbers_cbox_status': request.session.get('numbers_cbox_status', 'checked'),
  }

  return render(request, 'generator_app/text_input.html', context)

def ask_to_enter_text_again(request: HttpRequest, message=None):
  if message is None:
    message = "Please enter some long text (at least {} words).".format(MIN_PROMPT_TEXT_LENGTH_REQUIREMENT)

  return render(request, 'generator_app/text_input.html', {
    'error_message': message,
  })

def submit_input(request: HttpRequest):
  text = request.POST['typed_text']
  separate_comas = 'separate_comas' in request.POST.keys()
  replace_number = 'remove_numbers' in request.POST.keys()

  processed = normal_preprocessing(text,
                                  remove_numbers=replace_number,
                                  split_by_punctuation=separate_comas)
  if len(processed) < MIN_PROMPT_TEXT_LENGTH_REQUIREMENT:
    return ask_to_enter_text_again(request)

  request.session['input_given'] = True
  request.session['entered_text_start'] = ' '.join(processed[:8]) + str('..')
  request.session['frequency_table'] = create_frequency_table(processed, MAX_KEY_LENGTH, True)
  request.session['coma_cbox_status'] = (lambda: 'checked' if separate_comas else '')()
  request.session['numbers_cbox_status'] = (lambda: 'checked' if replace_number else '')()

  # remove data from previous generations
  request.session['generated_text'] = ''
  request.session['last_prompt'] = ''
  request.session['stop_reason'] = ''

  return HttpResponseRedirect(reverse('generator_app:generator_page'))

def generator_page(request: HttpRequest):
  if not request.session.get('input_given', False):
    return ask_to_enter_text_again(request)

  context = {
    'last_prompt': request.session['last_prompt'],
    'generated_text': request.session['generated_text'],
    'stop_reason': request.session['stop_reason'],
    'key_length': request.session.get('key_length', MAX_KEY_LENGTH // 2),
    'text_length': request.session.get('text_length', 50),
    'entered_text_start': request.session['entered_text_start'],
  }

  return render(request, 'generator_app/generator.html', context)

def generate_text(request: HttpRequest):
  request.session['last_prompt'] = request.POST['prompt']

  text_length = int(request.POST['text_length'])
  key_length = int(request.POST['key_length'])

  remove_numbers = request.session['numbers_cbox_status'] == 'checked'
  split_by_punctuation = request.session['coma_cbox_status'] == 'checked'
  generator_output = generate(request.session['frequency_table'], request.session['last_prompt'],
                              text_length, key_length,
                              remove_numbers,
                              split_by_punctuation)
  generated_text, chosen_prompt, reason_for_stop = generator_output


  request.session['generated_text'] = generated_text
  request.session['last_prompt'] = chosen_prompt
  request.session['stop_reason'] = reason_for_stop
  request.session['key_length'] = request.POST['key_length']
  request.session['text_length'] = request.POST['text_length']

  return HttpResponseRedirect(reverse('generator_app:generator_page'))

def count_substrings_page(request: HttpRequest):
  text = request.session.get('preprocessed_text', None)
  if text is None:
    return ask_to_enter_text_again(request)

  text_start = text
  if len(text_start) > 15:
    text_start = text_start[:13] + '...'

  occurance_count = request.session.get('occurance_count', 0)
  context = {'text_start': text_start,
             'occurance_count': occurance_count}

  return render(request, 'generator_app/substring_counting.html', context)

def count_substrings(request: HttpRequest):
  substring = request.POST['substring'] # type: str
  string = request.session.get('preprocessed_text', None) # type: str

  count = string.count(substring)
  request.session['occurance_count'] = count
  return HttpResponseRedirect(reverse('generator_app:count_substrings_page'))

def clear_session(request: HttpRequest):
  request.session.flush()
  return HttpResponseRedirect(reverse('generator_app:homepage'))
