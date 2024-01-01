def generate_translation(cardtype,langs,chosen_lang,phrases,words):
    '''
    Generates translations for phrases and optionally for words 
    based on language settings.

    Parameters:
    - cardtype (str): The type of flashcard 
    - langs (List[str]): List of source languages for each phrase.
    - chosen_lang (str): The target language for translation.
    - phrases (List[str]): List of phrases to be translated.
    - words (List[str], optional): List of words to be translated. 

    Returns:
    Tuple[List[str], List[str]]: A tuple containing lists of translated 
    phrases and translated words.
  '''
    from googletrans import Translator
    translator=Translator()
    translated_phrases=[translator.translate(phrases[i],source=langs[i],
                      dest=chosen_lang).text for i in range(len(phrases))]
    if cardtype=="v": 
      translated_words=[translator.translate(words[i],source=langs[i],
                  dest=chosen_lang).text for i in range(len(phrases))]
    else: translated_words=['' for i in range(len(phrases))]
    return translated_phrases,translated_words