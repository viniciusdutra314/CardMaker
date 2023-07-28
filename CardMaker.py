from rich import print #insert colors and emojis on the terminal
import genanki #integration with anki
from googletrans import Translator #translate the phrases
from openpyxl import load_workbook,Workbook
from gtts import gTTS #generate audios
import os #get the file directories
import time #count the amount of time used in creating cards
import tempfile #save and delete the tempaudios

translator = Translator() #start translator
t_o=time.time() # counting time
def translate(message,source="en"):
  global chosen_language
  return translator.translate(message, src=source,dest=chosen_language).text

print('Welcome to Anki-Cardmaker :earth_americas: !')
print('The program is on a command line but there is no need to fear :smiley:')

chosen_language=input("Choose the language that your cards and the interface will be translated (ex:pt,fr,en): ").lower()
while True:
  try:
    translate("checking if the chosen_language is actually working")
    break
  except: 
    print("You have typed your language [red] wrongly [/red]or unfortunately your language is not supported by the code :(")
    chosen_language=input("Choose the language that your cards and the interface will be translated (ex:pt,fr,en): ").lower()
tables_in_the_directory=[j for j in os.listdir() if j[-5::]==".xlsx" and j[0:2]!="~$" and j not in ["checktable.xlsx","verifiedtable.xlsx"]] 

if len(tables_in_the_directory)>1:  #multiple tables to select
  print(tables_in_the_directory)
  while True:
    table_name=input(translate("Name of the excel table")+" ")+".xlsx"
    if table_name in tables_in_the_directory: break
    else:
      wrong_name=translate("Wrong name!")
      print('[red]wrong_name[/red]')
else: 
  try: table_name=tables_in_the_directory[0]
  except: raise ValueError(translate("You haven't import any excel table"))
  print(translate("Using the table")+"[green] "+table_name+"[/green]")
workbook1 ,deck_name= load_workbook(table_name), table_name[:-5:]
table=workbook1.active
print("[blue]p=pronunciation [/blue] [red]s=speaking [/red] [green] w=writing[/green] [yellow] v=vocabulary [/yellow]")
cardtype=input(translate("What is the type of your card?")+" ").lower()
while cardtype not in ["s","p","w","v"]:
  print(translate("[red]ERROR[/red], cardtype invalid, type it again"))
  cardtype=input()

def import_column(table,column):
  return [cell.value for cell in table[column] if cell.value!=None and cell.value!=""][1::]

phrases = import_column(table,"A")
if cardtype=="v": 
  words=import_column(table,"B")

column="B" if cardtype!="v"  else "C"
languages=import_column(table,column)
if len(languages)==1:
  unique_lang=languages[0]
  languages=[unique_lang for _ in range(len(phrases))]
assert len(languages)>1, translate("Language error, you probably forgot to specify the languages in your excel table")

workbook1.close()

def wordinphrase(word,phrase):
    word,phrase=str(word).lower(),str(phrase).lower()
    remove=[".",",","?","!",":",";","-","=","_"]
    for k in remove:
        word=word.replace(k,"")
        phrase=phrase.replace(k," ")
    if len(word.split())==1: #single word
      for j in phrase.split():
          if str(j)==str(word):
              return True
    else: #composite word
      if word in phrase: return True
    return False

if cardtype=='v':
    if input(translate("Do you want to check if the word is in the phrase?")+" y=yes, n=no:")[0].lower() =="y":
        for j in range(len(phrases)):
            if not wordinphrase(words[j],phrases[j]):
              while True:
                print(translate("[red]Error[/red]: Word not in the phrase"))
                print("\n"+phrases[j]+"\n"+words[j])
                words[j]=input(translate("Correct word:"))
                if wordinphrase(words[j],phrases[j]):
                  break


print(translate("Translating...(1/2)"))
translated_phrases=[translate(phrases[i],source=languages[i]) for i in range(len(phrases))]
if cardtype=="v": translated_words=[translate(words[i],source=languages[i]) for i in range(len(phrases))]

#checking
if cardtype!="p":
  workbook2= Workbook()
  check_table=workbook2.active
  vocab_header=["Words","Translated_Words","ChatGPT"] if cardtype=="v" else ["ChatGPT"]
  check_table.append(["Phrases","Translated_Phrases"]+ vocab_header)

  def chatgpt_copy_n_past(i):
    global cardtype,words,phrases
    if cardtype=="v":
      return translate("Explain what this word") +f"_{words[i]}_" + translate("means in this phrase and also in general") + f"_{phrases[i]}_"
    else:
      return translate("Translate this phrase to my mother tongue and explain is meaning") +phrases[i]

  for i in range(len(phrases)):
    check_table["A"+str(i+2)]=phrases[i]
    check_table["B"+str(i+2)]=translated_phrases[i]
    check_table["C"+str(i+2)]=words[i] if cardtype=="v" else chatgpt_copy_n_past(i)
    if cardtype=="v":
      check_table["D"+str(i+2)]=translated_words[i]
      check_table["E"+str(i+2)]=chatgpt_copy_n_past(i)
  workbook2.save("checktable.xlsx")
  workbook2.close()
  print(translate("Your translations are ready in")+"[green] checktable.xlsx! [/green]")
  print(translate("Please assert that everthing is fine and then save as"))
  print("[green] verifiedtable.xlsx [/green]"+translate(",press any key to continue"))
  time_to_check=input()
  while True:
    try:
      workbook3=load_workbook("verifiedtable.xlsx")
      break
    except: 
      print(translate("[red]Error, You forgot to save the verifiedtable.xlsx [/red]"))
      time_to_check=input(translate("press any key to continue"))
  verified_table=workbook3.active  
  phrases= import_column(verified_table,"A")
  translated_phrases=import_column(verified_table,"B")
  if cardtype=="v":
    words=import_column(verified_table,"C")
    translated_words=import_column(verified_table,"D")
  workbook3.close()
print(translate("Audios...(2/2)"))
#create a temp directory inside the project's folder
with tempfile.TemporaryDirectory(dir=os.getcwd(),prefix=".tempaudio") as audio_path:
  for j in range(len(phrases)):
      try:
        if cardtype=="v":
          audio = gTTS(words[j]+"."+phrases[j], lang=languages[j])
          audio.save(audio_path + "//" + deck_name + "phrase" + str(j) + '.mp3')
          audio= gTTS(words[j], lang=languages[j])
          audio.save(audio_path + "//" + deck_name + "word" + str(j) + '.mp3')
        if cardtype in ["s","w"]:
          audio = gTTS(phrases[j], lang=languages[j])
          audio.save(audio_path + "//" + deck_name + "phrase" + str(j) + '.mp3')
        if cardtype=="p":
          audio = gTTS(phrases[j], lang=languages[j])
          audio.save(audio_path + "//" + deck_name + "pronunciation" + str(j) + '.mp3')
      except:pass

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
  if cardtype=="w":
      my_model = genanki.Model(
          516_000_134,
          'CardMaker Type in the Answer',
          fields=fields,
          templates=[
              {
                  'name': 'Card 1',
                  'qfmt': '{{Question}}<br> {{type:Answer}}',
                  'afmt': '{{FrontSide}}{{MyMedia}}',
              },
          ])
  if cardtype=="p":
      my_model = genanki.Model(
          130_931_301,
          'CardMaker Pronunciation',
          fields=fields,
          templates=[
              {
                  'name': 'Card 1',
                  'qfmt': '{{Question}}<br>{{MyMedia}}',
                  'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
              },
          ])
  #Color of the cards

  print("[blue]Blue[/blue] [red]Red [/red] [yellow]Yellow[/yellow] [magenta] Purple [/magenta] [green] Green [/green]")
  color=input(translate("Select a color: "))[0:2].lower()
  colors_rgb = {'gr': '<span style="color: rgb(81, 255, 37);">', 're': '<span style="color: rgb(228, 14, 14);">',
                    'bl': '<span style="color: rgb(18, 166, 252);">',
                    'ye': '<span style="color: rgb(249, 255, 54);">',
                    'pu': '<span style="color: rgb(198, 38, 255);">',
                    'pi': '<span style="color: rgb(255, 14, 192);">', }
  while True:
    try:
      color=colors_rgb[color]
      break
    except:
      print(translate("[red]Color invalid! [/red]"))
      color=input(translate("Select a color: "))[0:2].lower()

  def insert_sound(file_name): return "[" + "sound:" + file_name + ".mp3" + "]"
  def bold(text): return '<u><b><i>' + text +'</i></b></u></span> '
  def create_note(text):
    global i,my_model,languages
    return genanki.Note(model=my_model,fields=text,tags=[str(languages[int(i)]), "cardmaker"])

  for i in range(len(phrases)):
        try:
          if cardtype=="s":
              note =create_note([color + bold(languages[i] ) +translated_phrases[i],insert_sound(deck_name + "phrase" + str(i)) + phrases[i],""])
          if cardtype=="v":
              note =create_note(["",insert_sound(deck_name + "word" + str(i)) + color + bold(words[i])+  " == " + translated_words[i],
                                insert_sound(deck_name + "phrase" + str(i))  + color+ bold(words[i]) + ". " +phrases[i]])
          if cardtype=="w":
              note = create_note([color + bold(languages[i])+translated_phrases[i], phrases[i],insert_sound(deck_name+"phrase"+str(i))])
          if cardtype=="p":
              note = create_note([color + bold(phrases[i]),insert_sound(deck_name + "pronunciation" + str(i))," ", ""])
          deck.add_note(note)
        except:pass


  media_files=[audio_path+"//"+j for j in os.listdir(audio_path)]
  genanki.Package(deck,media_files=media_files).write_to_file(deck_name +'.apkg')

  deltat=time.time() -t_o
  print(f"Congratulations, {len(phrases)} flashcards in {round(deltat/60,1)} minutes! {round(60*len(phrases)/deltat,1)} flashcards per minute")
