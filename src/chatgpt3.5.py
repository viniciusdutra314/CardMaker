import requests
OPENAI_API_KEY='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'

def chatgpt(cardtype,translation_lang,original_lang,word,phrase,OPENAI_API_KEY):
    '''
    Generates responses using the OpenAI GPT-3.5 Turbo model based on specified inputs.

    Parameters:
    - cardtype (str): Type of flashcard ('v' for vocabulary, 's' for sentence, 'w' for word). 
    - translation_lang (str): target language for translation.
    - original_lang (str): Original language of the phrase or word.
    - word (str): Word to be explained (if applicable).
    - phrase (str): Phrase or sentence for translation or explanation.
    - OPENAI_API_KEY (str): OpenAI GPT-3 API key for authentication.

    Returns:
    str: The generated response based on the specified inputs.
    '''
    from requests import post
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    if cardtype=='v':
        question=f"Explain in {translation_lang} what '{word}' means in the phrase"
        question+=f"'{phrase}' and also in a broader context,"
        question+=f'But please maintain the word and the phrase in {original_lang}'
    elif cardtype in ['s','w']:
        question=f"Translate this phrase {phrase} to {translation_lang} and explain its meaning"
        question+=f"also in {translation_lang}"
    else:
        return None
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    response = post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']
