import pandas as pd #handle the excel tables
from googletrans import Translator #translate the phrases
from gtts import gTTS #generate audios
import genanki #integration with anki
import os #get the file directories
import time #count the amount of time used in creating cards
from colorama import Fore,Back,Style #use colors
import colorama
import pytesseract as tess #duolingo text extract
from random import randint #random 2 letters in the id_deck
from PIL import Image #open the duolingo prints
import xlsxwriter #excel tables
from selenium import webdriver # open color custom website


translator = Translator() #start translator
colorama.init(strip=False) #colors in the terminal
t_o=time.time() # counting time
chosen_language=input("Choose the language that your cards will be translated (ex:pt,fr,en): ")
user_message="What is the name of your Anki User "
user_message=translator.translate(user_message, src="en", dest=chosen_language)
usuario=input(f"{user_message.text} : ")
audio_path=os.getenv('APPDATA') + "\\" +"Anki2" + "\\" + str(usuario) + "\\" + "collection.media" #anki audio path, normally is in the C drive, but you can change if you have installed Anki in other path
times_audio=0
while os.path.exists(audio_path)==0:
    times_audio+=1
    if times_audio==1: # the first time it assumes that the error is in the user's name
        error_user = translator.translate("User not found!", src="en", dest=chosen_language)
        print(Back.RED + error_user.text, end="")
        print(Style.RESET_ALL)
        usuario = input(f"{user_message.text} : ")
        audio_path = os.getenv('APPDATA') + "\\" + "Anki2" + "\\" + str(usuario) + "\\" + "collection.media"
    if times_audio>=2: # the second it assumes that the error is in the directory
        print("Maybe you have installed Anki in an alternative directory")
        audio_path=input("Please put your anki directory media, example: (C:\\Users\\os_system_user\\AppData\\Roaming\\Anki2\\user_name\\collection.media)  ")
name_deck_mensagem = translator.translate("Deck's name:  ", src="en", dest=chosen_language)
deck_name = input(name_deck_mensagem.text)
letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] # creating two random letters in the final of the decks name in order to not have two
deck_name+=letters[randint(0,25)] + letters[randint(0,25)]
path = os.getcwd() #your current directory

##Duolingo, it'll check if there's a folder named "print"
def commonelement(a,b):
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i]==b[k]:
                return "True"
                break
    return "False"

if commonelement(["prints","Prints","PRINTS"],os.listdir())=="True":
    prints_folder = path + "\\prints"
    duolingo_question_mensagem=translator.translate(
            "We found a folder named 'prints', do you want to extract the text from the 'prints'? (yes = y, no = n):  ", src="en", dest=chosen_language)
    duolingo_question=input(duolingo_question_mensagem.text)
try:
    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except:
    if duolingo_question.lower()[0]=="y":
        try:
            tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Tesseract is normally installed in the C drive
        except:
            pytesseract_error=translator.translate(
            "Erro: Tesseract-OCR not found", src="en", dest=chosen_language)
            print(Back.RED + pytesseract_error, end="")
            print(Style.RESET_ALL)
            pytesseract_noninstalled=translator.translate(
            "Maybe you have not installed Tesseract-OCR, in that case open 'https://github.com/UB-Mannheim/tesseract/wiki' and install the software. ", src="en", dest=chosen_language)
            pytesseract_error_path=translator.translate(
            "Put your directory", src="en", dest=chosen_language)
            tess.pytesseract.tesseract_cmd = input(pytesseract_error_path)
        # Creating the spreadsheet
        file = xlsxwriter.Workbook("duolingo.xlsx")
        table = file.add_worksheet()
        table.write("A1", "Front")
        table.write("B1", "Back")
        table.write("C1","Prints")
        prints=os.listdir(prints_folder) #lista com todos os prints em jpg,png...
        phrases=[]
        i=0
        textextraction_mensage= translator.translate("Extracting Text 0/2",src="en", dest=chosen_language)
        print(textextraction_mensage)
        for j in prints:
            img=Image.open(prints_folder+'\\'+ j)
            text=tess.image_to_string(img,lang='fra',config=r'--oem 3 --psm 6')
            text=text.replace("@","").replace("\\","").replace(">","").replace(")","").replace("!","I").replace('|',"").replace('.','').replace("$","").replace("(","").replace('«',"" ).replace("1","").replace("5","")
            text=text.strip()
            text=text.replace("\n"," ")
            phrases.append(text)
            img.close()
            if phrases[i] !='':
                table.write("A" + str(i+2), phrases[i])
                table.write("C"+str(i+2),str(j))
            else:
                del phrases[i]
                i=i-1
            i=i+1
        warning_duolingo = translator.translate(
            "Fill the back of the cards and verify if the phrases are correct,save,close the file and press any keyboard key to continue",
            src="en", dest=chosen_language)
        warning_duolingo = input(warning_duolingo.text)
        file.close()

table_error=0 # it gets stuck in loop until you put the right name of the excel table
while table_error==0:
        try:
            archive_name=translator.translate(
                "Name of the excel table: ",
                src="en", dest=chosen_language)
            archive_name=input(archive_name.text)
            path = os.path.join(os.getcwd(), archive_name)
            archive = pd.read_excel(path+".xlsx")
            table_error=1
        except:
            wrong_name=translator.translate("Wrong name!",src="en",dest=chosen_language)
            print(Back.RED + wrong_name.text, end="")
            print(Style.RESET_ALL)
check_message=translator.translate("Do you want to check the cards before they been save? (Yes = y No= n):  ",src="en",dest=chosen_language)
check=input(check_message.text)
archive = archive.dropna()
archive.reset_index(drop=True, inplace=True)
try: #idenfity the type of the table (standard=phrase and word,active=just one phrase and remembering how to say it in other language)
    try:
        phrases = archive[["Front"]]
        words = archive[["Back"]]
        cardtype="passive"
    except:
        phrases=archive[["Active"]]
        cardtype="active"
except: #close the code and start again
    print(Back.RED + "ERROR")
    print(Style.RESET_ALL)
    front_message=translator.translate("Your excel table don't match with any type of table, this is probably due to bad formatting", src="en", dest=chosen_language)
    print(front_message.text)
    time.sleep(10)
    c=alpha
#Check if the words are in the phrase
j=0

## This function check if a exact word is in the phrase. it will not return true if for example
## phrase= "I worked a lot today"  word=work. This is different from the build-in function in python
## work is in "I worked a lot today", it'll return True, because "work" is in "worked"
def wordinphrase(word,phrase):
    word,phrase=str(word),str(phrase)
    remove=[".",",","?","!",":",";"]
    for k in remove:
        phrase=phrase.replace(k," ")
    equal=0
    eachword=phrase.split()
    for j in eachword:
        if str(j)==str(word):
            equal+=1
    if equal==0:return False
    else: return True

if check=="y" and cardtype=='passive':
    while j<len(phrases):
        if words.iloc[j][0].lower() not in phrases.iloc[j][0].lower():
            word_notinphrase=translator.translate(f"Erro: Word not in the phrase ",src="en",dest=chosen_language)
            print(Back.RED + word_notinphrase.text,end="")
            print(Style.RESET_ALL)
            print(phrases.iloc[j][0])
            print(words.iloc[j][0])
            correctword_message = translator.translate("Correct word: ", src="en", dest=chosen_language)
            correctword=input(correctword_message.text)
            words.iloc[j][0] = correctword
            if wordinphrase(words.iloc[j][0].lower(),phrases.iloc[j][0].lower())==True:
                j+=1
        else:j+=1
translation_phrases=[]
unique_language_message=translator.translate("If there's just one unique language, type it here (Example: French=fr), if not, press any key: ",sr="en",dest=chosen_language)
unique_language=input(unique_language_message.text)
if len(unique_language)==2: # if this is a language like en,fr,pt
    languages=[]
    for k in range(len(phrases)):
        languages.append(unique_language)
try:
    alpha=languages[0]
    alpha=1 #identify if there's a unique language or not
except:
    languages=[]
    alpha=0
if cardtype=="passive": #try to identify the languages
    translation_words = []
    for j in range(len(phrases)):
        print(str(round(100 * (j / len(phrases)))) + "%")
        try:
            if alpha==0:
                languages.append((translator.detect(phrases.iloc[j][0]).lang))
            translation_phrases.append((translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language)).text)
            translation_words.append((translator.translate(words.iloc[j][0], src=str(languages[j]), dest=chosen_language)).text)
        except:
            print("Error in the translation")
            print(phrases.iloc[j][0])
            print(words.iloc[j][0])
            languages.append(input("Language: "))
            translation_phrases.append(
            translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language).text)
            translation_words.append(translator.translate(words.iloc[j][0], src=str(languages[j]), dest=chosen_language).text)
if cardtype=="active":
    for j in range(len(phrases)):
        print(str(round(100 * (j / len(phrases)))) + "%")
        try:
            if alpha==0:
                languages.append((translator.detect(phrases.iloc[j][0]).lang))
            translation_phrases.append(translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language))
        except:
            print("Error in the translation")
            print(phrases.iloc[j][0])
            languages.append(input("Language: "))
            translation_phrases.append(translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language))
print("100%")
j=0
if check.lower()=="y":
    checkphrases_message=translator.translate("Para mudar uma tradução escreva a nova tradução caso contrario deixe vazio"+"\n"+
                                              "É possível deletar um card, deletar=d"+ "\n"
                                              + "É possível voltar, voltar=b" + "\n" +
                                              "Se o idioma estiver errado, digite !l no final da tradução nova",src="pt",dest=chosen_language)
    print(checkphrases_message.text)
    while j<len(phrases):
        print("----", j,"/",len(phrases),"-----")
        print(translator.translate("Language of the card",src="en",dest=chosen_language).text,Fore.LIGHTYELLOW_EX+ languages[j],Style.RESET_ALL)
        phrasehl=phrases.iloc[j][0].split()
        stringtoprint=""
        for k in range(len(phrasehl)):
            if phrasehl[k]==words.iloc[j][0]:
                position=k
                stringtoprint+=Back.GREEN+phrasehl[k]+Style.RESET_ALL+ " "
            else: stringtoprint+=phrasehl[k] +" "
        print(stringtoprint)
        print("---"+translator.translate("Translation",src="en",dest=chosen_language).text+"---")
        translation=(translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language)).text
        translation=translation.split()
        stringtoprint=""
        interval=1
        for k in range(len(translation)):
            if k==position-interval:
                stringtoprint+=Back.BLUE + translation[k] +" "
            if k==position+interval:
                stringtoprint+=translation[k]+Style.RESET_ALL +" "
            if k not in [position-interval,position+interval]:
                stringtoprint+=translation[k]+" "
        print(stringtoprint)
        print("---" + translator.translate("Translated word", src="en", dest=chosen_language).text + "---")
        print(Back.RED + words.iloc[j][0],"=",translation_words[j],end="")
        print(Style.RESET_ALL)
        newtranslation=input(("---"+translator.translate("New translation",src="en",dest=chosen_language).text)+": ")
        if newtranslation.lower().count("!l")!=0:
            languages[j]=input(translator.translate("New language",src="en",dest=chosen_language).text+": ")
            newtranslation=newtranslation.replace("!l","")
        if len(newtranslation)!=newtranslation.count(" ") and newtranslation!="del" :
            if newtranslation.lower()!='b':
                translation_words[j]=newtranslation
        if newtranslation.lower()=="d":
            phrases = phrases.drop(j)
            phrases.reset_index(drop=True, inplace=True)
            words=words.drop(j)
            words.reset_index(drop=True, inplace=True)
            del translation_words[j]
            del translation_phrases[j]
        if newtranslation!="d": j+=1
        if newtranslation=="b":
            j=j-2
            try:newtranslation=translation_phrases[j+2]
            except:newtranslation=translation_phrases[j]
print("Audios...(2/2)")
for j in range(0, len(phrases)):
    print(str(round(100*(j/len(phrases)))) + "%")
    try:
        tts = gTTS(str(words.iloc[j][0]), lang=languages[j])
        tts.save(audio_path + "\\" +str(deck_name) + "word" + str(j) + '.mp3')
        tts = gTTS(str(phrases.iloc[j][0]), lang=languages[j])
        tts.save(audio_path + "\\" + str(deck_name) + "phrase" + str(j) + '.mp3')
    except:pass
print("100%")

id_deck =1_335_132_555 #id fixo para não mudar o


deck = genanki.Deck(
    id_deck,
    deck_name)


my_model = genanki.Model(
    id_deck,
    'CardMaker Q&A',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'MyMedia'},  # ADD THIS
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}<br>{{MyMedia}}',  # AND THIS
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])
#Color of the cards
print(translator.translate("Colors that are in the code: ",src="en",dest=chosen_language).text)
print("blue,green,red,purple,pink,yellow")
custom_color_message=translator.translate("You can select the color of the highlighted word, if you want to create a new color press yes=y. If you want a predetermined color write the name of the color",src="en",dest=chosen_language)
color=input(custom_color_message.text+": ")
if color=="y":
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.rapidtables.com/web/color/RGB_Color.html")
    except: print("https://www.rapidtables.com/web/color/RGB_Color.html")
    R=input("Red: ")
    G=input("Green: ")
    B=input("Blue: ")
    driver.close()
    color=f'<span style="color: rgb({R}, {G}, {B});">'
else: #you can add a new color, just put it here in the dictionary
    colors_rgb = {'green': '<span style="color: rgb(81, 255, 37);">', 'red':'<span style="color: rgb(228, 14, 14);">', 'blue':'<span style="color: rgb(18, 166, 252);">',
                  'yellow':'<span style="color: rgb(249, 255, 54);">', 'purple':'<span style="color: rgb(198, 38, 255);">', 'pink':'<span style="color: rgb(255, 14, 192);">', }
    color=colors_rgb[color]

for i in range(0, len(phrases)):
    if cardtype=="active":
        pass
    if cardtype=="passive":
        note = genanki.Note(model=my_model,
                fields=["","[" + "sound:" + str(deck_name) + "word" + str(i) + ".mp3" + "]" + color + '<u><b><i>' + str(" "+ words.iloc[i][0]).replace("'","")+ '</i></b></u></span>'  " == " + str(
                            translation_words[i]), "[" + "sound:" + str(deck_name) + "phrase" + str(i) + ".mp3" + "]" + color + '<u><b><i>' + str(words.iloc[i][0]).replace("'","")+ '</i></b></u></span>' + ". " +
                    phrases.iloc[i][0]],tags=[str(languages[i]),"cardmaker"])
        deck.add_note(note)
genanki.Package(deck).write_to_file(str(deck_name) +'.apkg')

tf=time.time()

deltat=tf -t_o

print(f"Congratulations, {len(words)} flashcards! In {round(deltat/60,1)} minutes, {round(len(words)/deltat,2)}flashcards per minute")
time.sleep(120)