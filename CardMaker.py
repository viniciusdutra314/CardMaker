from os import listdir,getcwd 
from tempfile import TemporaryDirectory  
from time import time

import genanki  
from googletrans import Translator,LANGUAGES
from gtts import gTTS  
from openpyxl import Workbook, load_workbook
from rich import print  
def translate(message,source="en"):
  global chosen_language
  return translator.translate(message, src=source,dest=chosen_language).text
def import_column(table,column):
  return [cell.value for cell in table[column] if cell.value][1::]
def insert_sound(file_name): return f"[sound:{file_name}.mp3]"
def bold(text): return f'<u><b><i>{text}</i></b></u></span> '
def create_note(text):
    global i,my_model,langs
    return genanki.Note(model=my_model,fields=text,
                        tags=[str(langs[int(i)]), "cardmaker"])
def get_user_input(prompt,validation_func,
                   erro_msg='',input_mod=lambda x:x):
   while True:
      user_input=input(prompt)
      if validation_func(prompt):
            return input_mod(user_input)
      else:
         print(erro_msg)
def is_lang_valid(language_code):
    return language_code in LANGUAGES.keys()
def chatgpt_copy_n_past(cardtype,word,phrase):
    if cardtype=="v":
      prompt=translate("Explain what this word")
      prompt+=f"_{word}_"
      prompt+=translate("means in this phrase and also in general")
      prompt+=f"_{phrase}_"
      return prompt 
    else:
      return translate(f"Translate this phrase to my mother 
                       tongue and explain is meaning") +phrases[i]         
translator = Translator() 
t_o=time() 

print('Welcome to Anki-Cardmaker :earth_americas: !')
print(f'The program is on a command line but there is 
      no need to fear :smiley:')
chosen_language=get_user_input(f"Choose the language that your cards and 
                          the interface will be translated (ex:pt,fr,en): ",
                          lambda lang: is_lang_valid(lang),
                          f"Typo in your language or unfortunately your language 
                          is not supported by the code :(",
                          lambda x:x.lower())
  
tables_in_the_directory=[j for j in listdir() if j.endswith('.xlsx') and j.startswith("~$") 
                         and j not in ["temp_table.xlsx","verified_table.xlsx"]] 
num_tables=len(tables_in_the_directory)
if len(num_tables)==0:
   print(translate("You haven't import any excel table"))
elif len(num_tables)==1:
   table_name=tables_in_the_directory
elif len(num_tables)>1: 
  print(tables_in_the_directory)
  table_name=get_user_input(translate("Name of the excel table"),
            lambda table_name: table_name+".xlsx" in tables_in_the_directory,
            translate("Invalid table name"),
            lambda x: x +".xlsx")
  
print(f"{translate('Using the table')}[green]table_name[/green]")
workbook ,deck_name= load_workbook(table_name), table_name[:-5:]
table=workbook.active
print(f"[blue]p=pronunciation [/blue] [red]s=speaking [/red] 
      [green] w=writing[/green] [yellow] v=vocabulary [/yellow]")
cardtype=get_user_input(translate("What is the type of your card?"),
                   lambda cardtype: cardtype in ["s","p","w","v"],
                   translate("[red]ERROR[/red], cardtype invalid"),
                   lambda x:x[0].lower())


phrases = import_column(table,"A")
if cardtype=="v": 
   words=import_column(table,"B")
   langs=import_column(table,'C')
else:
  langs=import_column(table,'B')
workbook.close()
if len(langs)==1:
  unique_lang=langs[0]
  langs=[unique_lang for _ in range(len(phrases))]
for line,lang in enumerate(langs): 
   if not is_lang_valid(lang):
    raise ValueError(f"{lang} in line {line} is not supported")

print(translate("Translating...(1/2)"))
translated_phrases=[translate(phrases[i],source=langs[i]) for i in range(len(phrases))]
if cardtype=="v": translated_words=[translate(words[i],source=langs[i]) for i in range(len(phrases))]

#checking
if cardtype!="p":
  workbook2= Workbook()
  check_table=workbook2.active
  vocab_header=["Words","Translated_Words"] 
  if cardtype=="v": vocab_header.append("ChatGPT")
  check_table.append(["Phrases","Translated_Phrases"]+ vocab_header)
  for i in range(len(phrases)):
    check_table["A"+str(i+2)]=phrases[i]
    check_table["B"+str(i+2)]=translated_phrases[i]
    if cardtype!="v":
      check_table["C"+str(i+2)]=chatgpt_copy_n_past(cardtype,
                                                    words[i],phrases[i])
    else:  
      check_table["C"+str(i+2)]=words[i]
      check_table["D"+str(i+2)]=translated_words[i]
      check_table["E"+str(i+2)]=chatgpt_copy_n_past(cardtype,
                                                    words[i],phrases[i])
  workbook2.save("check_table.xlsx")
  workbook2.close()
  print(f"{translate('Your translations are ready in')}[green] check_table.xlsx![/green]")
  print(translate("Please assert that everthing is fine and then save as"))
  input(f"[green] verified_table.xlsx [/green],{translate('press any key to continue')}:")
  while 'verified_table.xlsx' not in listdir():
      print(f"[red]translate('Error, You forgot to save the verified_table.xlsx')[/red]")
      input(translate("press any key to continue"))
  workbook3=load_workbook("verified_table.xlsx")
  verified_table=workbook3.active  
  phrases= import_column(verified_table,"A")
  translated_phrases=import_column(verified_table,"B")
  if cardtype=="v":
    words=import_column(verified_table,"C")
    translated_words=import_column(verified_table,"D")
  workbook3.close()
print(translate("Audios...(2/2)"))
#create a temp directory inside the project's folder
with TemporaryDirectory(dir=getcwd(),prefix=".tempaudio") as audio_path:
  for j in range(len(phrases)):
      try:
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
      except:...

  from random import randint
  id_deck =randint(1e9, 1e10)
  fields=[{'name': 'Question'},{'name': 'Answer'},{'name': 'MyMedia'}]

  deck = genanki.Deck(id_deck,deck_name)

  if cardtype in ["v","s"]:
      my_model = genanki.Model(
          678_613_134,
          'CardMaker Q&A',
          fields=fields,
          templates=[
              {
                  'name': 'Card Q&A',
                  'qfmt': '{{Question}}<br>{{MyMedia}}',
                  'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
              },
          ])
  elif cardtype=="w":
      my_model = genanki.Model(
          516_000_134,
          'CardMaker Type in the Answer',
          fields=fields,
          templates=[
              {
                  'name': 'Card Type in the Answer',
                  'qfmt': '{{Question}}<br> {{type:Answer}}',
                  'afmt': '{{FrontSide}}{{MyMedia}}',
              },
          ])
  elif cardtype=="p":
      my_model = genanki.Model(
          130_931_301,
          'CardMaker Pronunciation',
          fields=fields,
          templates=[
              {
                  'name': 'Card Pronunciation',
                  'qfmt': '{{Question}}<br>{{MyMedia}}',
                  'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
              },
          ])
  #Color of the cards

  print("[blue]Blue[/blue] [red]Red [/red] [yellow]Yellow[/yellow] [magenta] Purple [/magenta] [green] Green [/green]")
  colors_rgb = {'gr': '<span style="color: rgb(81, 255, 37);">', 're': '<span style="color: rgb(228, 14, 14);">',
                    'bl': '<span style="color: rgb(18, 166, 252);">',
                    'ye': '<span style="color: rgb(249, 255, 54);">',
                    'pu': '<span style="color: rgb(198, 38, 255);">',
                    'pi': '<span style="color: rgb(255, 14, 192);">', }
  color=get_user_input(translate("Select a color: "),
                  lambda color: colors_rgb[color],
                  translate("[red]Color invalid! [/red]"),
                  lambda color:color[0:2].lower())

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


  media_files=[f"{audio_path}//{j}" for j in listdir(audio_path)]
  genanki.Package(deck,media_files=media_files).write_to_file(f"{deck_name}.apkg")

  deltat=time() -t_o
  print(f"Congratulations, {len(phrases)} flashcards in {deltat/60:.1f} 
        minutes! {60*len(phrases)/deltat:1f} flashcards per minute")
