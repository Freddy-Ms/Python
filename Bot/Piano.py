from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api
import win32con

#pyautogui.displayMousePosition()
#750,550
#830,550
#890,550
#980,550


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while keyboard.is_pressed('q') == False:
    if pyautogui.pixel(750,550)[0] == 0:
        click(750,550)
    if pyautogui.pixel(830,550)[0] == 0:
        click(830,550)
    if pyautogui.pixel(890,550)[0] == 0:
        click(890,550)
    if pyautogui.pixel(980,550)[0] == 0:
        click(980,550)
    
