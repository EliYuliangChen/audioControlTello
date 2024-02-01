from vosk import Model, KaldiRecognizer
import pyaudio

from djitellopy import Tello

tello = Tello()
tello.connect()

model = Model(r"C:\\Users\\cheny\\Downloads\\vosk-model-small-en-us-0.15")
# model = Model(r"C:\\Users\\cheny\\Downloads\\vosk-model-small-cn-0.22")

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

def analyzeCNCommand(command):
    try:
        if "起飞" in command:
            tello.takeoff()
        elif "降落" in command:
            tello.land()
        elif "向前飞" in command:
            tello.move_forward(30)
        elif "向后飞" in command:
            tello.move_back(30)
        elif "向左飞" in command:
            tello.move_left(30)
        elif "向右飞" in command:
            tello.move_right(30)
        elif "向上飞" in command:
            tello.move_up(30)
        elif "向下飞" in command:
            tello.move_down(30)
        elif "向前翻" in command:
            tello.flip_forward()
        elif "向后翻" in command:
            tello.flip_back()
        elif "向左翻" in command:
            tello.flip_left()
        elif "向右翻" in command:
            tello.flip_right()
        else:
            print("对不起，我不明白你的意思")
    except Exception:
        print("出现了一些问题")
        pass

while True:
    print("Listening...")
    command = getCommand()
    print("Command: " + command)
    analyzeCommand(command)
    print(tello.get_battery())
