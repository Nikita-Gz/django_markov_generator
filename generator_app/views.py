from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse

from .generator_code import rules
from .generator_code.generator_functions import create_frequency_table, generate
from .generator_code.text_preprocessing import normal_preprocessing

def homepage(request: HttpRequest):
  # todo: make it a proper homepage maybe
  return HttpResponseRedirect(reverse('generator_app:text_input'))

def text_input(request: HttpRequest, error_name=''):
  if error_name != '':
    err_message = rules.error_descriptions.get(error_name, 'unknown error')
  else:
    err_message = ''

  context = {
    'entered_text_start': request.session.get('entered_text_start', ''),
    'coma_cbox_status': request.session.get('coma_cbox_status', ''),
    'numbers_cbox_status': request.session.get('numbers_cbox_status', 'checked'),
    'error_message': err_message,
  }

  return render(request, 'generator_app/text_input.html', context)

def ask_to_enter_text_again(error_name: str):
  return HttpResponseRedirect(reverse('generator_app:text_input_err', args=(error_name,)))

def submit_input(request: HttpRequest):
  separate_comas = 'separate_comas' in request.POST.keys()
  replace_number = 'remove_numbers' in request.POST.keys()

  # load text either from file or input
  if 'txt_file' in request.FILES:
    try:
      text = "".join(map(chr, request.FILES['txt_file'].read()))
    except Exception as e:
      return ask_to_enter_text_again('bad_file')
  else:
    text = request.POST['typed_text']

  processed = normal_preprocessing(text,
                                  remove_numbers=replace_number,
                                  split_by_punctuation=separate_comas)
  if len(processed) < rules.MIN_PROMPT_TEXT_LENGTH_REQUIREMENT:
    return ask_to_enter_text_again('bad_input')

  request.session['input_given'] = True
  request.session['entered_text_start'] = ' '.join(processed[:8]) + str('..')
  request.session['frequency_table'] = create_frequency_table(processed, rules.MAX_KEY_LENGTH, True)
  request.session['coma_cbox_status'] = (lambda: 'checked' if separate_comas else '')()
  request.session['numbers_cbox_status'] = (lambda: 'checked' if replace_number else '')()

  # remove data from previous generations
  request.session['generated_text'] = ''
  request.session['last_prompt'] = ''
  request.session['stop_reason'] = ''

  return HttpResponseRedirect(reverse('generator_app:generator_page'))

def generator_page(request: HttpRequest):
  if not request.session.get('input_given', False):
    return ask_to_enter_text_again('bad_input')

  context = {
    'last_prompt': request.session['last_prompt'],
    'generated_text': request.session['generated_text'],
    'stop_reason': request.session['stop_reason'],
    'key_length': request.session.get('key_length', rules.MAX_KEY_LENGTH // 2),
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

def clear_session(request: HttpRequest):
  request.session.flush()
  return HttpResponseRedirect(reverse('generator_app:homepage'))
