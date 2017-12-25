import cv2
import numpy as np
import datetime

cap = cv2.VideoCapture(1)
first_frame = None

while(True):
    ret, frame = cap.read()
    if ret == False:
        print("Turn on your camera!")
        break
    text = "Waiting..."

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("g1", gray)
    #Deixa a imagem mais fácil de se trabalhar computacionalmente, "borrando-a"
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #cv2.imshow("g2", gray)

    # if the first frame is None, initialize it
    if first_frame is None:
        first_frame = gray
        print("OK")
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow("Frame delta", frame_delta)

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it. Return the lenght of pointsq
        if cv2.contourArea(c) < 500:
            print(cv2.contourArea(c))
            continue

        # compute the bounding box for the contour, draw it on the frame, and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        text = "Detected!"

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Status of camera: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    #cv2.imshow("Frame Delta", frame_delta)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
