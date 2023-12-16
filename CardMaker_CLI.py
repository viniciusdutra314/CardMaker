from CardMaker import *
print(f'Welcome to Anki-Cardmaker :earth_americas: !')
print( f'The program is on a command line but there is',
f'no need to fear :smiley:', sep=' ')
cl=get_user_input("Choose the language that your cards and "+
                        "the interface will be translated (ex:pt,fr,en): ",
                        lambda lang: is_lang_valid(lang),
                        f"Typo in your language or unfortunately your language "+
                        "[red]is not supported[/red] by the code :(",
                        lambda x:x.lower())

tables_in_the_directory=[j for j in listdir() if j.endswith('.xlsx') and not 
(j.startswith("~$") or j in ["temp_table.xlsx","verified_table.xlsx"])] 
num_tables=len(tables_in_the_directory)
if num_tables==0:
    print(translate("You haven't import any excel table",chosen_language=cl))
elif num_tables==1:
    table_name=tables_in_the_directory[0]
elif num_tables>1: 
    print(tables_in_the_directory)
table_name=get_user_input(translate("Name of the excel table: ",chosen_language=cl),
            lambda x: x+".xlsx" in tables_in_the_directory,
            translate("Invalid table name",chosen_language=cl),
            lambda x: x +".xlsx")

print(f"{translate('Using the table',chosen_language=cl)} [green]{table_name}[/green]")
print(f"[blue]p=pronunciation [/blue] [red]s=speaking [/red]")
print(f"[green] w=writing[/green] [yellow] v=vocabulary [/yellow]",sep='')
cardtype=get_user_input(translate("What is the type of your card? ",chosen_language=cl),
                lambda cardtype: cardtype in ["s","p","w","v"],
                translate("[red]ERROR[/red], cardtype invalid",chosen_language=cl),
                lambda x:x[0].lower())
phrases,words,langs,deck_name=data_from_starting_table(cardtype,table_name)
print(translate("Translating...(1/2)",chosen_language=cl))
translated_phrases,translated_words=translate_phrases_n_words(cardtype,langs,phrases,words)
check_translation(cardtype,phrases,translated_phrases,
                words,translated_words)
print(f"{translate('Your translations are ready in',chosen_language=cl)}[green] check_table.xlsx![/green]")
print(translate("Please assert that everthing is fine and then save as",chosen_language=cl))
input(f"[green] verified_table.xlsx [/green],{translate('press any key to continue',chosen_language=cl)}:")
while 'verified_table.xlsx' not in listdir():
    print(f"[red]{translate('Error, You forgot to save the verified_table.xlsx',chosen_language=cl)}[/red]")
    input(translate("press any key to continue",chosen_language=cl))
phrases,translated_phrases,words,translated_words=import_data_from_table('verified_table.xlsx')
print(translate("Audios...(2/2)",chosen_language=cl))
#create a temp directory inside the project's folder
with TemporaryDirectory(dir=getcwd(),prefix=".tempaudio") as audio_path:
    if cardtype!='v': words=''
    create_audios(cardtype,langs,phrases,audio_path,deck_name,words)
    print("[blue]Blue[/blue] [red]Red [/red] [yellow]Yellow[/yellow] [magenta] Purple [/magenta] [green] Green [/green]")
    colors_rgb = {'gr': '<span style="color: rgb(81, 255, 37);">', 're': '<span style="color: rgb(228, 14, 14);">',
                        'bl': '<span style="color: rgb(18, 166, 252);">',
                        'ye': '<span style="color: rgb(249, 255, 54);">',
                        'pu': '<span style="color: rgb(198, 38, 255);">',
                        'pi': '<span style="color: rgb(255, 14, 192);">', }
    color=get_user_input(translate("Select a color: ",chosen_language=cl),
                    lambda color: color[0:2].lower() in colors_rgb,
                    translate("[red]Color invalid! [/red]",chosen_language=cl),
                    lambda color:color[0:2].lower())
    deck=create_deck(cardtype,deck_name,color,phrases,words)
    media_files=[f"{audio_path}//{j}" for j in listdir(audio_path)]
    genanki.Package(deck,media_files=media_files).write_to_file(f"{deck_name}.apkg")
    deltat=time() -t0
    print(f"Congratulations, {len(phrases)} flashcards in {deltat/60:.1f}",
    f"minutes! {60*len(phrases)/deltat:1f} flashcards per minute")
