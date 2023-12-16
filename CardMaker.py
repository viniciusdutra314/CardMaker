from os import listdir,getcwd 
from tempfile import TemporaryDirectory  
from time import time; t0=time()

import genanki  
from googletrans import Translator,LANGUAGES
from gtts import gTTS  
from openpyxl import Workbook, load_workbook
def bold(text): return f'<u><b><i>{text}</i></b></u></span> '
def chatgpt_copy_n_past(cardtype,phrase,word=''):
    if cardtype=="v":
      prompt=translate("Explain what this word")
      prompt+=f"_{word}_"
      prompt+=translate("means in this phrase and also in general")
      prompt+=f"_{phrase}_"
      return prompt 
    else:
      return translate(f"Translate this phrase to my mother tongue and explain it is meaning") +phrase         
def create_note(text):
    global i,my_model,langs
    return genanki.Note(model=my_model,fields=text,
                        tags=[str(langs[int(i)]), "cardmaker"])
def create_audios(cardtype,langs,phrases,audio_path,deck_name,words=''):
  for j in range(len(phrases)):
        if cardtype=="v":
          audio_phrase = gTTS(f"{words[j]}.{phrases[j]}", lang=langs[j])
          audio_phrase.save(f"{audio_path}//{deck_name}phrase{j}.mp3")
          audio_word= gTTS(words[j], lang=langs[j])
          audio_word.save(f"{audio_path}//{deck_name}word{j}.mp3")
        elif cardtype in ["s","w"]:
          audio_phrase = gTTS(phrases[j], lang=langs[j])
          audio_phrase.save(f"{audio_path}//{deck_name}phrase{j}.mp3")
        elif cardtype=="p":
          audio = gTTS(phrases[j], lang=langs[j])
          audio.save(f"{audio_path}//{deck_name}pronunciation{j}.mp3")
def create_deck(cardtype,deck_name,color,phrases,words=''):
  from random import randint
  id_deck =randint(1e9, 1e10)
  fields=[{'name': 'Question'},{'name': 'Answer'},{'name': 'MyMedia'}]
  deck = genanki.Deck(id_deck,deck_name)
  if cardtype in ["v","s"]:
      my_model = genanki.Model(
          678_613_134, 'CardMaker Q&A',
          fields=fields, templates=[
              {'name': 'Card Q&A',
              'qfmt': '{{Question}}<br>{{MyMedia}}',
              'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',},])
  elif cardtype=="w":
      my_model = genanki.Model(
          516_000_134, 'CardMaker Type in the Answer',
          fields=fields, templates=[
              {'name': 'Card Type in the Answer',
                'qfmt': '{{Question}}<br> {{type:Answer}}',
                'afmt': '{{FrontSide}}{{MyMedia}}',},])
  elif cardtype=="p":
      my_model = genanki.Model(
          130_931_301,'CardMaker Pronunciation',
          fields=fields,templates=[
              {'name': 'Card Pronunciation',
                'qfmt': '{{Question}}<br>{{MyMedia}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',},])

  for i in range(len(phrases)):
        try:
          if cardtype=="s":
              note =create_note([f"{color}{bold(langs[i])}{translated_phrases[i]}",
                                f"{insert_sound(f'{deck_name}phrase{i}')}{phrases[i]}",""])
          elif cardtype=="v":
              note =create_note(["",f"{insert_sound(f'{deck_name}word{i}')}\
                                {color}{bold(words[i])} == {translated_words[i]}",
                                f"{insert_sound(f'{deck_name}phrase{i}')}{color}\
                                  {bold(words[i])}. {phrases[i]}"])
          elif cardtype=="w":
              note = create_note([f"{color}{bold(langs[i])}{translated_phrases[i]}", 
                                  phrases[i],
                                  insert_sound(f"{deck_name}phrase{i}")])
          elif cardtype=="p":
              note = create_note([f"{color}{bold(phrases[i])}",
                                  insert_sound(f"{deck_name}pronunciation{i}"),
                                  " ", ""])
          deck.add_note(note)
        except:...
  return deck
def check_translation(cardtype,phrases,translated_phrases,
                      words='',translated_words='',
                      check_table_name='check_table.xlsx'):
    workbook_checking= Workbook()
    check_table=workbook_checking.active
    vocab_header=["ChatGPT"] 
    if cardtype=="v": vocab_header.append("Words","Translated Words")
    check_table.append(["Phrases","Translated_Phrases"]+ vocab_header)
    for i in range(len(phrases)):
      check_table["A"+str(i+2)]=phrases[i]
      check_table["B"+str(i+2)]=translated_phrases[i]
      check_table["C"+str(i+2)]=chatgpt_copy_n_past(cardtype,phrases[i],words[i])
      if cardtype=="v":
        check_table["D"+str(i+2)]=words[i]
        check_table["E"+str(i+2)]=translated_words[i]
    workbook_checking.save(check_table_name)
    workbook_checking.close()
def data_from_starting_table(cardtype,table_name):
  workbook ,deck_name= load_workbook(table_name), table_name[:-5:]
  input_table=workbook.active
  phrases = import_column(input_table,"A")
  if cardtype=="v": 
    words=import_column(input_table,"B")
    langs=import_column(input_table,'C')
  else:
    langs=import_column(input_table,'B')
    words=['' for i in range(len(phrases))]
  workbook.close()
  if len(langs)==1:
    unique_lang=langs[0]
    langs=[unique_lang for _ in range(len(phrases))]
  for line,lang in enumerate(langs): 
    if not is_lang_valid(lang):
      raise ValueError(f"{lang} in line {line} is not supported")
  return phrases,words,langs,deck_name
def is_lang_valid(language_code):
    return language_code in LANGUAGES.keys()
def import_column(table,column):
  return [cell.value for cell in table[column] if cell.value][1::]
def import_data_from_table(cardtype,table_name='verified_table.xlsx'):
  workbook_verified=load_workbook(table_name)
  verified_table=workbook_verified.active  
  phrases= import_column(verified_table,"A")
  translated_phrases=import_column(verified_table,"B")
  words=''
  translated_words=''
  if cardtype=="v":
    words=import_column(verified_table,"C")
    translated_words=import_column(verified_table,"D")
  workbook_verified.close()
  return phrases,translated_phrases,words,translated_words
def insert_sound(file_name): return f"[sound:{file_name}.mp3]"
def get_user_input(prompt,validation_func,
                   erro_msg='',input_mod=lambda x:x):
   while True:
      user_input=input(prompt)
      if validation_func(user_input):
            return input_mod(user_input)
      else:
         print(erro_msg)
def translate(message,translator=Translator(),source="en",chosen_language='pt'):
  return translator.translate(message, src=source,dest=chosen_language).text
def translate_phrases_n_words(cardtype,langs,chosen_lang,phrases,words=''):
  translated_phrases=[translate(phrases[i],source=langs[i],chosen_language=chosen_lang) for i in range(len(phrases))]
  if cardtype=="v": translated_words=[translate(words[i],source=langs[i]) for i in range(len(phrases))]
  else: translated_words=['' for i in range(len(phrases))]
  return translated_phrases,translated_words