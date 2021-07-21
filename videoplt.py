import cv2
import pytesseract
##################################################################################
frameWidth = 640
frameHeight = 480
nPlateCascade= cv2.CascadeClassifier("haarcascade_plate_number.xml")
minArea = 500
color = (255,0,255)
#################################################################################
i=input("Enter the location of then file with format:")
cap = cv2.VideoCapture(i)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
count = 0
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray,1.1,4)
 
    for (x,y,w,h) in numberPlates:
        area = w*h
        if area>minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
            txt= pytesseract.image_to_string(img[y:y+h,x:x+w])
            text=[]

            for i in txt:
                if i.isalnum():
                    text.append(i)

            cv2.putText(img, str(txt) ,(x,y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            
            imgRoi = img[y:y+h,x:x+w]
            # txt = pytesseract.image_to_string(img[y:y+h,x:x+w])
            cv2.imshow("txt",imgRoi)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("scan/noPlate_" + str(count) + ".jpg", imgRoi)
        cv2.rectangle(img , (0,200), (640,300) , (0,255,0) , cv2.FILLED )
        cv2.putText(img, "scan saved" , (150,255) , cv2.FONT_HERSHEY_DUPLEX , 
                    2,(0,0,255),2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1   
        
