#Kelime Sayma-birleştirme

#bir dizinin altındaki Tek dosayyı okur.

# Import Module
import os
import shutil
import glob
import csv
import string
import pandas as pd
  
# Folder Path
path = "D:/YDS/deneme"
  
# Change the directory
os.chdir(path)

outfilename="merged.txt" #yukarıdaki os.chdir ile aktif klasör değiştirilmiştri. aktif olan klasöredeki text belgeleri okunup merged adında bileştirilmiştir.

file1=open ("YDS.csv","w",encoding="utf-8")
writer=csv.writer(file1)
writer.writerow(["Kelime","Tekrar"])


with open(outfilename, 'wb') as outfile: 
#encoding="utf-8"
    for filename in glob.glob('*.txt'):
        if filename == outfilename:
            # don't want to copy the ou;tput into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)
                   
#Python Kelime Sayma (Dosyadaki Kelimeleri Sayma)
file = open("merged.txt")




# with read we can read our txt file
# if it is necesarry use replace()
line = file.read()
file.close()



# use blank(" ") as a reference and split words 
splitWords = line.split()

#import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in splitWords and [i for i in splitWords if i.isalpha()]]# sadece alphaları saymak için
stripped.sort()

allWords={}
#for word in splitWords:
for word in stripped:
    if word not in allWords:
        allWords[word] = 1
    else:
        allWords[word] += 1

#*.keys() returns the all keys of list 
for key in allWords.keys():
     #print ("Word: %s =>%s " %(key , allWords[key]))
    #print ("%s =>%s " %(key , allWords[key]))
    Kelime=("%s >%s " %(key , allWords[key]))
    writer.writerow([Kelime])

ss=pd.read_csv("YDS.csv")
ss.to_excel("YDS_excel.xlsx")
#liste = ["d","c","ç","b","a"]
#print("Sort metotu belirtilen listeyi sıralar")
#liste.sort()
#print(liste)