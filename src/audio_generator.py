def generate_audios(cardtype,langs,phrases,audio_path,deck_name,words=''):
  from gtts import gTTS  
  for j in range(len(phrases)):
        if cardtype=="v":
          audio_phrase = gTTS(f"{words[j]}.{phrases[j]}", lang=langs[j])
          audio_phrase.save(f"{audio_path}//{deck_name}phrase{j}.mp3")
          audio_word= gTTS(words[j], lang=langs[j])
          audio_word.save(f"{audio_path}//{deck_name}word{j}.mp3")
        elif cardtype in ["s","w"]:
          audio_phrase = gTTS(phrases[j], lang=langs[j])
          audio_phrase.save(f"{audio_path}//{deck_name}phrase{j}.mp3")
        elif cardtype=="p":
          audio = gTTS(phrases[j], lang=langs[j])
          audio.save(f"{audio_path}//{deck_name}pronunciation{j}.mp3")
