import contextlib
import keyboard
import pytesseract
from PIL import ImageGrab
with contextlib.redirect_stdout(None):
    import pygame
import time
import cv2
import numpy as np

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# strings
play_strings = ["get ready: 1", "get ready: 2", "rescue", "100", "0:00"]
stop_strings = ["round", "join", "next", "drowned"]

# settings
music_file = "Hyperspace - V2 - luxTypes.mp3"
volume = 0.35


if __name__ == "__main__":
    running = False
    run_start = None
    session_start = time.time()
    attempts = 0
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    print(f"Initialized player with song '{music_file}' at volume {volume}")

    while True:
        screenshot = ImageGrab.grab(bbox=(0, 40, 1920, 1080))
        gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        text = text.lower()

        if any(partial in text for partial in play_strings) and not running:
            running = True
            if play_strings[1] in text:
                time.sleep(0.5)
            pygame.mixer.music.play()
            attempts+=1
            run_start = time.time()
            print(f"\nPlaying Hyperspace | Attempt {attempts} | All Text: " + text.strip().replace("\n", " "))
            continue
        elif (any(partial in text for partial in stop_strings) or keyboard.is_pressed('g')) and running:
            running = False
            pygame.mixer.music.stop()
            run_time = time.time() - run_start
            print(f"\nStopped music after {run_time} | All Text: " + text.strip().replace("\n", " "))
        time.sleep(0.25)