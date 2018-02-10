rfile = open('D:\\qy\\bjnx.sql', 'r')
wfile = open("D:\\qy\\utf8.sql", "w", encoding='UTF-8')
for line in rfile:
    wfile.write(line)
rfile.close()
wfile.close()