import pandas as pd
from googletrans import Translator
from gtts import gTTS
import genanki
import os
import time
from colorama import Fore,Back,Style
import colorama
import pytesseract as tess
from PIL import Image,ImageEnhance
import PIL
import xlsxwriter


error=0

usuario=input("Qual é o nome do seu usuario Anki:  ")
audios_caminho=os.getenv('APPDATA') + "\\" +"Anki2" + "\\" + str(usuario) + "\\" + "collection.media"
while os.path.exists(audios_caminho)==0:
    print(Back.RED + "Usuario não encontrado!", end="")
    print(Style.RESET_ALL)
    usuario = input("Qual é o nome do seu usuario Anki:  ")
    audios_caminho = os.getenv('APPDATA') + "\\" + "Anki2" + "\\" + str(usuario) + "\\" + "collection.media"
nome_deck = input("Escolha um nome para o deck:   ")
vezes=(os.listdir()).count(nome_deck)
if vezes!=0:nome_deck+=f"({vezes})"
caminho = os.getcwd()
##Print converter

if 'prints' in os.listdir():
    pasta_prints = caminho + "\\prints"
    if len(os.listdir(pasta_prints))!=0:
        duolingo_pergunta=input("Detecamos uma pasta chamada prints, deseja extrair texto dos prints? ")
if 'Prints' in os.listdir():
    pasta_prints = caminho + "\\Prints"
    if len(os.listdir(pasta_prints))!=0:
        duolingo_pergunta = input("Detecamos uma pasta chamada prints, deseja extrair texto dos prints? ")
if 'PRINTS' in os.listdir():
    pasta_prints = caminho + "\\PRINTS"
    if len(os.listdir(pasta_prints))==0:
        duolingo_pergunta = input("Detecamos uma pasta chamada prints, deseja extrair texto dos prints? ")
if duolingo_pergunta.lower()[0:1]=="s":
    colorama.init(strip=False)
    usuario = os.getlogin()
    tess.pytesseract.tesseract_cmd = r'C:\Users\dutra\AppData\Local\Tesseract-OCR\tesseract.exe'.replace("dutra",usuario)
    # Comeco da criação da tabela
    file = xlsxwriter.Workbook("duolingo.xlsx")
    table = file.add_worksheet()
    table.write("A1", "Frente")
    table.write("B1", "Verso")
    prints=os.listdir(pasta_prints) #lista com todos os prints em jpg,png...
    frases=[]
    i=0
    print("Extraindo Texto(0/2)...")
    for j in prints:
        print(round(100*i/len(prints)),"%")
        img=Image.open(pasta_prints+'\\'+ j)
        text=tess.image_to_string(img,lang='fra',config=r'--oem 3 --psm 6')
        text=text.replace("@","").replace("\\","").replace(">","").replace(")","").replace("!","I").replace('|',"").replace('.','').replace("$","").replace("(","").replace('«',"" ).replace("1","").replace("5","")
        text=text.strip()
        text=text.replace("\n"," ")
        frases.append(text)
        img.close()
        if frases[i] !='':
            table.write("A" + str(i+2), frases[i])
        else:
            del frases[i]
            i=i-1
        i=i+1
    file.close()
time.sleep(1)
##Print Converter


t_o=time.time()

try:
    nome_arquivo = "duolingo.xlsx"
    caminho = os.path.join(os.getcwd(), nome_arquivo)
    arquivo = pd.read_excel(caminho)
    try:
        nome_arquivo = "anki.xlsx"
        caminho = os.path.join(os.getcwd(), nome_arquivo)
        arquivo = pd.read_excel(caminho)
    except:
            nome_arquivo = "Anki.xlsx"
            caminho = os.path.join(os.getcwd(), nome_arquivo)
            arquivo = pd.read_excel(caminho)

except:
    while error==0:
        try:
            nome_arquivo=input("Não foi possível encontrar uma tabela chamada Anki, ou duolingo "
                           "por favor coloque o nome da sua tabela:  ")
            caminho = os.path.join(os.getcwd(), nome_arquivo)
            arquivo = pd.read_excel(caminho+".xlsx")
            error=1
        except:
            print(Back.RED + "Nome Errado!", end="")
            print(Style.RESET_ALL)
checar=input("Deseja checar os cards antes de salvos? (S=Sim,N=Não)  ")


arquivo = arquivo.dropna()
arquivo.reset_index(drop=True, inplace=True)
try:
    frases = arquivo[["Frente"]]
    palavras = arquivo[["Verso"]]
except:
    print(Back.RED + "ERROR")
    print(Style.RESET_ALL)
    print("Coloque a primeira coluna como Frente e a segunda como Verso")
    time.sleep(10)
    c=alpha
#Checar se a palavra existe na frase
for j in range(len(frases)):
    if palavras.iloc[j][0] not in frases.iloc[j][0]:
        print(Back.RED + "ERROR: Palavra não está na frase",end="")
        print(Style.RESET_ALL)
        print(frases.iloc[j][0])
        print(palavras.iloc[j][0])
        try:print(eta)
        except:eta=input("Deseja continuar a checagem? ")
        if eta.lower()[0:1] == "n":
            break
        fezmerda=input("Coloque a palavra certa: ")
        palavras.iloc[j][0]=fezmerda

## Consertar tabela Kindle
if int(str(arquivo.iloc[0:5]).count("Location:")) !=0:
    for u in range(0, frases.shape[0] // 2):
        frases = frases.drop(2 * u + 1)
    frases.reset_index(drop=True, inplace=True)

traducao = []
translator = Translator()
idiomas_frase = []
idiomas_palavras=[]
print("Traduzindo...(1/2)")
j=-1
for j in range(len(frases)): #Verificar idioma e traduzir
    print(str(round(100 * (j / len(frases)))) + "%")
    idioma_originalfrase = translator.detect(frases.iloc[j]).lang
    idiomas_frase.append(idioma_originalfrase)
    idioma_originalpalavra = (translator.detect(palavras.iloc[j])).lang
    idiomas_palavras.append(idioma_originalpalavra)
    if type(idioma_originalfrase) == list:
        idiomas_frase[j]=idiomas_frase[j][0]
    if type(idioma_originalpalavra) == list:
        idiomas_palavras[j]=idiomas_palavras[j][0]
    if idiomas_frase[j]=="pt":
        traducao.append(palavras.iloc[j][0])
    else:
        try:
            idiomas_palavras.remove(idioma_originalpalavra)
            idiomas_palavras.append(idiomas_frase[j])
            trad = translator.translate(palavras.iloc[j][0], src=str(idiomas_palavras[j]), dest="pt")
            traducao.append(trad.text)
        except: traducao.append("Não foi possível identificar o idioma")
print("100%")
j=0
if checar.lower()=="s":
    print("Processo de Checagem: Para mudar uma tradução basta escrever a nova tradução, caso o contrário, deixe em branco")
    print("É possível deletar um card, escreva Deletar")
    print("É possível voltar, digite Voltar")
    print("Caso o idioma esteja errado, coloque !frente ou !verso, caso sejam ambos, !fudeu")
if checar.lower()[0:1]=="s":
    while j<len(frases):
        print("----Frase", j,"/",len(frases),"-----")
        print("Frente em ",Fore.LIGHTYELLOW_EX+ idiomas_frase[j],Style.RESET_ALL, "e Verso em",Fore.LIGHTYELLOW_EX+  idiomas_palavras[j],Style.RESET_ALL)
        print(Back.BLUE + frases.iloc[j][0],end='')
        print(Style.RESET_ALL)
        print("---Tradução Inteira---")
        try:print(Back.GREEN+translator.translate(frases.iloc[j][0], src=str(idiomas_frase[j]), dest="pt").text,end='')
        except:pass
        print(Style.RESET_ALL)
        print("---Tradução Parcial---")
        print(Back.RED + palavras.iloc[j][0],"=",traducao[j],end="")
        print(Style.RESET_ALL)
        palavranova=input("Substituir tradução:  ")
        if palavranova.lower().count("!frente")!=0 or palavranova.lower().count("!frase")!=0: idiomas_frase[j]=input("Frente Idioma: ")
        if palavranova.lower().count("!verso")!=0 or palavranova.lower().count("!palavra")!=0:idiomas_palavras[j]=input("Verso Idioma: ")
        if palavranova.lower().count("!fudeu")!=0:
            idiomas_frase[j] = input("Frente Idioma: ")
            idiomas_palavras[j] = input("Verso Idioma: ")
        palavranova=palavranova.replace("!verso","").replace("!frente","").replace("!fudeu","").replace("palavra","").replace("frase","").title()
        if len(palavranova)!=palavranova.count(" ") and palavranova[0:3].lower() !="del" :
            if palavranova.lower()!='voltar':
                traducao[j]=palavranova
        if palavranova[0:3].lower()=="del":
            frases = frases.drop(j)
            frases.reset_index(drop=True, inplace=True)
            palavras =palavras.drop(j)
            palavras.reset_index(drop=True, inplace=True)
            del traducao[j]
        if palavranova[0:3].lower()!="del": j+=1
        if palavranova.lower()=="voltar":
            j=j-2
            try:palavranova=traducao[j+2]
            except:palavranova=traducao[j]
flista = frases.values.tolist()
palavras = palavras.values.tolist()
print("Audios...(2/2)")
for j in range(0, len(frases)):
    print(str(round(100*(j/len(frases)))) + "%")
    try:
        if idiomas_palavras[j] =="pt" :
            c=0
        else:
            tts = gTTS(str(palavras[j]), lang=idiomas_palavras[j])
            tts.save(audios_caminho + "\\" +str(nome_deck) + "palavra" + str(j) + '.mp3')
        if idiomas_frase[j]=="pt" :
            c=0
        else:
            tts = gTTS(str(palavras[j])+"." +
                str(flista[j]).replace("»", "").replace("xa0", "").replace("\\", "").replace("]",
                                                                                             "").replace(
                    "[", "").replace(".", ""), lang=idiomas_frase[j])
            tts.save(audios_caminho + "\\" + str(nome_deck) + "frase" + str(j) + '.mp3')
    except:
        c=0
print("100%")

flista = frases.values.tolist()

id_deck =1_335_132_555 #id fixo para não mudar o


deck = genanki.Deck(
    id_deck,
    nome_deck)


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

green='<span style="color: rgb(81, 255, 37);">'

for i in range(0, len(flista)):
    if idiomas_palavras[j]=="pt":
        nota = genanki.Note(
            model=my_model,
            fields=[str(
                flista[i]).replace("»", "").replace("xa0", "").replace("\\", "").replace("]", "").replace("[",
                                                                                                          "").replace(
                ".", ""),str(palavras[i]) + ".", ""])
        deck.add_note(nota)
    else:
        if str(palavras[i]).count(" ")>=3: #Caso em que a palavra é na verdade uma frase
            nota = genanki.Note(
                model=my_model,
                fields=[str(
                            flista[i]).replace("»", "").replace("xa0", "").replace("\\", "").replace("]", "").replace("[",
                                                                                                                      "").replace(
                            ".", ""),
                        "[" + "sound:" + str(nome_deck) + "palavra" + str(i) + ".mp3" + "]" + str(palavras[i]) + ".","" ])
            deck.add_note(nota)
        else:
            nota = genanki.Note(
                model=my_model,
                fields=["", "[" + "sound:" + str(nome_deck) + "palavra" + str(i) + ".mp3" + "]" + green + '<u><b><i>' + str(palavras[i])+ '</i></b></u></span>'  " == " + str(
                            traducao[i]), "[" + "sound:" + str(nome_deck) + "frase" + str(i) + ".mp3" + "]" + green + '<u><b><i>' + str(palavras[i])+ '</i></b></u></span>' + "." + str(
                    flista[i]).replace("»", "").replace("xa0", "").replace("\\", "").replace("]", "").replace("[", "").replace(
                    ".", "")])
            deck.add_note(nota)
genanki.Package(deck).write_to_file(str(nome_deck) +'.apkg')


tf=time.time()

deltat=tf -t_o

if deltat>60:
    deltat=str(round(deltat//60)) + " Minutos e " + str(round(deltat%60)) + " Segundos"

else: deltat=round(deltat)
print(f"Parabéns! Você fez {len(palavras)} flashcards! Em somente {deltat} segundos ")
time.sleep(20)