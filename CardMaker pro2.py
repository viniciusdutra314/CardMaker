import pandas as pd
from googletrans import Translator
from gtts import gTTS
import genanki
import os
import time
from colorama import Fore,Back,Style
import colorama
import pytesseract as tess
from random import randint
from PIL import Image
import xlsxwriter
translator = Translator() #start translator
colorama.init(strip=False) #colors in the terminal
t_o=time.time() # counting time
chosen_language=input("Choose the language that your cards will be translated (ex:pt,fr,en): ")
error=0
user_message="What is the name of the Anki User"
user_message=translator.translate(user_message, src="en", dest=chosen_language)
usuario=input(f"{user_message.text} : ")
audio_path=os.getenv('APPDATA') + "\\" +"Anki2" + "\\" + str(usuario) + "\\" + "collection.media" #anki audio path
times_audio=0
while os.path.exists(audio_path)==0:
    times_audio+=1
    error_user = translator.translate("User not found!", src="en", dest=chosen_language)
    print(Back.RED + error_user.text, end="")
    print(Style.RESET_ALL)
    if times_audio>=2:
        print("Maybe you have installed Anki in an alternative directory, z")
    usuario=input(f"{user_message.text} : ")
    audio_path = os.getenv('APPDATA') + "\\" + "Anki2" + "\\" + str(usuario) + "\\" + "collection.media"
nome_deck_mensagem = translator.translate("Escolha um nome para o [Deck]:  ", src="pt", dest=idioma_escolhido)
nome_deck = input(nome_deck_mensagem.text)
letras=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
nome_deck+=letras[randint(0,25)] + letras[randint(0,25)]
vezes=(os.listdir()).count(nome_deck)
if vezes!=0:nome_deck+=f"({vezes})"
caminho = os.getcwd()
##Print converter

if 'prints' in os.listdir():
    pasta_prints = caminho + "\\prints"
    if len(os.listdir(pasta_prints))!=0:
        duolingo_pergunta_mensagem=translator.translate(
            "Detecamos uma pasta chamada [prints], deseja extrair texto dos [Prints]? ", src="pt", dest=idioma_escolhido)
        duolingo_pergunta=input(duolingo_pergunta_mensagem.text)
if 'Prints' in os.listdir():
    pasta_prints = caminho + "\\Prints"
    if len(os.listdir(pasta_prints))!=0:
        duolingo_pergunta_mensagem = translator.translate(
            "Detecamos uma pasta chamada [prints], deseja extrair texto dos [Prints]? ", src="pt", dest=idioma_escolhido)
        duolingo_pergunta = input(duolingo_pergunta_mensagem.text)
if 'PRINTS' in os.listdir():
    pasta_prints = caminho + "\\PRINTS"
    if len(os.listdir(pasta_prints))==0:
        duolingo_pergunta_mensagem = translator.translate(
            "Detecamos uma pasta chamada [prints], deseja extrair texto dos [Prints]?  ", src="pt", dest=idioma_escolhido)
        duolingo_pergunta = input(duolingo_pergunta_mensagem.text)
try:
    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseasdact.exe'
except:
    if duolingo_pergunta.lower()=="s":
        try:
            tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseasdact.exe'
        except:
            pytesseract_error=translator.translate(
            "Erro: PyTesseract não foi encontrado", src="pt", dest=idioma_escolhido)
            duolingo_pergunta=input(duolingo_pergunta_mensagem.text)
            print(Back.RED + pytesseract_error, end="")
            print(Style.RESET_ALL)
            pytesseract_error_diretorio=translator.translate(
            "Coloque o diretorio", src="pt", dest=idioma_escolhido)
            tess.pytesseract.tesseract_cmd = input("Coloque o diretorio ")
        # Comeco da criação da tabela
        file = xlsxwriter.Workbook("duolingo.xlsx")
        table = file.add_worksheet()
        table.write("A1", "Front")
        table.write("B1", "Back")
        table.write("C1","nome do print")
        prints=os.listdir(pasta_prints) #lista com todos os prints em jpg,png...
        frases=[]
        i=0
        print("Extraindo Texto(0/2)...")
        for j in prints:
            img=Image.open(pasta_prints+'\\'+ j)
            text=tess.image_to_string(img,lang='fra',config=r'--oem 3 --psm 6')
            text=text.replace("@","").replace("\\","").replace(">","").replace(")","").replace("!","I").replace('|',"").replace('.','').replace("$","").replace("(","").replace('«',"" ).replace("1","").replace("5","")
            text=text.strip()
            text=text.replace("\n"," ")
            frases.append(text)
            img.close()
            if frases[i] !='':
                table.write("A" + str(i+2), frases[i])
                table.write("C"+str(i+2),str(j))
            else:
                del frases[i]
                i=i-1
            i=i+1
        file.close()
time.sleep(1)
##Print Converter
try:
    if duolingo_pergunta.lower()[0]=="s" :
        os.system("start EXCEL.EXE duolingo.xlsx")
        cuidado_mensagem=translator.translate(
        "Complete o verso dos cards e verifique se as frentes estão corretas, salve, feche e quando determinar pressione [Enter] ", src="pt", dest=idioma_escolhido)
        cuidado=input(cuidado_mensagem.text)
except:pass


while error==0:
        try:
            nome_arquivo=input("Coloque o nome da Tabela Excel ")
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
    frases = arquivo[["Front"]]
    palavras = arquivo[["Back"]]
except:
    print(Back.RED + "ERROR")
    print(Style.RESET_ALL)
    front_mensagem=translator.translate("Coloque a primeira coluna como [FRONT] e a segunda como [BACK]", src="pt", dest=idioma_escolhido)
    print(front_mensagem.text)
    time.sleep(10)
    c=alpha #fechar o programa
#Checar se a palavra existe na frase
for j in range(len(frases)):
    if palavras.iloc[j][0].lower() not in frases.iloc[j][0].lower():
        if frases.iloc[j][0].lower()!="active":
            palavra_nao_frase=translator.translate("Erro: Palavra não está no [Front]",src="pt",dest=idioma_escolhido)
            print(Back.RED + palavra_nao_frase.text,end="")
            print(Style.RESET_ALL)
            print(frases.iloc[j][0])
            print(palavras.iloc[j][0])
            try:print(eta)
            except:
                checagem_mensagem=translator.translate("Deseja continuar a checagem? " ,src="pt",dest=idioma_escolhido)
                eta=input(checagem_mensagem.text)
            if eta.lower()[0:1] == "n":
                break
            fezmerda_mensagem = translator.translate("Coloque a palavra certa ", src="pt", dest=idioma_escolhido)
            fezmerda=input(fezmerda_mensagem.text)
            palavras.iloc[j][0]=fezmerda

## Consertar tabela Kindle
if int(str(arquivo.iloc[0:5]).count("Location:")) !=0:
    for u in range(0, frases.shape[0] // 2):
        frases = frases.drop(2 * u + 1)
    frases.reset_index(drop=True, inplace=True)

traducao = []
idiomas_frase = []
idiomas_palavras=[]
idioma_unico_mensagem=translator.translate("Caso seja um idioma só, coloque ele aqui (Exemplo: francês=fr): ",sr="pt",dest=idioma_escolhido)
idioma_unico=input(idioma_unico_mensagem.text)
print("Traduzindo...(1/2)")
j=-1
for j in range(len(frases)): #Verificar idioma e traduzir
    print(str(round(100 * (j / len(frases)))) + "%")
    if idioma_unico=="": idioma_originalfrase = translator.detect(frases.iloc[j]).lang
    else:idioma_originalfrase=idioma_unico
    idiomas_frase.append(idioma_originalfrase)
    if idioma_unico=="": idioma_originalpalavra = translator.detect(frases.iloc[j]).lang
    else:idioma_originalpalavra=idioma_unico
    idiomas_palavras.append(idioma_originalpalavra)
    if type(idioma_originalfrase) == list:
        idiomas_frase[j]=idiomas_frase[j][0]
    if type(idioma_originalpalavra) == list:
        idiomas_palavras[j]=idiomas_palavras[j][0]
    if idiomas_frase[j]==idioma_escolhido:
        traducao.append(palavras.iloc[j][0])
    else:
        try:
            idiomas_palavras.remove(idioma_originalpalavra)
            idiomas_palavras.append(idiomas_frase[j])
            trad = translator.translate(palavras.iloc[j][0], src=str(idiomas_palavras[j]), dest=idioma_escolhido)
            traducao.append(trad.text)
        except:
            traducao_mensagem=translator.translate("Não foi possível identificar o idioma",src="pt",dest=idioma_escolhido)
            traducao.append(traducao_mensagem.text)
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
        try:print(Back.GREEN+translator.translate(frases.iloc[j][0], src=str(idiomas_frase[j]), dest=idioma_escolhido).text,end='')
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
        if idiomas_palavras[j] ==idioma_escolhido :
            c=0
        else:
            tts = gTTS(str(palavras[j]), lang=idiomas_palavras[j])
            tts.save(audios_caminho + "\\" +str(nome_deck) + "palavra" + str(j) + '.mp3')
        if idiomas_frase[j]==idioma_escolhido :
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
#Color of the cards
green='<span style="color: rgb(81, 255, 37);">'
#replace garbage
garbage=["»", "xa0","\\","]","[",".",'"',"'"]
for j in range(len(flista)):
    for i in garbage:
        flista[j]=flista.replace(i,"")

for i in range(0, len(flista)):
    if idiomas_palavras[j]==idioma_escolhido: #active
        nota = genanki.Note(
            model=my_model,
            fields=[flista[i],str(palavras[i]) + ".", ""],tags=[str(idiomas_frase[i]),"cardmaker"])
        deck.add_note(nota)
    else:
        if str(palavras[i]).count(" ")>=3: #Caso em que a palavra é na verdade uma frase
            nota = genanki.Note(
                model=my_model,
                fields=[flista[i],
                        "[" + "sound:" + str(nome_deck) + "palavra" + str(i) + ".mp3" + "]" + str(palavras[i]) + ".","" ],tags=[str(idiomas_frase[i]),"cardmaker"])
            deck.add_note(nota)
        else: #passive
            nota = genanki.Note(
                model=my_model,
                fields=["", "[" + "sound:" + str(nome_deck) + "palavra" + str(i) + ".mp3" + "]" + green + '<u><b><i>' + str(palavras[i])+ '</i></b></u></span>'  " == " + str(
                            traducao[i]), "[" + "sound:" + str(nome_deck) + "frase" + str(i) + ".mp3" + "]" + green + '<u><b><i>' + str(palavras[i])+ '</i></b></u></span>' + "." +
                    flista[i], ""],tags=[str(idiomas_frase[i]),"cardmaker"])
            deck.add_note(nota)
genanki.Package(deck).write_to_file(str(nome_deck) +'.apkg')


tf=time.time()

deltat=tf -t_o

if deltat>60:
    deltat=str(round(deltat//60)) + " Min " + str(round(deltat%60)) + " s"

else: deltat=round(deltat)
print(f"Congratulations, {len(palavras)} flashcards! In {deltat} sec,  {round(int(len(palavras))/(float(deltat)/60),1)} flashcards per minute")
time.sleep(120)