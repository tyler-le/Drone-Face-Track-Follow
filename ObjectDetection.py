import cv2
import numpy as np
from djitellopy import Tello
import time


def run_webcam():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    threshold = 0.65

    while True:
        success, img = cap.read()
        names_indices, confidences, bounding_boxes = net.detect(img, confThreshold=threshold)

        if len(names_indices) != 0:
            for names_index, confidence, bounding_box in zip(names_indices.flatten(), confidences.flatten(),
                                                             bounding_boxes):
                cv2.rectangle(img, bounding_box, color=(0, 255, 0), thickness=3)
                cv2.putText(img, names[names_index - 1].upper(), (bounding_box[0] + 10, bounding_box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, str(round(confidence * 100, 2)) + '%', (bounding_box[0] + 200, bounding_box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Result', img)
        cv2.waitKey(1)


def run_tello():
    tello = Tello()
    tello.connect()
    print(tello.get_battery())
    tello.streamon()
    # tello.takeoff()
    # tello.send_rc_control(0, 0, 25, 0)
    width, height = 1080, 720

    time.sleep(2.5)
    threshold = 0.55

    while True:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (width, height))

        names_indices, confidences, bounding_boxes = net.detect(img, confThreshold=threshold)

        if len(names_indices) != 0:
            for names_index, confidence, bounding_box in zip(names_indices.flatten(), confidences.flatten(),
                                                             bounding_boxes):
                cv2.rectangle(img, bounding_box, color=(0, 255, 0), thickness=3)
                cv2.putText(img, names[names_index - 1].upper(), (bounding_box[0] + 10, bounding_box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, str(round(confidence * 100, 2)) + '%', (bounding_box[0] + 200, bounding_box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Result', img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
            break


names = []
names_path = 'coco.names'

# Take each line in coco.names and put as a list in names.
with open(names_path, 'r') as f:
    names = f.read().rstrip('\n').split('\n')

# Import Files
config_path = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weights_path = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weights_path, config_path)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

run_tello()


