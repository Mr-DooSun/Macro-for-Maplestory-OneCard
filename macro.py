import numpy as np
from PIL import ImageGrab
import cv2
from pytesseract import image_to_string
from time import sleep
import pynput

keyboard_button = pynput.keyboard.Controller()
keyboard_key=pynput.keyboard.Key

mouse_button=pynput.mouse.Button
mouse_controller=pynput.mouse.Controller()

def Click():
	mouse_controller.position=(570,570)
	mouse_controller.press(mouse_button.left)
	mouse_controller.release(mouse_button.left)

	sleep(0.5)

	keyboard_button.press(keyboard_key.enter)
	keyboard_button.release(keyboard_key.enter)

	sleep(2)

def Move():
	sleep(3)
	keyboard_button.press(keyboard_key.left)
	sleep(20)
	keyboard_button.release(keyboard_key.left)

def Number_fail(): #숫자 입력 실패
	sleep(1)
	mouse_controller.position=(910,485)
	mouse_controller.press(mouse_button.left)
	mouse_controller.release(mouse_button.left)

	sleep(2)

	mouse_controller.position=(570,570)
	mouse_controller.press(mouse_button.left)
	mouse_controller.release(mouse_button.left)

	sleep(1)

	keyboard_button.press(keyboard_key.enter)
	keyboard_button.release(keyboard_key.enter)

	sleep(2)


def Check_number():
	before_passoword="true"
	TrueOrFalse=False
	for_check=True
	# while True:
	pixel=0

	# printscreen_pil =  ImageGrab.grab(bbox=(475,520,750,530))
	printscreen_pil =  ImageGrab.grab(bbox=(440,390,530,420))
	printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 

	img=cv2.cvtColor(printscreen_numpy,cv2.COLOR_BGR2RGB)
	# img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	lower_color=(255, 255, 255)
	upper_color=(255,255, 255)

	img_mask = cv2.inRange(img, lower_color, upper_color)

	password = image_to_string(img)

	for num in range(0,len(password)) : #비밀번호 타이핑을 한다
		try :
			print(int(password[num]))
		except :
			return

	for num in range(0,len(password)) : #비밀번호 타이핑을 한다
		print(password[num])
		keyboard_button.press(password[num])
		keyboard_button.release(password[num])
		TrueOrFalse=True

	if before_passoword==password: #이전 비번과 이번 비번이 같을때(무한) 멈춘다
		TrueOrFalse=False
		Only_number() #숫자만 입력하시오 문구가 뜨는 함수로 넘어간다

	if TrueOrFalse : #타이핑된 비밀번호를 확인 시킨다
		mouse_controller.position=(910,485)
		mouse_controller.press(mouse_button.left)
		mouse_controller.release(mouse_button.left)
		before_passoword=password
		TrueOrFalse=False
		sleep(1)

def Check_Match(): #매칭 되고잇는지 확인
	pixel=0

	printscreen_pil =  ImageGrab.grab(bbox=(1260,390,1350,450))
	printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 

	img=cv2.cvtColor(printscreen_numpy,cv2.COLOR_BGR2RGB)

	lower_color=(102, 68, 0)
	upper_color=(180,180, 0)

	img_mask = cv2.inRange(img, lower_color, upper_color)

	for y in range(0,60) :
		if pixel > 1200 :
			return True
		for x in range(0,90) :
			if pixel > 1200:
				break
			if img_mask[y,x] == 255 :
				pixel+=1

def Play(): #원카드 플레이
	playOrstop=True
	while playOrstop:
		printscreen_pil =  ImageGrab.grab(bbox=(475,520,750,530))
		printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 

		img=cv2.cvtColor(printscreen_numpy,cv2.COLOR_BGR2RGB)

		lower_color=(255, 255, 255)
		upper_color=(255,255, 255)

		img_mask = cv2.inRange(img, lower_color, upper_color)

		for y in range(0,10) :
			for x in range(0,275) :
				if img_mask[y,x] == 255 :
					break

		print("x : "+str(475+x)+" y : "+str(520+y))

		if (475+x) > 748 :
			if (520+y) > 528 :
				mouse_controller.position=(475,420)
				mouse_controller.press(mouse_button.left)
				mouse_controller.release(mouse_button.left)
		else : 
			mouse_controller.position=(str(475+x),str(520+y))
			mouse_controller.press(mouse_button.left)
			mouse_controller.release(mouse_button.left)

		sleep(0.5)
		mouse_controller.position=(600,460)
		mouse_controller.press(mouse_button.left)
		mouse_controller.release(mouse_button.left)
		sleep(0.5)
		playOrstop=Check_end()

		# cv2.imshow("img",img_mask)

		sleep(1)

def Check_end():
	pixel = 0
	printscreen_pil =  ImageGrab.grab(bbox=(800,600,900,620))
	printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 

	img=cv2.cvtColor(printscreen_numpy,cv2.COLOR_BGR2RGB)
	        
	lower_color=(60, 30, 17)
	upper_color=(70,35, 20)

	img_mask = cv2.inRange(img, lower_color, upper_color)

	# cv2.imshow("img_mask",img_mask)
	# cv2.imshow("img",img)

	for y in range(0,20) :
		for x in range(0,100) :
			if img_mask[y,x] == 255 :
				pixel += 1

	if pixel < 35 :
		print(pixel)
		print("end game")
		return False
	else :
		return True
	print(pixel)

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()

if __name__=="__main__":
	while True:
		playOragain=False
		Move()
		Click()

		while not(playOragain) :
			Check_number()
			sleep(1)
			playOragain=Check_Match()

			if not(playOragain):
				Number_fail()
		sleep(10)

		keyboard_button.press(keyboard_key.enter)
		keyboard_button.release(keyboard_key.enter)

		sleep(20)

		Play()
		Check_end()

		cv2.destroyAllWindows()

		sleep(1)

		mouse_controller.position=(680,350)
		mouse_controller.press(mouse_button.left)
		mouse_controller.release(mouse_button.left)

		sleep(1)

		keyboard_button.press(keyboard_key.enter)
		keyboard_button.release(keyboard_key.enter)

		print("end")

		sleep(3)