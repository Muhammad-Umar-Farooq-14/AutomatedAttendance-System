
#code For AI SECTION -B 
import tkinter as tk#IMPORTING TKINTER LIBRARY
from tkinter import Message ,Text#IMPORT MESSAGE &TEXT FROM THE TKINTER LIBRARY
import cv2,os#IMPORTING CV2 AND OS
import shutil
import csv#IMPORTING CSV FOR WORKING IN EXCEL 
import numpy as np #IMPORTING NUMPY
from PIL import Image, ImageTk#IMPORTING FROM PILLOW LIBRARY
import pandas as pd #IMPORTING PANDAS
import datetime#IMPORTING DATE AND TIME
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#CREATING A WINDOW
window.title("Face Recognition System")

dialog_title = 'QUIT'
dialog_text = 'Do You Really want to quit'
#its a message box
 
#A window with geometry of 1280x720
image2 =Image.open('iks.jpg')
image1 = ImageTk.PhotoImage(image2)
window.configure(background='black')


#a fyull screen window
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



#these are all labels that we display on screen this is UI
##############################################################################################################33
#a label of the system 
message = tk.Label(window, text="AUTOMATED ATTENDANCE SYSTEM" ,bg="RED"  ,fg="white"  ,width=60  ,height=3,font=('times', 32, 'italic bold underline')) 
#placement on screen
message.place(x=0, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)
#ui for id
#entry is for entering data
txt = tk.Entry(window,width=20  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=700, y=215)
#label for your name entry
lbl2 = tk.Label(window, text="Enter Your Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)
#the place to enter your name
txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)
#label for notifactions
lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=400, y=400)
#a message to put in the place
message = tk.Label(window, text="" ,bg="white"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=400, y=650)

#message to to show attendance details
message2 = tk.Label(window, text="" ,fg="red"   ,bg="white",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=650)
 #its a function to clear the entry
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)
#its the function to clear the second entry
def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    #to tell if the entry is a number or not 
def is_number(s):
    try:
        float(s)     #gives true if the entry is float
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata  #this library gives characteristics of all the unicode numbers
        unicodedata.numeric(s)#to tell if it is numeric or not
        return True#gives true if yes
    except (TypeError, ValueError):
        pass
 
    return False
 #the function to take images it uses cv2 functions to do so

def TakeImages():        
    Id=(txt.get())
    #its the getter for txt defined earlier
    name=(txt2.get())
    #getter for name
    #if id is number and name is alpha start capturing the video
    #haarcascade_frontalface_default.xml is a classifier for face detection
    #smaple number is for every photo counter
    #while loops work until 30 images are taken.
    #cv2 functions are used to convert images into gray color for better accuracy and color complextions
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured image in the  TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                # it displays the frame
                cv2.imshow('frame',img)
            #waiting for 100 ms
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if sample num is greater than 100
            elif sampleNum>30:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        #StudentDetails\StudentDetails.csv is a database to save details of students
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#cv2 function for face recognition
    #if u r using old version u might use cv2.LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    #our xml classifier
    detector =cv2.CascadeClassifier(harcascadePath)
    #detector variable
    faces,Id = getImagesAndLabels("TrainingImage")
    #the image we saved earlier in take images
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    message.configure(text= res) #the message variable we defined earlier stores repsonse in it

def getImagesAndLabels(path):
    #getter for the paths of all files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    
    #creates empty face list
    faces=[]
    #creates empty ID's list
    Ids=[]
    #loop through all images and details
    for imagePath in imagePaths:
        #conversion of an image in grayscale
        pilImage=Image.open(imagePath).convert('L')
        #converting img in pillow array
        imageNp=np.array(pilImage,'uint8')
        #getter for id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extractes face from images stored earlier
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids
#track images is the taking of new image and checking for its credentials
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#our recognizer for face
    recognizer.read("TrainingImageLabel\Trainner.yml")#our classifier
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    #capturing of video with the help of cv2
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    #format of column names
    attendance = pd.DataFrame(columns = col_names) 
    #loop for image recognition
    #reradingt from camera in im

    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                #if the person is unknown
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    #all windows closed
    #printing of attendance through message 2 in response
    res=attendance
    message2.configure(text= res)

  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="green"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="green"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"  ,bg="green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="EXIT", command=window.destroy  ,fg="red"  ,bg="green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Najam Sheraz & TEAM","", "TEAM", "AI-B")
copyWrite.configure(state="disabled",fg="red"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
 
window.mainloop()