import os

from win32com import client as wc

def eachFilePath(root):
    url_list = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)

            if(str.endswith('.doc')):
                url_list.append(str)
    return url_list



def eachFilePath2(root):
    url_list = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)
            if(str.endswith('.docx')):
                url_list.append(str)
    return url_list

def doc2docx(list):
    for url in list:
        if(url.endswith('.doc')):
            word = wc.Dispatch('Word.Application')
            doc = word.Documents.Open(url)        # 目标路径下的文件
            doc.SaveAs(url+'x', 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件

            print(url+'x')
            doc.close()
            word.quit()

if __name__ == '__main__':
    url_list = eachFilePath("F:\\pjws")
    url_list2 = eachFilePath2("F:\\pjws")
    for url in url_list2:
        try:
            url_list.remove(url[:-1])
        except Exception:
            print('Error:'+url)
    print(len(url_list))
    doc2docx(url_list)