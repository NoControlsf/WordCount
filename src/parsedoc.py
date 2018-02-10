import os
import docx
import re
import sqlite3 as sqlite

def eachFilePath(root):
    url_list = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)

            if(str.endswith('.docx')):
                #print(str)
                url_list.append(str)
    return url_list

def readDocx(docName):
    result = []
    fullText = []
    try:
        doc = docx.Document(docName)
        paras = doc.paragraphs
        doc_name = docName.split('\\')[-1]
        #print(doc_name)
        result.append(doc_name)
        #print(paras[0].text)
        result.append(paras[0].text)
        #print(paras[1].text)
        result.append(paras[1].text)
        #print(paras[2].text)
        result.append(paras[2].text)
        """
        for p in paras[3:10]:
            if('原告' in p.text):
                #print(p.text)
                result.append(p.text)
                break
        for p in paras[3:10]:
            if('被告' in p.text):
                #print(p.text)
                result.append(p.text)
                break

        for p in paras[len(paras)-8:len(paras)]:
            if(re.search('.+?年.+?月.+?日', p.text)):
                #print(p.text)
                result.append(p.text)
        """
        for p in paras[3:]:
            fullText.append(p.text)
        art = '\n'.join(fullText)
        #print(art)
        result.append(art)
        return result
    except Exception:
        return 'error'


if __name__ == '__main__':
    url_list = eachFilePath("F:\\pjwserror")
    print(url_list)
    for url in url_list:
        result = readDocx(url)
        if(result == 'error'):
            conn = sqlite.connect("E:/stock/fdcstock.db")
            cur = conn.cursor()
            cur.execute('replace into pjwserror values({})'.format('\"'+url.split('\\')[-1]+'\"'))
            conn.commit()
            conn.close()
        else:
            print(result)
            sql = 'replace into pjwserrorart values({})'.format(('?,' * len(result))[:-1])
            conn = sqlite.connect("E:/stock/fdcstock.db")
            cur = conn.cursor()
            try:
                cur.execute(sql, result)
            except Exception:
                cur.execute('replace into pjwserror values({})'.format('\"'+url.split('\\')[-1]+'\"'))
            conn.commit()
            conn.close()