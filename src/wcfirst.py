import jieba.analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import docx


fullText = []
doc = docx.Document('./MineCraft服务器搭建.docx')
paras = doc.paragraphs
for p in paras:
    fullText.append(p.text)
lyric = '\n'.join(fullText)


result = jieba.analyse.textrank(lyric, topK=100, withWeight=True)
keywords = dict()
for i in result:
    keywords[i[0]] = i[1]
print(keywords)


image = Image.open('./1.jpg')
graph = np.array(image)
wc = WordCloud(font_path='./fonts/simhei.ttf', background_color='White', max_words=100, mask=graph)
wc.generate_from_frequencies(keywords)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis("off")
plt.show()
wc.to_file('result.png')