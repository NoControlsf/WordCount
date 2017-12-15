import cv2

# 读入图片文件
img_src = 'https://i0.hdslb.com/bfs/sycp/creative_img/201712/5a85c7c26a09b3b2b9881b9c1e75d547.jpg@440w_220h.webp'

cap = cv2.VideoCapture(img_src)
if cap.isOpened():
    ret, img = cap.read()
    cv2.imshow("image", img)
    cv2.waitKey()