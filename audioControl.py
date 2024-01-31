from vosk import Model, KaldiRecognizer
import pyaudio

from djitellopy import Tello

tello = Tello()
tello.connect()

# model = Model(r"YOURFILELOCATION")
model = Model(r"YOURFILELOCATION")

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

listening = False

def getCommand():
    listening = True
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    while listening:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                print("***********result: " + result)
                response = result[14:-3]
                listening = False
                stream.close()
                return response
        except OSError:
            pass

def analyzeCommand(command):
    try:
        if command == "take off":
            tello.takeoff()
        elif command == "land":
            tello.land()
        elif command == "forward":
            tello.move_forward(30)
        elif command == "back":
            tello.move_back(30)
        elif command == "left":
            tello.move_left(30)
        elif command == "right":
            tello.move_right(30)
        elif command == "up":
            tello.move_up(30)
        elif command == "down":
            tello.move_down(30)
        elif command == "flip":
            tello.flip_forward()
        else:
            print("I don't understand")
    except Exception:
        print("Something went wrong")
        pass

def analyzeCNCommand(command):
    try:
        if command == "起飞":
            tello.takeoff()
        elif command == "降落":
            tello.land()
        elif command == "前进":
            tello.move_forward(30)
        elif command == "后退":
            tello.move_back(30)
        elif command == "左":
            tello.move_left(30)
        elif command == "右":
            tello.move_right(30)
        elif command == "上":
            tello.move_up(30)
        elif command == "下":
            tello.move_down(30)
        elif command == "翻":
            tello.flip_forward()
        else:
            print("I don't understand")
    except Exception:
        print("Something went wrong")
        pass

while True:
    print("Listening...")
    command = getCommand()
    print("Command: " + command)
    # English
    # analyzeCommand(command)
    # Chinese
    analyzeCNCommand(command)
    print(tello.get_battery())
