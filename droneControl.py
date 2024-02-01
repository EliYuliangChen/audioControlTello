import cv2
import mediapipe as mp
from djitellopy import Tello
import threading
from time import sleep
import time
import numpy as np
import logging
from vosk import Model, KaldiRecognizer
import pyaudio

range = [7000, 9000]

pidSpeed = [0.4, 0.4, 0]
pid = [0.1, 0.1, 0]
width = 800  # WIDTH OF THE IMAGE
height = 600 # HEIGHT OF THE IMAGE

def keyboardMode(tello):
    while True:
        command = input("Enter command: ")
        if command == "take off":
            tello.takeoff()
        elif command.startswith("forward"):
            distance = int(command.split()[1])
            tello.move_forward(distance)
        elif command.startswith("back"):
            distance = int(command.split()[1])
            tello.move_back(distance)
        elif command.startswith("left"):
            distance = int(command.split()[1])
            tello.move_left(distance)
        elif command.startswith("right"):
            distance = int(command.split()[1])
            tello.move_right(distance)
        elif command.startswith("up"):
            distance = int(command.split()[1])
            tello.move_up(distance)
        elif command.startswith("down"):
            distance = int(command.split()[1])
            tello.move_down(distance)
        elif command.startswith("cw"):
            angle = int(command.split()[1])
            tello.rotate_clockwise(angle)
        elif command.startswith("ccw"):
            angle = int(command.split()[1])
            tello.rotate_counter_clockwise(angle)
        elif command == "flip forward":
            tello.flip_forward()
        elif command == "flip back":
            tello.flip_back()
        elif command == "flip left":
            tello.flip_left()
        elif command == "flip right":
            tello.flip_right()
        elif command == "stop":
            tello.stop()
        elif command == "land":
            tello.land()
            break
        elif command == "quit":
            break
        else:
            print("Invalid command")
        print(tello.get_battery())


def trackMode(tello, pid, pidSpeed, img):
    pFbError = 0
    pUdError = 0
    pSpeedError = 0
    while True:
        gestureList = getGesture(img)
        if gestureList[0] == "ThumbUp":
            break
        if gestureList[0] == "Top":
            tello.move_left(30)
            continue
        if gestureList[0] == "Bottom":
            tello.move_right(30)
            continue
        maxArea = max(gestureList[2])
        x, y = gestureList[1][0]
        speedError = x - width // 2
        udError = y - height//2
        fbError = maxArea - (range[0] + range[1]) // 2
        fb, ud, speed = 0, 0, 0
        
        if speedError != 0:
            speed = pidSpeed[0] * speedError + pidSpeed[1] * (speedError - pSpeedError)
            speed = int(np.clip(speed, -30, 30))
        else:
            speed = 0

        if udError != 0:
            ud = pid[0] * udError + pid[1] * (udError - pUdError)
            ud = int(np.clip(ud, -30, 30))
        else:
            ud = 0
            
        if maxArea > range[0] and maxArea < range[1]:
            fb = 0
        elif maxArea > range[1]:
            fb = pid[0] * pid[0] * pidSpeed[0] * fbError + pid[1] * pid[1] * pidSpeed[1] * (fbError - pFbError)
            fb = int(np.clip(fb, -30, 30))
        elif maxArea < range[0] and maxArea != 0:
            fb = pid[0] * pid[0] * pidSpeed[0] * fbError + pid[1] * pid[1] * pidSpeed[1] * (fbError - pFbError)
            fb = int(np.clip(fb, -30, 30))
        else:
            fb = 0

        tello.send_rc_control(0, -fb, -ud, speed)
        pSpeedError = speedError
        pFbError = fbError
        pUdError = udError

    tello.land()
    # return pSpeedError, pFbError, pUdError

def gestureDirection(hand_landmarks):
    thumb_tip = hand_landmarks[4]
    thumb_mcp = hand_landmarks[2]
    wrist = hand_landmarks[0]
    index_tip = hand_landmarks[8]
    index_pip = hand_landmarks[6]
    middle_tip = hand_landmarks[12]
    middle_pip = hand_landmarks[10]

    if thumb_tip.y < thumb_mcp.y and thumb_mcp.y < middle_tip.y:
        if index_tip.x > index_pip.x and middle_tip.x > middle_pip.x:
            return "ThumbUp"
        elif index_tip.x < index_pip.x and middle_tip.x < middle_pip.x:
            return "ThumbUp"
    elif thumb_tip.y > thumb_mcp.y and thumb_mcp.y > middle_tip.y:
        if index_tip.x < index_pip.x and middle_tip.x < middle_pip.x:
            return "ThumbDown"
        elif index_tip.x > index_pip.x and middle_tip.x > middle_pip.x:
            return "ThumbDown"
    elif index_tip.y < index_pip.y and middle_tip.y > middle_pip.y:
        return "Top"
    elif index_tip.y > index_pip.y and middle_tip.y < middle_pip.y:
        return "Bottom"
    elif index_tip.x < index_pip.x and middle_tip.x > middle_pip.x:
        return "Left"
    elif index_tip.x > index_pip.x and middle_tip.x < middle_pip.x:
        return "Right"
    else:
        return "None"
    
def flipMode(tello, img):
    while True:
        gesture = getGesture(img)
        if gesture == "ThumbUp":
            break
        elif gesture == "Top":
            tello.flip_forward()
        elif gesture == "Bottom":
            tello.flip_back()
        elif gesture == "Left":
            tello.flip_left()
        elif gesture == "Right":
            tello.flip_right()

        time.sleep(5)
    tello.land()
    
def getGesture(img):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)
    mpDraw = mp.solutions.drawing_utils
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    imgHeight, imgWidth, imgChannels = img.shape
    minx, miny = width, height
    maxx, maxy = 0, 0
    gesture = ''
    handsListArea = []
    handsMidPoint = []
    if results.multi_hand_landmarks:
        
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            gesture = gestureDirection(handLms.landmark)
            for id, lm in enumerate(handLms.landmark):
                xPos = int(lm.x * imgWidth)
                yPos = int(lm.y * imgHeight)
                minx = min(minx, xPos)
                miny = min(miny, yPos)
                maxx = max(maxx, xPos)
                maxy = max(maxy, yPos)
                if id == 9:
                    handsMidPoint.append((xPos, yPos))
        cv2.rectangle(img, (minx, miny), (maxx, maxy), (0, 0, 255), 2)
        handsListArea.append((maxx - minx) * (maxy - miny))
    return [gesture, handsMidPoint, handsListArea]

def getCommand(mic, recognizer):
    listening = True
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    while listening:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response = result[14:-3]
                listening = False
                stream.close()
                return response
        except OSError:
            pass

def audioMode(tello, mic, recognizer, command):
    while True:
        print("Listening...")
        command = getCommand(mic, recognizer)
        print("Command: " + command)
        try:
            if "quit" in command:
                break
            if "take off" in command:
                tello.takeoff()
            elif "land" in command:
                tello.land()
            elif "move forwards" in command:
                tello.move_forward(30)
            elif "move back" in command:
                tello.move_back(30)
            elif "move left" in command:
                tello.move_left(30)
            elif "move right" in command:
                tello.move_right(30)
            elif "move up" in command:
                tello.move_up(30)
            elif "move down" in command:
                tello.move_down(30)
            elif "flip forwards" in command:
                tello.flip_forward()
            elif "flip back" in command:
                tello.flip_back()
            elif "flip left" in command:
                tello.flip_left()
            elif "flip right" in command:
                tello.flip_right()
            else:
                print("I don't understand")
        except Exception:
            print("Something went wrong")
            pass

def main():
    tello = Tello()
    tello.connect()
    tello.send_keepalive()
    tello.for_back_velocity = 0
    tello.left_right_velocity = 0
    tello.up_down_velocity = 0
    tello.yaw_velocity = 0
    tello.speed = 0
    print(tello.get_battery())

    tello.streamoff()
    tello.streamon()
    model = Model(r"C:\\Users\\cheny\\Downloads\\vosk-model-small-en-us-0.15")
    # model = Model(r"C:\\Users\\cheny\\Downloads\\vosk-model-small-cn-0.22")

    frame_read = tello.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    while True:
        print("Please Choose a Mode: (1) Keyboard Mode (2) Audio Mode (3) Gesture Mode (4) Flip Mode")
        print("Lisening...")
        command = getCommand(mic, recognizer)
        print("Command: " + command)
        if "quit" in command:
            tello.land()
            break
        if "keyboard mode" in command:
            keyboardMode(tello)
        elif "audio mode" in command:
            audioMode(tello, mic, recognizer, command)
        elif "gesture mode" in command:
            tello.takeoff()
            cv2.imshow("Image", img)
            trackMode(tello, pid, pidSpeed, img)
        elif "flip mode" in command:
            tello.takeoff()
            cv2.imshow("Image", img)
            flipMode(tello, img)
        

if __name__ == "__main__":
    main()