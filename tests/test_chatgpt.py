from src.chatgpt import chatgpt_API,available_chatgpt_models
OPENAI_API_KEY="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"
if OPENAI_API_KEY:
    def test_chatgpt_models():
        models=available_chatgpt_models(OPENAI_API_KEY)
        assert len(models)>0 , 'Models are not available'
    def test_chatgpt_prompt_vocabulary():
        models=available_chatgpt_models(OPENAI_API_KEY)
        word='Throughout'
        phrase='There are crops throughout the land'
        for model in models:
            result=chatgpt_API('v','fr','en',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}")
            assert result[0]==0
    def test_chatgpt_prompt_speaking():
        models=available_chatgpt_models(OPENAI_API_KEY)
        phrase="C'est past vrai!"
        word=''
        for model in models:
            result=chatgpt_API('s','pt','fr',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}")
            assert result[0]==0
    def test_chatgpt_prompt_writing():
        models=available_chatgpt_models(OPENAI_API_KEY)
        phrase="Como crear bucles en Python?"
        word=''
        for model in models:
            result=chatgpt_API('s','pt','es',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}")
            assert result[0]==0