import pygame,os

import time

os.system("./iflytekTTS 'I love you!' test.wav");
pygame.init()

pygame.mixer.music.load("test.wav")

pygame.mixer.music.play()

time.sleep(10)
