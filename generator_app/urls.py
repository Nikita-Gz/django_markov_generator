from django.urls import path

from . import views

app_name = 'generator_app'
urlpatterns = [
  path('', views.homepage, name='homepage'),

  # urls related to entering text data
  path('text_input', views.text_input, name='text_input'),
  path('text_input/<str:error_name>', views.text_input, name='text_input_err'),
  path('submit_input', views.submit_input, name='submit_input'),

  # urls related to generating text
  path('generator_page', views.generator_page, name='generator_page'),
  path('generate_text', views.submit_generate_text, name='generate_text'),

  path('clear_session', views.clear_session, name='clear_session'),

  # url which raises unhandled exception, to see what response does django send
  path('f', views.ded, name='ded'),
]
