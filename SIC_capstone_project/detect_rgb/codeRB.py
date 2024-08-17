# import the necessary packages
import imutils
import cv2
import numpy as np 
import math

video = cv2.VideoCapture(1)

def findHSV(video,frontCentroid,rightCentroid,backCentroid,leftCentroid,upCentroid,downCentroid):
    global xC1,xC2,xC3,xC4,xC5,xC6,xC7,xC8,xC9
    global yC1,yC2,yC3,yC4,yC5,yC6,yC7,yC8,yC9 
    global C1,C2,C3,C4,C5,C6,C7,C8,C9 
    xC1,xC2,xC3,xC4,xC5,xC6,xC7,xC8,xC9 = 0,0,0,0,0,0,0,0,0
    yC1,yC2,yC3,yC4,yC5,yC6,yC7,yC8,yC9 = 0,0,0,0,0,0,0,0,0
    C1,C2,C3,C4,C5,C6,C7,C8,C9 = 0,0,0,0,0,0,0,0,0

    # statusF, statusU,statusR,statusL,statusL,statusD = '','','','','','' 
    frontCurrentCentroid = ''
    # frontFace,rightFace,backFace,leftFace,upFace,downFace = '','','','','','' 

    count_err = 0
    stt = 0
    # print('STT')
    while True:
        # print('stt:',stt)
        frontOldCentroid = frontCurrentCentroid
        ret,img = video.read()
        cv2.imshow("Rubik's solver",img)
        k = cv2.waitKey(1)
        # if k == 27 or k == ord('q'):
        #     break
        image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        low_val = np.array([0,0,150])
        high_val = np.array([140,255,255])
        mask = cv2.inRange(image,low_val,high_val)
        # blur = cv2.GaussianBlur(mask,(3,3),0)
        blur = cv2.medianBlur(mask,3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        openn = cv2.morphologyEx(blur,cv2.MORPH_OPEN,kernel,iterations=4)
        morph = cv2.morphologyEx(openn,cv2.MORPH_CLOSE,kernel,iterations=1)
        thres = cv2.threshold(morph,200,250,cv2.THRESH_BINARY)[1]
        # cv2.imshow('thres',thres)
        # find contours in the thresholded image
        # cnts = cv2.findContours(morph.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cv2.findContours(thres.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        contours = []
        contoursCount =[]
        cPoints = []
        currentStr = ''
        xSum = 0
        ySum = 0
        xC = 0
        yC = 0
        for c in cnts:
            area = cv2.contourArea(c)
            # print('area point:',area)
            if 2000 <= area <= 9500:
                # compute the center of the contour
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center = (cX, cY)
                # print('center: ',center)

                # draw the contour and center of the shape on the image
                cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
                cv2.circle(img, center, 7, (0,0, 255), -1)
                # cv2.putText(img, "center", (cX - 5, cY - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
                # show the image
                # cv2.imshow("Image", image)
                contours.append(center)
                contoursCount.append(c)
        # print('contours count:',contoursCount)
        # print('so C:',len(contoursCount))
        if len(contours)>8:
            global dis_2p 
            dis_2p = int(round(math.sqrt((contours[0][0]-contours[1][0])**2+(contours[0][1]-contours[1][1])**2)))
            # print('dis 2p:',dis_2p)

            # print('contours:',contours)
            # print('so o vuong:',len(contours))
            # print('contours:',contours)
            if len(contours)==9:
                for i in range(len(contours)+1):
                    if i <9:
                        xSum = xSum + contours[i][0]
                        ySum = ySum + contours[i][1]
                    elif i==9:
                        xC = int(round(xSum/9))
                        yC = int(round(ySum/9))
            for i in range(len(contours)):
                if (abs(contours[i][0]-xC)+abs(contours[i][1]-yC))<10:
                    xC5 = contours[i][0]
                    yC5 = contours[i][1]
                    C5 = (xC5 ,yC5 ) 
                    # print('x,y=({0},{1})'.format(xC5,yC5))
            disSum = []
            p2468sum = []
            for i in range(len(contours)):
                dis = round(math.sqrt((contours[i][0]-xC5)**2+(contours[i][1]-yC5)**2))
                disSum.append(dis)
                mean_disSum = round(np.mean(disSum))
            for i in range(len(contours)):
                if round(math.sqrt((contours[i][0]-xC5)**2+(contours[i][1]-yC5)**2))>mean_disSum:
                    if contours[i][0]<xC5 and contours[i][1]<yC5:
                        xC1 = contours[i][0]
                        yC1 = contours[i][1]
                        C1 = (xC1 ,yC1 )
                    elif contours[i][0]<xC5 and contours[i][1]>yC5:
                        xC7 = contours[i][0]
                        yC7 = contours[i][1]
                        C7 = (xC7 ,yC7 )       
                    elif contours[i][0]>xC5 and contours[i][1]>yC5:
                        xC9 = contours[i][0]
                        yC9 = contours[i][1]
                        C9 = (xC9 ,yC9 )
                    elif contours[i][0]>xC5 and contours[i][1]<yC5:
                        xC3 = contours[i][0]
                        yC3 = contours[i][1]
                        C3 = (xC3 ,yC3 )
                elif round(math.sqrt((contours[i][0]-xC5)**2+(contours[i][1]-yC5)**2))<mean_disSum:
                    if contours[i][0] > xC5+dis_2p-5:
                        xC6 = contours[i][0]
                        yC6 = contours[i][1]
                        C6 = (xC6 ,yC6 )
                    elif contours[i][0] < xC5-dis_2p+5:
                        xC4 = contours[i][0]
                        yC4 = contours[i][1]
                        C4 = (xC4 ,yC4 )
                    elif contours[i][1] > yC5+dis_2p-5:
                        xC8 = contours[i][0]
                        yC8 = contours[i][1]
                        C8 = (xC8 ,yC8 )
                    elif contours[i][1] < yC5-dis_2p+5:
                        xC2 = contours[i][0]
                        yC2 = contours[i][1]
                        C2 = (xC2 ,yC2 )
            cPoints.extend((C1,C2,C3,C4,C5,C6,C7,C8,C9))
            # print('c Ponts:',cPoints)
            if len(cPoints)>=9:
                for c in cPoints:
                    try:                                    
                        if c[1]+20>480 or c[0]+20>640:
                            # print('pass')
                            pass
                        else:
                            # print('dang chay ROI ne')
                            ROIimg = image[(c[1]+10), (c[0]+10)]
                            # print('ROi img:',ROIimg)
                            # print('ROi img:',ROIimg[0])
                            h = ROIimg[0]
                            s = ROIimg[1]
                            v = ROIimg[2]
                            # print('h=',h)
                            # print('h,s,v={0},{1},{2}'.format(h,s,v))
                            if 0<=h<=8 and 90<s<255 and 90<v<255:
                                # print('red')
                                currentStr = currentStr + 'r'
                                cv2.putText(img, "R", (c[0], c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)  
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            elif 8<h<=20 and 120<s<255 and 90<v<255:
                                # print('orange')
                                currentStr = currentStr + 'o'
                                cv2.putText(img, "O", (c[0], c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) 
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            elif 30<=h<=50 and 120<s<255 and 90<v<255:
                                # print('yellow')
                                currentStr = currentStr + 'y'
                                cv2.putText(img, "Y", (c[0], c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) 
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            elif 45<=h<=75 and 120<s<255 and 90<v<255:
                                # print('green')
                                currentStr = currentStr + 'g'
                                cv2.putText(img, "G", (c[0], c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) 
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            elif 90<=h<=140 and 120<s<255 and 90<v<255:
                                # print('blue')
                                currentStr = currentStr + 'b'
                                cv2.putText(img, "B", (c[0], c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) 
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            elif 0<h<=140 and 0<s<50 and 160<v<255:
                                # print('white')
                                currentStr = currentStr + 'w'
                                cv2.putText(img, "W", (c[0]+5, c[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) 
                                # cv2.imshow("Rubik's solver",img)
                                # cv2.waitKey(1)   
                            else:
                                pass
                    except:
                        # print('passing')
                        pass
            # print('current str:',currentStr)
            cv2.putText(img, "1", (xC1 - 5, yC1+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "2", (xC2 - 5, yC2+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "3", (xC3 - 5, yC3+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "4", (xC4 - 5, yC4+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "5", (xC5 - 5, yC5+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "6", (xC6 - 5, yC6+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "7", (xC7 - 5, yC7+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "8", (xC8 - 5, yC8+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(img, "9", (xC9 - 5, yC9+5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.imshow('mor',morph)
            cv2.imshow("Rubik's solver",img)
            k = cv2.waitKey(1)
            if k == 27 or k == ord('q'):
                break
            frontCurrentCentroid = currentStr[4]
            # print('front current centroi:',frontCurrentCentroid)
            # print('old centroi: ',frontOldCentroid)
            if len(currentStr)==9:    
                if frontCurrentCentroid == frontOldCentroid:
                    # print('code mui ten dang chayj')
                    # print('front current {0}, front old ne {1}'.format(frontCurrentCentroid,frontOldCentroid))
                    if stt == 0:
                        # turn to right
                        cv2.arrowedLine(img,C1,C3,(255,255,255),4)
                        cv2.arrowedLine(img,C4,C6,(255,255,255),4)
                        cv2.arrowedLine(img,C7,C9,(255,255,255),4)
                        cv2.putText(img, "front Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        if frontCentroid == '':
                            frontFace = FaceOfRubik(currentStr,currentStr[4])
                            frontCentroid = currentStr[4]
                            print('F saved')
                            
                    elif stt == 1:
                        # turn to back
                        cv2.arrowedLine(img,C1,C3,(255,255,255),4)
                        cv2.arrowedLine(img,C4,C6,(255,255,255),4)
                        cv2.arrowedLine(img,C7,C9,(255,255,255),4)
                        cv2.putText(img, "right Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 2:
                        # turn to left
                        cv2.arrowedLine(img,C1,C3,(255,255,255),4)
                        cv2.arrowedLine(img,C4,C6,(255,255,255),4)
                        cv2.arrowedLine(img,C7,C9,(255,255,255),4)
                        cv2.putText(img, "back Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 3:
                        # turn to front
                        cv2.arrowedLine(img,C1,C3,(255,255,255),4)
                        cv2.arrowedLine(img,C4,C6,(255,255,255),4)
                        cv2.arrowedLine(img,C7,C9,(255,255,255),4)
                        cv2.putText(img, "left Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 4:
                        # turn to up
                        cv2.arrowedLine(img,C7,C1,(255,255,255),4)
                        cv2.arrowedLine(img,C8,C2,(255,255,255),4)
                        cv2.arrowedLine(img,C9,C3,(255,255,255),4)
                        cv2.putText(img, "front Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 5:
                        # turn to front
                        cv2.arrowedLine(img,C1,C7,(255,255,255),4)
                        cv2.arrowedLine(img,C2,C8,(255,255,255),4)
                        cv2.arrowedLine(img,C3,C9,(255,255,255),4)
                        cv2.putText(img, "up Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 6:
                        # turn down
                        cv2.arrowedLine(img,C1,C7,(255,255,255),4)
                        cv2.arrowedLine(img,C2,C8,(255,255,255),4)
                        cv2.arrowedLine(img,C3,C9,(255,255,255),4)
                        cv2.putText(img, "front Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                    elif stt == 7:
                        # turn to front
                        cv2.arrowedLine(img,C7,C1,(255,255,255),4)
                        cv2.arrowedLine(img,C8,C2,(255,255,255),4)
                        cv2.arrowedLine(img,C9,C3,(255,255,255),4)
                        cv2.putText(img, "down Face", (20,50),cv2.FONT_HERSHEY_COMPLEX, 3, (150,150,150), 3)
                        cv2.imshow("Rubik's solver",img)
                        k = cv2.waitKey(1)
                else:
                    if stt == 0:
                        rightFace = FaceOfRubik(currentStr,currentStr[4])
                        rightCentroid = currentStr[4]
                        print('R saved')
                        stt += 1
                    elif stt == 2:
                        backFace = FaceOfRubik(currentStr,currentStr[4])
                        backCentroid = currentStr[4]
                        print('B saved')
                        stt += 1
                    elif stt == 3:
                        leftFace = FaceOfRubik(currentStr,currentStr[4])
                        leftCentroid = currentStr[4]
                        print('L saved')
                        stt += 1
                    elif stt == 5:
                        upFace = FaceOfRubik(currentStr,currentStr[4])
                        upCentroid = currentStr[4]
                        print('U saved')
                        stt += 1
                    elif stt == 7:
                        downFace = FaceOfRubik(currentStr,currentStr[4])
                        downCentroid = currentStr[4]
                        print('D saved')
                        stt += 1
                    elif stt == 8:
                        print('select color success')
                cv2.imshow('mor',morph)
                cv2.imshow("Rubik's solver",img)
                k = cv2.waitKey(1)
        cv2.imshow('mor',morph)
        cv2.imshow("Rubik's solver",img)
        k = cv2.waitKey(1)
        if k == 27 or k == ord('q') or stt == 1:
            break
                
    return k,frontCentroid,rightCentroid,backCentroid,leftCentroid,upCentroid,downCentroid

while True:
    try:
        k,frontCentroid,rightCentroid,backCentroid,leftCentroid,upCentroid,downCentroid = findHSV(video,frontCentroid,rightCentroid,backCentroid,leftCentroid,upCentroid,downCentroid)
        # cv2.imshow('mor',morph)
        # cv2.imshow("Rubik's solver",img)
        # k = cv2.waitKey(1)
        if k == 27:
            break
    except:
        pass
cv2.destroyAllWindows()