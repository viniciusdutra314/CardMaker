# *CardMaker is a library to create anki language learning cards programmatically*

## Creator
Hey my name is Vinícius Dutra and I'm currently studying computational physics at USP São Carlos, I'm the creator of the Brazilian youtube channel [Singularidade](https://www.youtube.com/Singularidade). I created a video explaining this library, it is the something thing that is written here but in video, the video is subtitled in multiple languages (Portuguese, English, Spanish and French) if you want to watch the video

## What it does?
You will need to save your phrases (in the foreign language that you are studying) in one excel table, the code will highlight the word that you want do not know and provide a possible translation for that word. Besides that, the code will create a temporary translation for the phrase in order to help you judge if the translation of the word was correct, if not, inside the code you can change the translation. After that, the code will create a deck .apkg file (Anki file) with audio in the front and at the back of the card. The code has 3 card modes (vocabulary, speaking, and writing) and many more features that will be explained in the following topics
## Language Support:

## Installation
#### In your Computer
The code was created using a variety of external python libraries, fortunately, all of them can be installed using the !pip install command, just be aware that some libraries (googletrans==3.1.0a0) have a specific version used. Here is the list of all the commands to install and the reason why the code uses these external libraries: 
```python
!pip install colorama #colors in the terminal
!pip install genanki #integration with anki
!pip install googletrans==3.1.0a0 #uses google translate
!pip install gtts #make audios
!pip install multiprocessing #count the number of cores
!pip install pandas #handle the excel tables
!pip install selenium #change the color of the highlighted word using a website
!pip install threading #multithreading processing
!pip install xlsxwriter #create excel tables
!pip install openpyxl 
```
#### Run in Google Colab
It is also possible to run the code on Google Colab using the **CardMaker (google colab)**, some additional steps to add the audio will be required, but the code can idea is the same, just click [here](https://colab.research.google.com/github/viniciusdutra314/CardMaker/blob/main/CardMaker%20(google%20colab).ipynb) 
## Type of Cards
### Formatting
All the excel tables used are in the folder [Tables examples](https://github.com/viniciusdutra314/CardMaker/tree/main/Tables%20examples). All the examples were created thinking in a person that was studying Spanish.
The first row of the excel is what determines the type of card, so please copy this first row exactly as it is shown in the images, otherwise, the code will not run but it doesn't have a card type selected. 
## Vocabulary
#### Excel Table
In the **Front** column you should put the phrases that you want to learn and in the **Back** the words that you do not know
<img src="images/vocabularytable.jpg" width="680" height="230">
#### Result
The front of the card is the phrase if the unknown word highlighted and the back is the translation of the word (front and back have audios, in this case the pronunciation in Spanish)

<img src="images/resultvocabulary.jpg" width="670" height="230">

## Speaking
#### Excel Table
In the first column **Speaking** you should put the phrase that you want to speak, there is no second column, only the first one.

<img src="images/speakingtable.jpg" width="670" height="230">
#### Result
The idea is to create active vocabulary, you have a phrase that you need to say in other language

<img src="images/resultspeaking.jpg" width="670" height="230">
## Writing
#### Excel Table
It is very similar to the cardtype **Speaking**, in terms of excel you just need to put the phrases in the **Writing** column.

<img src="images/writing.jpg" width="670" height="230">
#### Result
This mode is based on the "type in answer", you training your writing, any mistake will appear as red

<img src="images/writingresult.jpg" width="700" height="350">
