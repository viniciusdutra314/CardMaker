from src.card_manager import (create_card_content,
                              colored_text,change_font_style)

def test_colored():
    texto='hey'
    colors=[[255,0,0],[0,255,0],[0,0,255],[0,0,0],[255,255,255]]
    for index,color in enumerate(colors):
        if index==0:
            assert colored_text(texto,color)=="<span style='color :rgb(255, 0, 0);'>hey</span>"
        if index==1:
            assert colored_text(texto,color)=="<span style='color :rgb(0, 255, 0);'>hey</span>"
        if index==2:
            assert colored_text(texto,color)=="<span style='color :rgb(0, 0, 255);'>hey</span>"
        if index==3:
            assert colored_text(texto,color)=="<span style='color :rgb(0, 0, 0);'>hey</span>"
        if index==4:
            assert colored_text(texto,color)=="<span style='color :rgb(255, 255, 255);'>hey</span>"
def test_changefontstyle():
    texto='Example of text'
    assert change_font_style(texto,True,True,1)=="<h1><i><b>Example of text</b></i></h1>"
    assert change_font_style(texto,True,False,1)=="<h1><b>Example of text</b></h1>"
    assert change_font_style(texto,False,False,1)=="<h1>Example of text</h1>"
    assert change_font_style(texto,False,False,-1)=="Example of text"
    for size in range(1,7):
        assert change_font_style(texto,False,False,size)==f"<h{size}>Example of text</h{size}>"
def test_vocabularycards():
    phrase='Oggi è il 3 gennaio 2024'
    word='Oggi'
    trans_phrase="Today's January third"
    trans_word='Today'
    audios={'phrase':'[sound:phrase.mp3]','word':'[sound:word.mp3]'}
    visual_configs={'color':[255,0,0],'bold':True,
                    'italic':False,'font_size':4}
    front,back,tag=create_card_content('v','it',phrase,word,trans_phrase,
                      trans_word,visual_configs,audios)
    assert front=="<h4><b>[sound:phrase.mp3]<span style='color :rgb(255, 0, 0);'>Oggi</span> è il 3 gennaio 2024</b></h4>"
    assert back=="<h4><b>[sound:word.mp3]<span style='color :rgb(255, 0, 0);'>Oggi</span>->Today</b></h4>"
    assert tag=="CardMaker-it-v"
def test_speakingcards():
    phrase='Oggi è il 3 gennaio 2024'
    word=''
    trans_phrase="Today's January third"
    trans_word=''
    audios={'phrase':'[sound:phrase.mp3]','word':'[sound:word.mp3]'}
    visual_configs={'color':[255,0,0],'bold':True,
                    'italic':False,'font_size':4}
    for cardtype in ['s','w']:
        front,back,tag=create_card_content(cardtype,'it',phrase,word,trans_phrase,
                        trans_word,visual_configs,audios)
        assert front=="<h4><b>[sound:phrase.mp3]Oggi è il 3 gennaio 2024<span style='color :rgb(255, 0, 0);'> // it</span></b></h4>"
        assert back=="<h4><b>[sound:word.mp3]Today's January third</b></h4>"
        assert tag==f"CardMaker-it-{cardtype}"