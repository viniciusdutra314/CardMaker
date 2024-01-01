def chatgpt_API(cardtype,translation_lang,original_lang,
            OPENAI_API_KEY,model,word,phrase=''):
    '''
    Generates responses using the OpenAI ChatGPT based on specified inputs.

    Parameters:
    - cardtype (str): Type of flashcard 
    - translation_lang (str): target language for translation.
    - original_lang (str): Original language of the phrase and/or word.
    - word (str): Word to be explained (if applicable).
    - phrase (str): Phrase or sentence for translation or explanation.
    - OPENAI_API_KEY (str): OpenAI GPT-3 API key for authentication.
    - model (str): One of the many models available, for example, "gpt-3.5-turbo"

    Returns:
     str: The generated response based on the specified inputs.
    '''
    from requests import post
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    prompt=f"(i'll be using the 2 word lang convention)"
    if cardtype=='v':
        prompt+=f"Imagine that you're a {original_lang} professor and you need to"
        prompt+=f" explain for a student that only speaks {translation_lang}"
        prompt+=f" what the '{word}' means in the phrase"
        prompt+=f" '{phrase}' and also in a broader context"
        prompt+=f"(make your replay totally in {translation_lang},"
        prompt+=f"give 3 examples totally in {original_lang} and"
        prompt+=f"be direct in the answer"
    elif cardtype in ['s','w']:
        prompt=f"Translate this phrase {phrase} to {translation_lang} and explain its meaning"
        prompt+=f"also in {translation_lang}"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    response = post(url, headers=headers, json=data)
    if response.status_code==200:
        return 0,response.json()['choices'][0]['message']['content']
    else:
        erro_msg=response.json()['error']['message']
        return 1,erro_msg,prompt

def available_chatgpt_models(OPENAI_API_KEY):
    '''Retrieve a list of available ChatGPT text models from 
    the OpenAI API using your credentials.

    Parameters:
    - OPENAI_API_KEY (str): Your OpenAI API key for authentication.

    Returns:
    - List[str] : A list of available GPT text models
    
    Obs:
    - If you want more models available you can change the conditional
    '''
    from requests import get
    url="https://api.openai.com/v1/models"
    header={"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response=get(url,headers=header)
    if response.status_code==200:
        models=[]
        for x in response.json()['data']:
            if x['id'].startswith('gpt') and 'instruct' not in x['id']:
                models.append(x['id'])
        return models
    else: return []

