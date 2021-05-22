import cv2 as cv
import face_recognition as fr
from face_recognition.api import face_distance
import numpy as np
import os 
import math
name=[]
encoded_image=[]
path='Images'
for i in os.listdir(path):
    x=os.path.splitext(path+'/'+i)[0]
    x=x.split('/')
    name.append(x[1])
    imgmain=fr.load_image_file(path+'/'+i)
    imgmain=cv.cvtColor(imgmain,cv.COLOR_BGR2RGB)
    face_location=fr.face_locations(imgmain)[0]
    encode_main_img=fr.face_encodings(imgmain)[0]
    encoded_image.append(encode_main_img)
# print(encode_main_img)
print(name)
try:
    cam=cv.VideoCapture(0)
except:
    print("No Webcam Available")
    exit()
while cam.isOpened():
    ret,img=cam.read()
    capture_image=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    try:
        curr_face_location=fr.face_locations(capture_image)[0]
        curr_face_encoded=fr.face_encodings(capture_image)[0]
        result=fr.compare_faces(encoded_image,curr_face_encoded)
        face_dist=fr.face_distance(encoded_image,curr_face_encoded)
        # print(result)
        if result==[True]:
            ind=np.argmin(face_dist)
            print(name[ind])
            # for top
            print(curr_face_location)
            top,right,bottom,left=curr_face_location
            cv.rectangle(img, (left-10, top-10), (right+10, bottom+10), (255, 0, 0), 2)
            cv.rectangle(img, (left-10, bottom+10), (right+10, bottom+40), (255, 0, 0), cv.FILLED)
            # # cv.putText(img,name[ind],(50,50),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            cv.putText(img, "Name:"+name[ind], (left-5, bottom +20), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv.putText(img, "Accuracy:"+str(math.ceil(face_dist[ind]*100*2))+'%', (left-5, bottom+35), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv.putText(img,"Door Unlocked!!!",(40,40),cv.FONT_ITALIC,1,(0,0,0),2)
        else:
            cv.putText(img,'Wrong Face Detected',(40,40),cv.FONT_ITALIC,1,(0,0,255),2)
            cv.putText(img,"Door Locked",(60,60),cv.FONT_ITALIC,1,(0,0,255),2)
    except:
        cv.putText(img,'No Face Detected',(40,40),cv.FONT_ITALIC,1,(0,0,255),2)
        cv.putText(img,"Door Locked",(60,60),cv.FONT_ITALIC,1,(0,0,255),2)

    cv.imshow('Frame',img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
cam.release()
cv.destroyAllWindows()



