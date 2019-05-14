path = '/home/marcin/Dane/'

import glob
files = [f for f in glob.glob(path + "*/*/*.pdf", recursive=True)]

for f in files[0:3]:
    print(f)


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
# from six import BytesIO as StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text





import re
from string import punctuation

def normalize2(file):
    
    #\x0c to znak specjalny końca strony
    file = file.replace("\x0c", " startstrona ")
    file = " startstrona " + file
    
    file = re.sub("[0-9]", "", file)

    #zmiana na małe litery
    file = file.lower()
    #Zmieniamy np. ó na o
    file = re.sub(r'[^\x20-\x7e]', '', file)
    #usuwanie cyfry
    file = re.sub(r'\d+', '', file)
    #usuwanie znaków specjalne
    file = ''.join(c for c in file if c not in punctuation)
    #Usuwamy  białe spacje
    file = re.sub(' +', ' ', file)
    return(file)





text=[]
i=0
for file in files:
    try:
        t = convert_pdf_to_txt(file)
    except:
        t = ""
        print("Błąd: " + str(i) + " - " + file)
    
    text.append(t)
    
    if(i%10==0):
        print(i)
    i = i+1    

if((i-1)%10!=0):
    print(i)
    
    
text_clean = []
text_n = []

for i in range(len(text)):  
    t = text[i]
    if(len(t)>0):
        if(t.count("\n")/len(t)>0.3):
            t2 = t.replace("-\n", "").replace("\n\n", "\n").replace("\n", " ").replace("  ", "#").replace(" ", "").replace("#", " ")
    
        else:
            t2 = t.replace("-\n", "").replace("\n\n", "\n").replace("\n", " ")
    else:
        t2 = ""
    
    text_clean.append(t2)
    
    t3 = normalize2(t2)
    text_n.append(t3)









for i in range(len(text_n)):
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_n[i][0:1000])

for i in range(len(text_clean)):
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_clean[i][0:1000])


print(text_n[10].replace("startstrona", "\n\n")[0:10000])


#k = 13
#t = remove_footer(text_n[k], 4)
#print(t.replace("startstrona", "\n\n"))
#
#text[k][0:1000]
#text_clean[k][0:1000]
