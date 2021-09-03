import cv2 
import time
import numpy as np

fourcc=cv2.VideoWriter_fourcc(*"XVID")
output_file=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

cap=cv2.VideoCapture(0)
time.sleep(2)
bg=0

for i in range(60):
    ret,bg=cap.read()

bg=np.flip(bg,axis=1)

while(cap.isOpened()):
    ret,image=cap.read()
    if not ret:
        break
    image=np.flip(image,axis=1)
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)

    mask1=mask1+mask2

    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask2=cv2.bitwise_not(mask1)

    #keeping only parts of an object wihch has red color frontimage
    result1=cv2.bitwise_and(image,image,mask=mask2)
    #keeping only parts of image of background which is behind red color
    result2=cv2.bitwise_and(bg,bg,mask=mask2)

    final_result=cv2.addWeighted(result1,1,result2,1,0)
    output_file.write(final_result)
    cv2.imshow("invisible cloak",final_result)
    cv2.waitKey(1)

cap.release()
output_file.release()
cv2.destroyAllWindows()
