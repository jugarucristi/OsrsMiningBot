#include <windows.h>
#include <winuser.h>
#include <iostream>
#include <random>
#include <math.h>
using namespace std;




class cursor {
private:
	unsigned int sleepTime = 500;

public:
	static void HideConsole()
	{
		::ShowWindow(::GetConsoleWindow(), SW_HIDE);
	}

	static void ShowConsole()
	{
		::ShowWindow(::GetConsoleWindow(), SW_SHOW);
	}

	static bool IsConsoleVisible()
	{
		return ::IsWindowVisible(::GetConsoleWindow()) != FALSE;
	}

	unsigned int distance(unsigned int firstX, unsigned int firstY, unsigned int secondX, unsigned int secondY)
	{
		return sqrt((secondX - firstX)*(secondX - firstX) + (secondY - firstY)*(secondY - firstY));
	}

	void mouseSpeedDebugger()
	{
		POINT currentCursorPosition;
		GetCursorPos(&currentCursorPosition);
		int pointOfReferenceX = currentCursorPosition.x, pointOfReferenceY = currentCursorPosition.y;
		while (true)
		{
			SHORT keyPress = GetKeyState('B');
			if (keyPress)
			{
				break;
			}
			if (pointOfReferenceX != currentCursorPosition.x && pointOfReferenceY != currentCursorPosition.y)
				std::cout << currentCursorPosition.x - pointOfReferenceX << " " << currentCursorPosition.y - pointOfReferenceY << std::endl;  // Display mouse speed for research purposes
			pointOfReferenceX = currentCursorPosition.x, pointOfReferenceY = currentCursorPosition.y;
			GetCursorPos(&currentCursorPosition);
			Sleep(1);
		}
	}

	void mouseTravel(unsigned int xDestination, unsigned int yDestination)
	{
		POINT currentCursorPosition;
		GetCursorPos(&currentCursorPosition);

		unsigned int xStart = currentCursorPosition.x;
		unsigned int yStart = currentCursorPosition.y;
		unsigned int xLenght, yLenght;
		unsigned int initialLength = distance(xStart, yStart, xDestination, yDestination);
		unsigned int currentLength = initialLength;
		
		

		if (xDestination > xStart)
			xLenght = xDestination - xStart;
		else
			xLenght = xStart - xDestination;

		if (xLenght == 0)
			xLenght = 1;

		if (yDestination > yStart)
			yLenght = yDestination - yStart;
		else
			yLenght = yStart - yDestination;

		if (yLenght == 0)
			yLenght = 1;
		std::cout << xLenght << " " << yLenght << endl;
		float ratioX = (float) xLenght / yLenght;
		float ratioY = (float) yLenght / xLenght;

		int xSpeed = 5;
		int ySpeed = 5;
		unsigned int leeway = 7;
	

		while (distance(xStart, yStart, xDestination, yDestination) > leeway)
		{
			unsigned int xOffset = xSpeed * ratioX;
			unsigned int yOffset = ySpeed * ratioY;

			if (xStart+2 >= xDestination && xStart-2 <= xDestination) {
				xOffset = 0;
				yOffset = 20;
			}

			if (yStart + 2 >= yDestination && yStart - 2 <= yDestination) {
				yOffset = 0;
				xOffset = 20;
			}

			if (xStart < xDestination)				//Values for next mouse position
				xStart += xOffset;
			else
				xStart -= xOffset;

			if (yStart < yDestination)
				yStart += yOffset;
			else
				yStart -= yOffset;

			SHORT keyPress = GetKeyState('B');		//Pause the bot
			if (keyPress)
			{
				std::cin.ignore(1);
			}

			currentLength = distance(xStart, yStart, xDestination, yDestination);	//Speed

			unsigned int lengthPercenteage = 100 - (currentLength * 100 / initialLength);
	
			if (lengthPercenteage > 80-rand()%10 && xSpeed>5 && ySpeed>5)
			{
				xSpeed -= 1 +rand()%2;
				ySpeed -= 1 +rand()%2;
			}
			if (lengthPercenteage < 20+rand()%10 && xSpeed<25+rand()%15 && ySpeed<25+rand()%15 )
			{
				xSpeed += 1+rand()%2;
				ySpeed += 1+rand()%2;
			}

			if (xDestination > xStart)				//Ratio recalculation
				xLenght = xDestination - xStart;
			else
				xLenght = xStart - xDestination;

			if (yDestination > yStart)
				yLenght = yDestination - yStart;
			else
				yLenght = yStart - yDestination;
			ratioX = (float)xLenght / yLenght;
			ratioY = (float)yLenght / xLenght;

			SetCursorPos(xStart, yStart);
		Sleep(10);
		}
		Sleep(sleepTime);
	}

	void LeftClick()
	{
		INPUT    Input = { 0 };
		// left down 
		Input.type = INPUT_MOUSE;
		Input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
		::SendInput(1, &Input, sizeof(INPUT));

		// left up
		::ZeroMemory(&Input, sizeof(INPUT));
		Input.type = INPUT_MOUSE;
		Input.mi.dwFlags = MOUSEEVENTF_LEFTUP;
		::SendInput(1, &Input, sizeof(INPUT));
		Sleep(sleepTime);

	}

	void RightClick()
	{
		INPUT    Input = { 0 };
		// right down
		Input.type = INPUT_MOUSE;
		Input.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
		::SendInput(1, &Input, sizeof(INPUT));

		// left up
		::ZeroMemory(&Input, sizeof(INPUT));
		Input.type = INPUT_MOUSE;
		Input.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
		::SendInput(1, &Input, sizeof(INPUT));
		Sleep(sleepTime);
	}


}pointer;


int main() {

	cursor::HideConsole();
	cursor pointer; 
	//pointer.mouseSpeedDebugger();
	
	pointer.mouseTravel(400, 500);
	pointer.RightClick();
	pointer.mouseTravel(410, 585);
	pointer.LeftClick();
	pointer.mouseTravel(0, 0);

	/*pointer.mouseTravel(400, 500);
	pointer.mouseTravel(0, 0);
	pointer.mouseTravel(1000, 700);
	pointer.mouseTravel(400, 500);
	pointer.mouseTravel(500, 400);*/
}
