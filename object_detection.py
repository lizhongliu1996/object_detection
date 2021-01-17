import cv2, time
from datetime import datetime
import pandas as pd

first_frame = None
status_ls = [None, None]
times = []
df = pd.DataFrame(columns = ["start", "end"])
alpha = 0.1

video = cv2.VideoCapture(0)
#+ cv2.CAP_DSHOW
img = cv2.imread("dogg.jpeg")

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray,(31,31),0)

    if first_frame is None:
        first_frame = gray_blur
        continue

    delta_frame = cv2.absdiff(first_frame, gray_blur)
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, (3,3), iterations=2)

    (contours,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        cv2.putText(frame, "handsome guy", (x,y-10), cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255), 1)
        cv2.putText(frame,"press a/d to change transparency",(0,10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,(255,0, 0),1)

        resized_img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
        added_img = cv2.addWeighted(frame[y:y+h,x:x+w,:], alpha, resized_img[0:h,0:w,:],1-alpha,0)
        frame[y:y+h,x:x+w] = added_img

    status_ls.append(status)

    status_ls = status_ls[-2:]
    # if status_ls[-1] != status_ls[-2]:
        #times.append(datetime.now())
    if status_ls[-1] == 1 and status_ls[-2] == 0:
        times.append(datetime.now())
    if status_ls[-1] == 0 and status_ls[-2] == 1:
        times.append(datetime.now())

    #cv2.imshow("gaussian", gray_blur)
    #cv2.imshow("delta_frame", delta_frame)
    #cv2.imshow("added_img", added_img)
    cv2.imshow("capturing", frame)
    #cv2.imshow("thresh_frame", thresh_frame)
    key = cv2.waitKey(20)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
    # press d to increase alpha by 0.1
    if key == ord('d'):
        alpha +=0.1
        if alpha >=1.0:
            alpha = 1.0
     # press a to decrease alpha by 0.1
    elif key == ord('a'):
        alpha -= 0.1
        if alpha <=0.0:
            alpha = 0.0

for i in range(0, len(times), 2):
    df = df.append({"start":times[i], "end":times[i+1]},ignore_index=True)

df.to_csv("times.csv")

video.release()

cv2.destroyAllWindows()
