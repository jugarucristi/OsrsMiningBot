import cv2 as cv
from windowCapture import window_capture
from vision import Vision
from time import time, sleep
import pyautogui
import mouseMovement
import random
wincap = window_capture('RuneLite', 775, 525)


cascade = cv.CascadeClassifier('cascade/cascade.xml')

vision_iron_ore = Vision(None)

loop_time = time()

pyautogui.moveTo(wincap.offset_x,wincap.offset_y)
mouseMovement.mouseTravel(wincap.offset_x+350,wincap.offset_y+300)

def emptyInventory():
    inventory_ore_location = [wincap.offset_x+580+random.randint(-1,1),wincap.offset_y+230+random.randint(-1,1)]
    mouseMovement.mouseTravel(inventory_ore_location[0],inventory_ore_location[1])
    sleep(random.randint(100,400)/1000)
    pyautogui.keyDown('shift')
    sleep(random.randint(100,400)/1000)
    pyautogui.leftClick()
    sleep(random.randint(100,400)/1000)
    pyautogui.keyUp('shift')


def spinCamera (currentMousePos):
    currentX = currentMousePos[0]
    currentY = currentMousePos[1]
    pyautogui.mouseDown(button='middle')
    sleep(random.randint(150,350)/1000)
    mouseMovement.mouseTravel(currentX + random.randint(80, 200), currentY + random.randint(10, 30))
    sleep(random.randint(150,350)/1000)
    pyautogui.mouseUp(button='middle')
    mouseMovement.mouseTravel(currentX+ random.randint(-20, 20), currentY +random.randint(-40,40))


while(True):

    oldMousePos = pyautogui.position()

    screenshot = wincap.get_screenshot()

    rectangles = cascade.detectMultiScale(screenshot)

    detection_image = vision_iron_ore.draw_rectangles(screenshot, rectangles)

    #cv.imshow('Matches', detection_image)

    print('FPS {}'.format(1 / (time() - loop_time)))

    loop_time = time()


    mined = False
    if len(rectangles) > 0:
        mined = True
        targets = vision_iron_ore.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        mouseMovement.mouseTravel(xDestination=target[0] + random.randint(0,5),yDestination= target[1]+ random.randint(0,5))
        pyautogui.click()
        if len(rectangles) == 0:
            spinCamera(oldMousePos)

    sleep(random.randint(4,6))

    if mined == True:
        emptyInventory()

    if oldMousePos == pyautogui.position() :
        spinCamera(oldMousePos)

    key = cv.waitKey(1)
    if key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    if key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

    currentMousePos = pyautogui.position()



