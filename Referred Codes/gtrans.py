from googletrans import Translator as GT
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 120)  #120 words per minute
engine.setProperty('volume', 0.9) 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    return None

def trans(text, lang):
    gt = GT()
    translated = gt.translate(text, dest=lang, src='en')
    print ('Translate Text : ' + translated.origin)
    print ('Translated Text : ' + translated.text)
    speak('Translated Text : ' + translated.text)
    translated = gt.translate(translated.text, dest='en', src=lang)
    print ('Re-Translate Text : ' + translated.origin)
    print ('Re-Translated Text : ' + translated.text)
    speak('Re-Translated Text : ' + translated.text)
    return None

# End of File