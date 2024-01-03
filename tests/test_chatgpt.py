from src.chatgpt import chatgpt_API,available_chatgpt_models
OPENAI_API_KEY=False
if OPENAI_API_KEY:
    def test_chatgpt_models():
        models=available_chatgpt_models(OPENAI_API_KEY)
        assert len(models)>0 , 'Models are not available'
    def test_chatgpt_prompt_vocabulary():
        models=available_chatgpt_models(OPENAI_API_KEY)
        word='Throughout'
        phrase='There are crops throughout the land'
        for index,model in enumerate(models):
            result=chatgpt_API('v','fr','en',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}, number={index}, {result[1]}")
            assert result[0]==0
    def test_chatgpt_prompt_speaking():
        models=available_chatgpt_models(OPENAI_API_KEY)
        phrase="C'est past vrai!"
        word=''
        for index,model in enumerate(models):
            result=chatgpt_API('s','pt','fr',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}, number={index}, {result[1]}")
            assert result[0]==0
    def test_chatgpt_prompt_writing():
        models=available_chatgpt_models(OPENAI_API_KEY)
        phrase="Como crear bucles en Python?"
        word=''
        for index,model in enumerate(models):
            result=chatgpt_API('s','pt','es',OPENAI_API_KEY,
                               model,word,phrase)
            if result[0]==1: print(f"It get wrong in {model}, number={index},{result[1]}")
            assert result[0]==0