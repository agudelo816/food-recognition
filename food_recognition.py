# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import imutils
import time
import siftnload as sift
from Result import Result
from Query import Query
import math

strCropped = "cropped.png"

dataset = ['banana1.png','banana2.png','banana3.png','banana4.png',
               'banana5.jpg', 'banana6.jpg', 'banana7.jpg', 'banana8.jpg',
               'banana9.jpg', 
               'bar1.png', 'bar2.png','bar3.png', 'bar4.png',
               'box1.png', 'box2.png', 'box3.png', 'box4.png',
               'box5.png', 'box6.png', 'box7.png', 'oj1.png',
               'oj2.png', 'oj3.png','oj4.png','oj5.png',
               'oj6.jpg', 'oj7.jpg', 'oj8.jpg', 'oj9.jpg', 
               'carrot1.png', 'carrot2.png', 'carrot3.png', 'carrot4.png',
               'carrot5.png', 'carrot6.png', 'carrot7.png', 'carrot8.jpg',
               'carrot9.jpg', 'carrot10.jpg', 'carrot11.jpg', 'carrot12.jpg',
               'carrot13.jpg', 'carrot14.jpg', 'energy1.jpg', 'energy2.jpg',
               'energy3.jpg', 'energy4.jpg','coffee1.jpg', 'coffee2.jpg',
               'coffee3.jpg', 'coffee4.jpg']
  
objects = []
listofstuff = []

def objectRecognition(mObj, methodType, query, dataset):
    if methodType == "Sift Matching":
        sift.siftMatching(mObj, query, dataset)
    return;

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)


start_time = time.time()

image = None
boolOcc = False
objCounter = 0
backgroundCounter = 0
boolBack = False

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if((time.time() - start_time) < 5):
        image = frame.array
        image = imutils.resize(image, width=500)
        if(not(boolBack)):
            boolBack = True
            strBC = str(backgroundCounter)
            backgroundCounter = backgroundCounter + 1
            cv2.imwrite(strBC+"background.png", image)


        # show the frame
         # cv2.imshow("Frame", image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        


    if((time.time() - start_time) > 5):
            
        c_frame = frame.array
    
        # loop over the frames of the video
        text = "Unoccupied"
    
        # if the frame could not be grabbed, then we have reached the end
        # of the video
    
        # resize the frame, convert it to grayscale, and blur it
        c_frame = imutils.resize(c_frame, width=500)
        c_gray = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
        c_gray = cv2.GaussianBlur(c_gray, (21, 21), 0)
    
        # cv2.imshow("gray", c_gray)
    
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(gray, c_gray)
        thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
    
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
    
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 300:
                continue
    
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(c_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
            if(text == "Occupied"):
                if(not(boolOcc)):
                    # print "Occupied"
                    picTimer = time.time()
                boolOcc = True

        if(boolOcc and ((time.time() - picTimer) > 5)):
            cv2.imwrite("framedelta.png", frameDelta)
            cv2.imwrite("threshold.png", thresh)
            cv2.imwrite("frame.png", c_frame)
            
            # print thresh.shape

            white_thresh = 255
            height, width = thresh.shape
            
    
            max_x = 0  # right
            max_y = height  # bottom
    
            
            min_y = 0  # top
            min_x = width  # left

                
            
            for i in range(0, height - 1):  # looping at python speed...
                for j in range(0, width - 1):  # ...
                    if thresh[i, j] > 250:
                        if (j > max_x):
                            max_x = j
                        if (i > min_y):
                            min_y = i
                        if (j < min_x):
                            min_x = j
                        if (i < min_y):
                            min_y
    
           #  print "max_x " + str(max_x)
           #  print "max_y " + str(max_y)
           #  print "min_x " + str(min_x)
           #  print "min_y " + str(min_y)

            strPre = str(objCounter)
            strDataset = strPre+strCropped
            
            crop_img = c_frame[0:375, min_x:max_x]
            cv2.imwrite(strDataset, crop_img)
            i = objCounter 
            objCounter = objCounter + 1

            boolRemoved = True
            if(len(objects) > 0):
                for mobjects in range(len(objects)):
                    curObjMax = objects[mobjects].get_max()
                    curObjMin = objects[mobjects].get_min()

                    if(((min_x-5) <= (curObjMin)) and (max_x+5 >= (curObjMax))):
                        # print "Removed"
                        listofstuff[mobjects] = "Removed"
                        boolRemoved = False
                        strMatch = ""
                        objCounter = objCounter - 1
            
            if(boolRemoved):
                objects.append(Query(strDataset))
                objectRecognition(objects[i], "Sift Matching", strDataset, dataset)
                strMatch = ""
                # print "Query image: "+strDataset
                #for k in range(len(objects[i].results)):
                    #print "    Test: "+objects[i].get_result(k).type
                    #print "         Ranking: "
                    #for j in range(len(objects[i].get_result(k).matches)):
                        #print "         "+str(j+1)+": "+objects[i].get_result(k).get_match(j)

                strMatch = objects[i].get_result(0).get_match(0)
                    #print strMatch
                objects[i].set_x(min_x, max_x)
                # print "max x"+str(objects[i].get_max())

            

            #print "Sift Matching"
            boolOcc = False
            start_time = time.time()
            dsCount = 0
            for data in dataset:

                if (strMatch == data):
                    break

                dsCount = dsCount + 1
            # print "dscount "+str(dsCount)
            strFinalMatch = ""
            if(dsCount >= 0 and dsCount <= 8):
                strFinalMatch = "banana"
            elif(dsCount >= 9 and dsCount <= 12):
                strFinalMatch = "nature valley bar"
            elif(dsCount >= 13 and dsCount <= 19):
                strFinalMatch = "box"
            elif((dsCount >= 20) and (dsCount <= 28)):
                strFinalMatch = "orange"
            elif((dsCount >= 29) and (dsCount <= 42)):
                strFinalMatch = "carrots"
            elif((dsCount >= 43) and (dsCount <= 46)):
                strFinalMatch = "energy"  
            elif((dsCount >= 47) and (dsCount <= 50)):
                strFinalMatch = "coffee"  
            #elif(dsCount == 20):
                #strFinalMatch = "white"
            # else:
                # strFinalMatch = ""


            # print "Final Match"+strFinalMatch

            listofstuff.append(strFinalMatch)

            for p in listofstuff:
                if(p != ""):
                    print p

            print "--------------"
                

            boolBack = False
                
            
                    
                
                
        # draw the text and timestamp on the frame
        cv2.putText(c_frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(c_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, c_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", c_frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
    
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
   
        # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
  


camera.release()
cv2.destroyAllWindows()
