#! /usr/local/bin/python
# -*- coding:utf-8 -*-

import pygame,os

import time

os.system("./iflytekTTS 'I love you 我喜欢你!' test.wav");
pygame.init()

pygame.mixer.music.load("test.wav")

pygame.mixer.music.play()

time.sleep(10)
