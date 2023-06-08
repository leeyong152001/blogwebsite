import os
from gtts import gTTS

def loadAudio(text,title):
    output = gTTS(text,lang="vi", slow=False)
    name ='./core/static/audio/'+ title+".mp3"
    output.save(name)

