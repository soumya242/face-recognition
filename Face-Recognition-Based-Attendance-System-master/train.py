# -*- coding: utf-8 -*-
"""
Created on oct 23 2019
Last updated on Feb 10 2020
@author: Aditya Kumar Tiwari
"""

import tkinter as tk
from tkinter import messagebox
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import mysql.connector
import re

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import mysql.connector



mydb = mysql.connector.connect(host= "localhost", user="root", passwd="password", database="attendence_teacher")
mycursor = mydb.cursor()
#import csvmail as cm

fileName = ""

window = tk.Tk()
window.title("face recognizer")


#dialog_title = 'QUIT'
#dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
#window.geometry('1280x720')
window.configure(background='salmon2')

#window.attributes('-fullscreen', True)

#window.grid_rowconfigure(0, weight=10)
#window.grid_columnconfigure(0, weight=10)

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.




message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="salmon2"  ,fg="linen"  ,width=50  ,height=2,font=('times', 30, 'italic bold underline'))

message.place(x=150, y=0)
message.pack()


def selection():
    selection = "You selected the option " + str( "Student" if radio.get()==1 else "Faculty")
    global role
    role = selection[-7:]
    label.config(text=selection , bg= "salmon2",fg="brown", font=('times', 15, ' bold '))
    option()

def option():
    if 'role' not in globals():
        mes = tk.Label(window, text="PLEASE SELECT ROLE OPTION FOR REGISTRATION", bg="salmon2", fg="brown",
                       width=60, height=1, font=('times', 15, 'bold'))
        mes.place(x=500, y=120)
    else:
        mes = tk.Label(window, text="", bg="salmon2", fg="brown",
                       width=60, height=1, font=('times', 15, 'bold '))

        mes.place(x=500, y=120)

option()
radio = tk.IntVar()
lb = tk.Label(text="Enter role for",  bg = "salmon2",fg="brown", font=('times', 15, ' bold '))
lb.place(x=300, y=90)
# lb.pack()
R1 = tk.Radiobutton(window, text="Student", variable=radio, value=1, command=selection, bg = "salmon2",fg="brown", activebackground = "Red",font=('times', 15, ' bold italic '))
R1.place(x=300, y=120)
# R1.pack(anchor=tk.W)

R2 = tk.Radiobutton(window, text="Faculty", variable=radio, value=2, command=selection, bg = "salmon2",fg="brown", activebackground = "Red", font=('times', 15, ' bold italic '))
R2.place(x=300, y=150)
# R2.pack(anchor=tk.W)

label = tk.Label(window)
label.pack()

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=230, y=200)

txt = tk.Entry(window,width=30  ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=490, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=230, y=260)

txt2 = tk.Entry(window,width=30 ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=490, y=275)

lbl4 = tk.Label(window, text="Enter Email", width=20, fg="red", bg="yellow", height=2, font=('times', 15, ' bold '))
lbl4.place(x=230, y=320)

txt4 = tk.Entry(window, width=30, bg="yellow", fg="red", font=('times', 15, ' bold '))
txt4.place(x=490, y=335)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline '))
lbl3.place(x=230, y=400)

message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=65  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message.place(x=490, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=22  ,fg="red"  ,bg="yellow"  ,height=4 ,font=('times', 15, ' bold  underline'))
lbl3.place(x=100, y=600)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=52  ,height=4  ,font=('times', 15, ' bold '))
message2.place(x=400, y=600)

def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear3():
    txt4.delete(0, 'end')
    res = ""
    message.configure(text= res)
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def is_Email(email):
    if (re.search(regex, email)):
        return True
    else:
        return False

def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    email=(txt4.get())

    if 'role' not in globals():
        messagebox.showerror("Error", "role can not be empty")
    else:
        if(is_number(Id) and name.isalpha() and is_Email(email)):
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
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 60
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id + " Name : " + name + " Role : "+ role + " email : " + email
            row = [Id , name, role, email]
            with open('StudentDetails/StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            if(role=="Faculty"):
                sql = "INSERT INTO teacher_tb (id, teacher_name, email) VALUES (%s, %s, %s)"
                val = (Id, name, email)
                mycursor.execute(sql, val)
                mydb.commit()
                result = mycursor.rowcount
            message.configure(text= res)
        else:

            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)

            if (not is_Email(email)):
                res = "Enter valid Email"
                message.configure(text= res)


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    #detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
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
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    global fileName
    fileName="Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()

    res=attendance
    message2.configure(text= res)


def sendmail():
    my_filtered_csv = pd.read_csv(fileName, usecols=['Id'])
    listId = my_filtered_csv['Id'].values.tolist()
    EMAIL_ID = "adi1998.tiwari@gmail.com"
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    for id in listId:
        mycursor.execute(f"select email from teacher_tb where id = '{id}'")
        result = mycursor.fetchall()
        for i in result:
            email = i[0]
            emailfrom = EMAIL_ID
            emailto = email
            fileToSend = fileName
            username = EMAIL_ID
            password = EMAIL_PASS

            msg = MIMEMultipart()
            msg["From"] = emailfrom
            msg["To"] = emailto
            msg["Subject"] = "Attendance detail of class"
            msg.preamble = "Attendance detail of class"

            ctype, encoding = mimetypes.guess_type(fileToSend)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(fileToSend)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(fileToSend, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(fileToSend, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
            msg.attach(attachment)

            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username, password)
            server.sendmail(emailfrom, emailto, msg.as_string())
    res="mail sent"
    message.configure(text=res)
    server.quit()

  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=860, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=860, y=260)
clearButton3 = tk.Button(window, text="Clear", command=clear3  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton3.place(x=860, y=320)
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=100, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=400, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=700, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1000, y=600)
mail = tk.Button(window, text="Mail info", command=sendmail ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
mail.place(x=1000, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Aditya","", "TEAM", "superscript")
copyWrite.configure(state="disabled",fg="red"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
 
window.mainloop()