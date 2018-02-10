import shutil

import docx
import sqlite3 as sqlite

def readDocx(docName):
    fullText = []
    doc = docx.Document(docName)
    paras = doc.paragraphs
    for p in paras:
        fullText.append(p.text)
    return '\n'.join(fullText)


def read_errorurl():
    db = sqlite.connect('e:/stock/fdcstock.db')
    cur = db.cursor()
    Results = cur.execute('select distinct errorurl from pjwserror')
    Results_list = []
    for dateResult in Results:
        Results_list.append(dateResult[0])
    db.commit()
    db.close()
    return Results_list

def copyfile():
    list = read_errorurl()
    for tmp in list:
        oldurl = 'f:\\PJWSDOCX\\'+tmp
        newurl = 'f:\\pjwserror\\'+tmp
        try:
            shutil.copyfile(oldurl, newurl)
        except Exception:
            print(tmp)

if __name__ == '__main__':
    #print(readDocx('f:\\a.docx'))
    copyfile()