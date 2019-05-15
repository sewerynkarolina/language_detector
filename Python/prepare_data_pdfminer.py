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





# Czytanie danych i zapis w paczkach (na wypadek, gdyby coś się popsuło po drodze)
import pandas as pd
h = len(files)/4

i=0
for j in range(4):
    files_t = files[int(j*h):int((j+1)*h)]

    text=[]
    print("Paczka " + str(j))
    if(i%50!=0):
        print(i)
    

    for file in files_t:
        try:
            t = convert_pdf_to_txt(file)
        except:
            t = ""
            print("Błąd: " + str(i) + " - " + file)
        
        text.append(t)
        
        if(i%50==0):
            print(i)
        i = i+1    
    
    if((i-1)%50!=0):
        print(i-1)
    
    t = pd.DataFrame({ "label": files_t, "text": text})
    t.to_csv(path + "text" + str(j) + ".csv")
    t.to_pickle(path + "text" + str(j) + ".pkl")
    





