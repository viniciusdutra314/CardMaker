# CardMaker is a library to create anki language learning cards programmatically

## What it does?:
You will need to save your phrases (in the foreign language that you are studying) in one excel table, the code will highlight the word that you want do not know and provide a possible translation for that word. Besides that, the code will create a temporary translation for the phrase in order to help you judge if the translation of the word was correct, if not, inside the code you can change the translation. After that, the code will create a deck .apkg file (Anki file) with audio in the front and at the back of the card. The code has 3 card modes (vocabulary, speaking, and writing) and many more features that will be explained in the following topics

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
