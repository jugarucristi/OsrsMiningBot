import pyautogui
import math
import random

def distance (firstX, firstY, secondX, secondY) :
    return math.sqrt((secondX - firstX)*(secondX - firstX) + (secondY - firstY)*(secondY - firstY))

def mouseTravel(xDestination ,yDestination):
    currentMousePos = pyautogui.position()

    xStart =currentMousePos[0]
    yStart = currentMousePos[1]

    if abs(xStart - xDestination) < 10 and abs(yStart - yDestination) < 10 :
        return

    initialLength = distance (xStart, yStart, xDestination, yDestination)
    currentLength = initialLength

    if xDestination > xStart:
        xLenght = xDestination - xStart
    else :
        xLenght = xStart - xDestination

    if xLenght == 0:
        xLenght = 1

    if yDestination > yStart :
        yLenght = yDestination - yStart
    else :
        yLenght = yStart - yDestination

    if yLenght == 0:
        yLenght = 1

    Xratio = xLenght / yLenght
    Yratio = yLenght / xLenght

    xSpeed = 15
    ySpeed = 15
    leeway = 20

    while distance(xStart,yStart,xDestination,yDestination) > leeway :

        if Xratio <= 100 :
            xOffset = xSpeed * Xratio
        if Yratio <= 100:
            yOffset = ySpeed * Yratio

        if abs(xStart- xDestination) < 5 :
            xOffset = 0
            yOffset = 10

        if  abs(yStart- yDestination) < 5 :
            yOffset = 0;
            xOffset = 10;

        if xOffset > 200:
            xOffset = 200
        if yOffset > 200:
            yOffset = 200

        if xStart < xDestination :
            xStart += xOffset
        else :
            xStart -=xOffset

        if yStart < yDestination :
            yStart += yOffset
        else :
            yStart -= yOffset

        currentLength = distance(xStart, yStart , xDestination, yDestination)

        lenghtPercenteage = 100 - (currentLength * 100 / initialLength)

        if lenghtPercenteage > 75 % 10 and xSpeed > 10 and ySpeed > 10 :

            xSpeed -= 3 - random.randint(0,2)
            ySpeed -= 3 - random.randint(0,2)

        if lenghtPercenteage < 20  and xSpeed < 100  and ySpeed < 100:

            xSpeed += 3 + random.randint(0,2)
            ySpeed += 3 + random.randint(0,2)

        if xDestination > xStart :
            xLenght = xDestination - xStart
        else :
            xLenght = xStart - xDestination

        if yDestination > yStart :
            yLenght = yDestination - yStart
        else :
            yLenght = yStart - yDestination

        Xratio = xLenght / (yLenght + 1)
        Yratio = yLenght / (xLenght + 1)

        if xStart > 3840 or yStart > 1080  or xStart < 0 or yStart < 0:
            break

        pyautogui.moveTo(xStart, yStart)
        print(xStart, yStart)






