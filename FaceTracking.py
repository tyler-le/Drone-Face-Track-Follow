import cv2
import pygame
from djitellopy import Tello
import time

# Small Area Around Face => Too Far => Move Forward // area < 6200px
# Big Area Around Face => Too Close => Move Backward // area > 6800px
# Area Around Face Within Acceptable Range => Stay // 6200px < area < 6800px
# Face Left of Center Point => Yaw Counter Clockwise
# Face Right of Center Point => Yaw Clockwise

tello = Tello()
tello.connect()
tello.streamon()
time.sleep(2.5)
width, height = 360, 240

# Pygame window for keyboard press
pygame.init()
window = pygame.display.set_mode((400, 400))


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 5)  # Detect Face

    myFacesCenter = []
    myFacesArea = []

    # Draw Rectangle Around Face
    for (x, y, width, height) in faces:
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)

        # Find Center Point & Draw
        centerX = x + (width // 2)
        centerY = y + (height // 2)
        cv2.circle(img, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

        # Find Area of Rectangle
        area = width * height

        # Parallel Arrays
        myFacesCenter.append([centerX, centerY])
        myFacesArea.append(area)

    if len(myFacesArea) != 0:
        # Gives us the index location of the max area in list
        i = myFacesArea.index(max(myFacesArea))
        return img, [myFacesCenter[i], myFacesArea[i]]

    else:
        # No center found, so return all 0's
        return img, [[0, 0], 0]


# >200 - ccw <200 - cw keep dot centerx in middle of screen ... keep centerX as close to 180 as possible. if > 180,
# go ccw until 180 and vice versa
def trackFace(info, width):
    minArea, maxArea = 6200, 6800
    centerX, centerY = info[0]
    area = info[1]
    low_x_threshold = width / 2 - 30  # 150
    high_x_threshold = width / 2 + 30  # 210
    forwardBackward = 0

    # Green Zone
    if minArea < area < maxArea:
        forwardBackward = 0

    # Too Close
    elif area > maxArea:
        forwardBackward = -20

    # Too Far
    elif area < minArea and area != 0:
        forwardBackward = 20

    # Face is within center threshold
    if low_x_threshold <= centerX <= high_x_threshold or centerX == 0:
        yaw = 0

    # Face is off center, turn CW
    elif 0 < centerX < low_x_threshold:
        yaw = -10

    # Face is off center, turn CCW
    elif centerX > high_x_threshold:
        yaw = 10

    tello.send_rc_control(0, forwardBackward, 0, yaw)


def process_key(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                tello.takeoff()
            if event.key == pygame.K_l or event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                tello.land()
            if event.key == pygame.K_a:
                tello.move_left(30)
            if event.key == pygame.K_d:
                tello.move_right(30)
            if event.key == pygame.K_w:
                tello.move_up(30)
            if event.key == pygame.K_s:
                tello.move_down(30)
            if event.key == pygame.K_LEFT:
                tello.rotate_counter_clockwise(30)
            if event.key == pygame.K_RIGHT:
                tello.rotate_clockwise(30)
            if event.key == pygame.K_1:
                tello.flip_left()
            if event.key == pygame.K_2:
                tello.flip_right()
            if event.key == pygame.K_3:
                tello.flip_back()
            if event.key == pygame.K_4:
                tello.flip_forward()


while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (width, height))

    # Info is an array where info[0] is an array containing x, y center point. info[1] is the area.
    img, info = findFace(img)
    trackFace(info, width)

    # Handle keyboard input to control drone, just in case we need to take control
    events = pygame.event.get()
    process_key(events)
    time.sleep(0.05)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break
