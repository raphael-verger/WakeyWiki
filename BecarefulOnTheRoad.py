import numpy as np
import cv2
import dlib
from math import hypot
import time
import tkinter as tk
import requests
from API import *
from recording import record
from playsound import playsound
blink_threshold = 6.5
sleep_threshold = 5
tired_threshold = 20

# define variables
blink_counter = 0
isTiredCount = 0
start = time.time()
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 0), (0, 0, 255)]
pause=False

def respond():
  record()
  filename = "output.wav"
  audio_url = upload(filename)
  ans = save_transcript(audio_url)
  print(ans)
  time.sleep(5)
  count = 0
  if 'yes' in ans.lower():
    print(2)
    playsound("C:\\Users\\brrzh\\Downloads\\McGill 6.mp3")
  else:
    playsound("C:\\Users\\brrzh\\Downloads\\McGill University - Biochemistry 21 (1).mp3")


# functions for all tiredness states of the driver
def is_falling_asleep():
  print("You are falling alseep! Wake up!")
  playsound("C:\\Users\\brrzh\\Downloads\\mixkit-bell-notification-933.mp3") #alarm
  playsound("C:\\Users\\brrzh\\Downloads\\McGill University - Biochemistry 17.mp3")
  respond()
  user_interface("You are falling alseep! Wake up!")
def is_sleepy():
  print("Did you fall asleep?")
  playsound("C:\\Users\\brrzh\\Downloads\\McGill University - Biochemistry 12.mp3")
  respond()
  user_interface("Did you fall asleep?")
def is_tired():
  print("You look tired, maybe get some rest")
  user_interface("You look tired, maybe get some rest")
def closeWindow(window):
  window.destroy()
  print("Close window")
def pauseDetection(window):
  window.destroy()
  pause=True
  print("Pause detection")

def user_interface(feedback):
  window = tk.Tk()
  window.geometry("750x500")
  window.title("123Don'tSleep")
  message = tk.Label(window, text=feedback, font=("Helvetica", 20))
  message.place(x=100,y=250)
  OK = tk.Button(window, text="I'm okay", command = window.destroy, fg="red", font="Verdana 14 underline", bd=2, bg="light blue", relief="groove")
  OK.place(x=600,y=400)
  pause = tk.Button(window, text="Pause detection for 1h", command = window.destroy, fg="red", font="Verdana 14 underline", bd=2, bg="light blue", relief="groove")
  pause.place(x=200,y=400)
  window.mainloop()

#def Label(self):
  #self.backgroundImage=tk.PhotoImage(file=)
  
  


# User interface widgets
#title = ttk.Label(parent, text='123')



  
# define cv2 objects
vid = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

# define dlib objects
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# function to calculate midpoint
def midpoint(p1 , p2):
  return (int((p1.x+p2.x)/2), int((p1.y + p2.y)/2))

# function to calculate the blinking rate
def get_blinking_ratio(eye_points, facial_landmarks):
  left_point = (facial_landmarks.part(eye_points[0]).x,facial_landmarks.part(eye_points[0]).y)
  right_point = (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y)
  center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
  center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
  hor_line = cv2.line(frame, left_point, right_point,(0,255,0),2)
  ver_line = cv2.line(frame, center_top, center_bottom,(0,255,0),2)
  ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))   
  hor_line_length = hypot((left_point[0]-right_point[0]),(left_point[1]- right_point[1]))
  if ver_line_length==0:
    ratio=0
  else:
    ratio = (hor_line_length / ver_line_length)
  return ratio


# Setup the user interface
#userInterface = np.zeros((471,636,3)) + 255
#userInterface = cv2.rectangle(userInterface, (0,0), (1000,1000), (200,200,200), -1) #background
#userInterface = cv2.rectangle(userInterface, (40,110), (600,330), (150,100,0), -1)
#userInterface = cv2.rectangle(userInterface, (40,10), (220,55), (0,0,0), 2)
#userInterface = cv2.rectangle(userInterface, (275,401), (370,445), colors[2], -1)
#userInterface = cv2.rectangle(userInterface, (390,401), (485,445), colors[2], -1)
#userInterface = cv2.rectangle(userInterface, (505,401), (600,445), colors[3], -1)

#cv2.putText(userInterface, "123 Don't Sleep!", (52, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
#cv2.putText(userInterface, "Pause", (295, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.putText(userInterface, "Play", (420, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.putText(userInterface, "Terminate", (515, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)



#cv2.namedWindow('UI', cv2.WINDOW_AUTOSIZE)

 
while(True):

      if pause:
        time.sleep(10)
        print("Dection program is back on!")
        pause = False

      ret, frame = vid.read()
      gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      faces = detector(gray)
      for face in faces:
        landmarks = predictor(gray, face)
        
        left_eye_ratio = get_blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio = get_blinking_ratio([42,43,44,45,46,47],landmarks)
        blinking_ratio = (left_eye_ratio+right_eye_ratio)/2

        if blinking_ratio > blink_threshold:
          time.sleep(0.13)
          cv2.putText(frame,"BLINKING", (50,150) , font, 7, (255,0,0))
          blink_counter += 1
          print(blink_counter)
          if(blink_counter == 10):
            end = time.time()
            if(end-start<sleep_threshold):
              is_falling_asleep()
            elif(end-start<tired_threshold):
              if(isTiredCount>=4):
                is_sleepy()
              else:
                is_tired()
                isTiredCount+=1
            blink_counter = 0
            start = end 


      cv2.imshow("Frame", frame)
      #cv2.imshow("UI", userInterface)

      if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()