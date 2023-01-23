#modules in alphabetic order
from colorama import Fore,Back,Style,init #use colors
import genanki #integration with anki
from googletrans import Translator #translate the phrases
from gtts import gTTS #generate audios
import os #get the file directories
from multiprocessing import cpu_count #know the exact number of cores
import pandas as pd #handle the excel tables
from selenium import webdriver # open color custom website
import time #count the amount of time used in creating cards
from threading import Thread #acelerate the code
import xlsxwriter #excel tables

translator = Translator() #start translator
init(strip=False) #colors in the terminal
t_o=time.time() # counting time
threads=round(cpu_count()/2) #using half of the threads to acelerate the code...you can change this if you want

chosen_language=input("Choose the language that your cards will be translated (ex:pt,fr,en): ")
#chosen_language="pt"
user_message="What is the name of your Anki User "
user_message=translator.translate(user_message, src="en", dest=chosen_language)
usuario=input(f"{user_message.text} : ")
#usuario="Dutra"
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
        audio_path=input("Please put your anki directory media, example: (C:\\Users\\os_system_user\\AppData\\Roaming\\Anki2\\user_name\\collection.media)  ")path = os.getcwd() #your current directory

filesinthedirectory=[j for j in os.listdir()]#if j[-5:-1]==".xlsx"] #show the excel tables that are in your current folder
tablesinthedirectory=[]
for j in filesinthedirectory:
    try:
        if j[-5::]==".xlsx" and j[0:2]!="~$": #the ~$ exclude temporary files
            tablesinthedirectory.append(j)
    except:pass
print(tablesinthedirectory)

table_error=0 # it gets stuck in loop until you put the right name of the excel table
while table_error==0:
        try:
            archive_name=translator.translate(
                "Name of the excel table: ",
                src="en", dest=chosen_language)
            archive_name=input(archive_name.text)
            path = os.path.join(os.getcwd(), archive_name+".xlsx")
            archive = pd.read_excel(path)
            table_error=1
        except:
            pass
            wrong_name=translator.translate("Wrong name!",src="en",dest=chosen_language)
            print(Back.RED + wrong_name.text, end="")
            print(Style.RESET_ALL)
deck_name = archive_name
u=""
counter=0
while os.path.exists(os.getcwd()+"\\"+deck_name+u+".apkg")==True:
    counter+=1
    u=str(counter)
deck_name+=str(u)
check_message=translator.translate("Do you want to check the cards before they been save? (Yes = y No= n)",src="en",dest=chosen_language)
check=input(check_message.text+": ")
archive = archive.dropna()
archive.reset_index(drop=True, inplace=True)
try: #idenfity the type of the table
    try:
        phrases = archive[["Front"]]
        words = archive[["Back"]]
        cardtype="vocabulary"
    except:
        try:
            phrases=archive[["Speaking"]]
            cardtype="speaking"
        except:
            phrases=archive[["Writing"]]
            cardtype="writing"
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
    word,phrase=str(word).lower(),str(phrase).lower()
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

if check=="y" and cardtype=='vocabulary':
    while j<len(phrases):
        if words.iloc[j][0].lower().replace(".","").replace(",","").replace(";","").replace(":","") not in phrases.iloc[j][0].lower().replace(".","").replace(",","").replace(";","").replace(":",""):
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
translation_phrases = []
translation_words=[]
temp1=[]
temp2=[]
numbers=[]
print(translator.translate("Translating...(1/2)",src="en",dest=chosen_language).text)
def translate(k,threads):
    global phrases,words,chosen_language,alpha,translation_words,translation_phrases,languages
    for j in range(k,len(phrases),threads):
        try:
            if alpha==0:
                    languages.append((translator.detect(phrases.iloc[j][0]).lang))
            t1=str(j)+" "+(translator.translate(phrases.iloc[j][0], src=str(languages[j]), dest=chosen_language)).text
            translation_phrases.append(t1)
            temp1.append(str(j)+" "+phrases.iloc[j][0])
            numbers.append(str(j))
            if cardtype=="vocabulary":
                t2=str(j)+" "+ (translator.translate(words.iloc[j][0], src=str(languages[j]), dest=chosen_language)).text
                translation_words.append(t2)
                temp2.append(str(j)+" "+words.iloc[j][0])
        except:pass
processes=[]
for n in range(threads):
    p=Thread(target=translate,args=[n,threads])
    p.start()
    processes.append(p)
for process in processes:
    process.join()
translation_phrases=sorted(translation_phrases)
phrases=sorted(temp1)
numbers=sorted(numbers)
if cardtype=="vocabulary":
    translation_words=sorted(translation_words)
    words=sorted(temp2)
for j in range(len(phrases)):
    try:
        translation_phrases[j]=((translation_phrases[j]).replace(numbers[j],""))
        phrases[j]=(phrases[j].replace(numbers[j],""))
        if cardtype=="vocabulary":
            translation_words[j]=((translation_words[j]).replace(numbers[j],""))
            words[j]=(words[j].replace(numbers[j],""))
    except:pass
j=0
if check.lower()=="y" and cardtype=="vocabulary":
    checkphrases_message=translator.translate("Para mudar uma tradução escreva a nova tradução caso contrario deixe vazio"+"\n"+
                                              "É possível deletar um card, deletar=d"+ "\n"
                                              + "É possível voltar, voltar=b" + "\n" +
                                              "Se o idioma estiver errado, digite !l no final da tradução nova",src="pt",dest=chosen_language)
    print(checkphrases_message.text)
    while j<len(phrases):
        print("----", j+1,"/",len(phrases),"-----")
        print(translator.translate("Language of the card",src="en",dest=chosen_language).text,Fore.LIGHTYELLOW_EX+ languages[j],Style.RESET_ALL)
        phrasehl=phrases[j].split()
        stringtoprint=""
        for k in range(len(phrasehl)):
            if phrasehl[k]==words[j].replace(" ",""):
                position=k
                stringtoprint+=Back.GREEN+phrasehl[k]+Style.RESET_ALL+ " "
            else: stringtoprint+=phrasehl[k] +" "
        print(stringtoprint)
        print("---"+translator.translate("Translation",src="en",dest=chosen_language).text+"---")
        translation=(translator.translate(phrases[j], src=str(languages[j]), dest=chosen_language)).text
        translation=translation.split()
        stringtoprint=""
        interval=1
        for k in range(len(translation)):
            try:
                if k==position-interval:
                    stringtoprint+=Back.BLUE + translation[k] +" "
                if k==position+interval:
                    stringtoprint+=translation[k]+Style.RESET_ALL +" "
                if k not in [position-interval,position+interval]:
                    if k == len(translation)-1:
                        stringtoprint += translation[k] + Style.RESET_ALL
                    else:
                        stringtoprint += translation[k] + " "
            except:
                stringtoprint+=translation[k]+" "
        print(stringtoprint)
        print("---" + translator.translate("Translated word", src="en", dest=chosen_language).text + "---")
        print(Back.RED + words[j],"=",translation_words[j],end="")
        print(Style.RESET_ALL)
        newtranslation=input(("---"+translator.translate("New translation",src="en",dest=chosen_language).text)+": ")
        if newtranslation=="s":
            savefile = xlsxwriter.Workbook(deck_name+"stopped"+".xlsx")
            stoppedtable = savefile.add_worksheet()
            stoppedtable.write("A1", "Front")
            stoppedtable.write("B1", "Back")
            stop = j
            for k in range((len(phrases)-j)):
                try:
                    stoppedtable.write("A"+str(j+k),phrases[j+k])
                    stoppedtable.write("B"+str(j+k),words[j+k])
                except:pass
            j=len(phrases)+2
            savefile.close()
            break
        if newtranslation.lower().count("!l")!=0:
            languages[j]=input(translator.translate("New language",src="en",dest=chosen_language).text+": ")
            newtranslation=newtranslation.replace("!l","")
        if len(newtranslation)!=newtranslation.count(" ") and newtranslation!="del" :
            if newtranslation.lower()!='b':
                translation_words[j]=newtranslation
        if newtranslation.lower()=="d":
            del phrases[j], words[j],translation_words[j],translation_phrases[j]
        if newtranslation!="d": j+=1
        if newtranslation=="b":
            j=j-2
            try:newtranslation=translation_phrases[j+2]
            except:newtranslation=translation_phrases[j]
try:
    gamma=stop
except:
    stop=len(phrases)

if check.lower()=="y" and cardtype in ["speaking","writing"]:
    checkfile = xlsxwriter.Workbook(deck_name + "_checkspeaking" + ".xlsx")
    checktable = checkfile.add_worksheet()
    checktable.write("A1", "speakingorwriting")
    checktable.write("B1", "Translation")
    for j in range(stop):
        checktable.write("A"+str(j+2),phrases[j])
        checktable.write("B"+str(j+2),translation_phrases[j])
    checkfile.close()
    input(translator.translate(f"Open the excel table and check if there's any mistake, press any key to continue",src="en",dest=chosen_language).text)
    path = os.path.join(os.getcwd(), deck_name+"_checkspeaking" + ".xlsx")
    excelcheck = pd.read_excel(path)
    excelcheck = excelcheck.dropna()
    excelcheck.reset_index(drop=True, inplace=True)
    phrases = excelcheck[["speakingorwriting"]]
    translation_phrases = excelcheck[["Translation"]]
    templist1=[]
    templist2=[]
    for k in range(len(translation_phrases)):
        templist1.append(translation_phrases.iloc[k][0])
        templist2.append(phrases.iloc[k][0])
    translation_phrases=templist1
    phrases=templist2
    stop=len(phrases)
print(translator.translate("Audios...(2/2)",src="en",dest=chosen_language).text)
def audiogenerator(k,threads):
    global words,phrases,languages,audio_path,deck_name,stop
    for j in range(k, stop,threads):
        try:
            if cardtype == "vocabulary":
                tts = gTTS(str(words[j])+"."+str(phrases[j]), lang=languages[j])
                tts.save(audio_path + "\\" + str(deck_name) + "phrase" + str(j) + '.mp3')
                tts = gTTS(str(words[j]), lang=languages[j])
                tts.save(audio_path + "\\" + str(deck_name) + "word" + str(j) + '.mp3')
            if cardtype in ["speaking","writing"]:
                tts = gTTS(str(phrases[j]), lang=languages[j])
                tts.save(audio_path + "\\" + str(deck_name) + "phrase" + str(j) + '.mp3')
        except:pass

processes=[]
for n in range(threads):
    p=Thread(target=audiogenerator,args=[n,threads])
    p.start()
    processes.append(p)
for process in processes:
    process.join()
if cardtype=="vocabulary" or "speaking":
    id_deck =1_335_132_555
if cardtype=="writing":
    id_deck=2_343_103_533
deck = genanki.Deck(
    id_deck,
    deck_name)
if cardtype in ["vocabulary","speaking"]:
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
if cardtype=="writing":
    my_model = genanki.Model(
        id_deck,
        'CardMaker Type in the Answer',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'MyMedia'},  # ADD THIS
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br> {{type:Answer}}',  # AND THIS
                'afmt': '{{FrontSide}}{{MyMedia}}',
            },
        ])
#Color of the cards
print(translator.translate("Colors that are in the code: ",src="en",dest=chosen_language).text)
print("blue,green,red,purple,pink,yellow")
custom_color_message=translator.translate("You can select the color of the highlighted word, if you want to create a new color press yes=y. If you want a predetermined color write the name of the color",src="en",dest=chosen_language)
colorforall=input(custom_color_message.text+": ")
#color_scheme={"es":"red","fr":"blue","en":"green","la":"yellow"} # I use a specific color for each language
colors_rgb = {'green': '<span style="color: rgb(81, 255, 37);">', 'red': '<span style="color: rgb(228, 14, 14);">',
              'blue': '<span style="color: rgb(18, 166, 252);">',
              'yellow': '<span style="color: rgb(249, 255, 54);">',
              'purple': '<span style="color: rgb(198, 38, 255);">',
              'pink': '<span style="color: rgb(255, 14, 192);">', }
color=[]
for j in range(stop):
    try:
        color.append(colors_rgb[color_scheme[languages[j]]])
    except: color.append(colors_rgb[colorforall])
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
if type(color)=="str": #you can add a new color, just put it here in the dictionary
    try:
        alpha=colors_rgb[color]
    except: color=colors_rgb["red"]

for i in range(0, stop):
    try:
        if cardtype=="speaking":
            note = genanki.Note(model=my_model,
                                fields=[color[i] + '<u><b><i>' +" ["+ languages[i]+"] "+'</i></b></u></span>' +
                                        translation_phrases[i],"[" + "sound:" + str(deck_name) + "phrase" + str(i) + ".mp3" + "]" + str(" " + phrases[i])
                                    ,"" ],tags=[str(languages[i]), "cardmaker"])
        if cardtype=="vocabulary":
            note = genanki.Note(model=my_model,
                    fields=["","[" + "sound:" + str(deck_name) + "word" + str(i) + ".mp3" + "]" + color[i] + '<u><b><i>' + str(" "+ words[i]) + '</i></b></u></span>'  " == " + str(
                                translation_words[i]), "[" + "sound:" + str(deck_name) + "phrase" + str(i) + ".mp3" + "]" + color[i] + '<u><b><i>' +words[i]+ '</i></b></u></span>' + ". " +
                        phrases[i]],tags=[str(languages[i]),"cardmaker"])
        if cardtype=="writing":
            note = genanki.Note(model=my_model,
                                fields=[color[i] + '<u><b><i>' + " [" + languages[i] + "] " + '</i></b></u></span>' +
                                        translation_phrases[i], phrases[i],"[" + "sound:" + str(deck_name) + "phrase" + str(i) + ".mp3" + "]"], tags=[str(languages[i]), "cardmaker"])
        deck.add_note(note)
    except:pass

genanki.Package(deck).write_to_file(str(deck_name) +'.apkg')

tf=time.time()

deltat=tf -t_o

print(f"Congratulations, {len(phrases)} flashcards in {round(deltat/60,1)} minutes! {round(60*len(phrases)/deltat,1)} flashcards per minute")
