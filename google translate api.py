#google translate api

import pandas as pd 
import googletrans

f = open('D:\\Dosya\\yolu\\girdi.txt', 'r')
if f.mode == 'r':
    contents = f.read()
    print(contents) 

from googletrans import Translator

file_translate = Translator()

result = file_translate.translate(contents,dest='tr')
print(result.text)


with open('D:\\Dosya\\yolu\\ceviri.txt', 'w') as f:
    f.write(result.text)