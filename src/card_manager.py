def colored_text(string,color):
    """
    Create HTML-formatted colored text.

    Parameters:
    - string (str): The text content to be colored.
    - color (tuple): A tuple representing the RGB values of the desired color.
    Each value in the tuple should be an integer between 0 and 255.

    Returns:
    str: HTML-formatted text with the specified color.

    Example:
    >>> colored_text("Hello, World!", (255, 0, 0))
    '<span style=\'color: rgb(255, 0, 0);\'>Hello, World!</span>'
    """
    html="<span style='color :rgb"
    html+=f"({color[0]}, {color[1]}, {color[2]});'>"
    html+=string+'</span>'
    return html

def create_note(cardtype,learning_lang,phrase,word,
                trans_phrase,trans_word,visual_configs):
    """Create Anki note content based on specified parameters.

    Parameters:
    - cardtype (str): Type of the card
    - learning_lang (str): Language the user is learning.
    - phrase (str): Original phrase or sentence.
    - word (str): Target word in the phrase or sentence.
    - trans_phrase (str): Translated version of the original phrase.
    - trans_word (str): Translated version of the target word.
    - visual_configs (dict): Visual configurations for formatting the note.
        - color (tuple): RGB values for text color.
        - bold (str): HTML bold tag.
        - font_size (str): HTML font size tag.
    Returns:
    tuple: Front content, back content, and tag for the Anki note.
    """
    color=visual_configs['color']
    bold=visual_configs['bold']
    font_size=visual_configs['font_size']
    if cardtype=='v':
        pieces=phrase.split(word)
        for piece in pieces[1:]:
            front=colored_text(word,color)+piece
        back=colored_text(word,color)+ '->' +trans_word
    elif cardtype in ['s','w']:
        front=phrase+ ' // '+learning_lang
        back=trans_phrase
    tag=f'CardMaker-{learning_lang}-{cardtype}'
    front=font_size + bold + front + bold + font_size
    back=font_size + bold + back + bold + font_size
    return front,back,tag

