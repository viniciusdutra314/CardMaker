from CardMaker import *
from os import listdir
cardtype='v'
num_lines=[7,6]
path='tests//vocabulary_tables'
def test_get_start_table():
    global cardtype,num_lines,path
    for index,table in enumerate(sorted(listdir(path))):
        phrases,words,langs,deck_name=data_from_starting_table('v',path+'//'+table)
        assert len(phrases)==len(words)==len(langs)==num_lines[index], 'Incompatible number of elements'

def async_audio():
    global cardtype,path
    for i,table in enumerate(sorted(listdir(path))):
        phrases,words,langs,deck_name=data_from_starting_table('v',path+'//'+table)
        generate_audios(cardtype,langs,phrases,'tests//audio_tests',f'exemplo{i}',words)

def test_async_translate():
    global cardtype,num_lines,path
    chosen_lang='pt'
    for i,table in enumerate(sorted(listdir(path))):
        phrases,words,langs,deck_name=data_from_starting_table('v',path+'//'+table)
        trans_phrases,trans_words=generate_translation(cardtype,langs,chosen_lang,phrases,words)
        assert len(trans_phrases)==len(trans_words)==len(langs)==num_lines[i], 'Incompatible number of elements'