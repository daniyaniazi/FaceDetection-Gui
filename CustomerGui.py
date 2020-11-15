from tkinter import *
import cv2,os
from tkinter import messagebox,Canvas
import Registration
import CreateStats
from PIL import Image, ImageTk
from keras.models import model_from_json
from keras.preprocessing import image
import numpy
from datetime import datetime
from datetime import timedelta 
#------------------ GUI Window -------------------------
root = Tk()
root.title=("Customer Detection")
root.geometry('1300x600+0+0')
root.config(bg='gray20')
# ------------VARIABLES--------------------------------
# load model
model = model_from_json(open("fer.json", "r").read())
# load weights
model.load_weights('fer.h5')
dataset='datasets'
(images,labels,names,id)=([],[],{},0)
# ----------------FUNCTIONS----------------------------
def removeSuccesMessage():
    suc_reg_lbl.config(text='',bg='gray10')
def register():
    cust_name=username_input.get()
    Registration.collectSamples(dataset=dataset,subdata=cust_name)
    res=Registration.registerCustomer(cust_name)
    if res=='Customer Register Succesfuly':
        suc_reg_lbl.config(text=cust_name+' Registered Succesfully',bg='sea green')
        root.after(5000,removeSuccesMessage)
        username_entry.delete(0, END)
    else:
        messagebox.showerror('Error',"Customer was already registered")
def recordEmo(pred_name, pred_emo,endTime,status):
    now=datetime.now()
    startTimestr = now.strftime('%H:%M:%S')
    if now<endTime:
        with open('CustEmo.csv', 'a') as emofile:
                print(f"\nwrite a file {pred_name},{startTimestr},{pred_emo},{status}")
                emofile.writelines(f"\n{pred_name},{startTimestr},{pred_emo},{status}")
    else:
        print("One Minutes Passed")
def customerdetection(*args):
        images,labels,names=Registration.loadDataset()
        face_recognizer_model=Registration.loadAlgorithm(images,labels)
        webcam=cv2.VideoCapture(0)
        cnt=0
        (width,height)=(130,100)
        recordCnt=0
        status=''
        while True:
            (ret,img)=webcam.read()
<<<<<<< Updated upstream
            if ret:
                Registration.put_text(img, 'Press Q to quit', 50, 220)
                gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                facesFound= Registration.face_cascade.detectMultiScale(gray_img,1.32,3)
                for (x,y,w,h) in facesFound:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    faceFound=gray_img[y:y+h,x:x+w]
                    face_resized=cv2.resize(faceFound,(int(width),int(height)))
                    label,confidence= face_recognizer_model.predict(face_resized)
                    Registration.draw_rect(img, (x,y,w,h))
                    predicted_name = names[label]
                    if confidence<70:
                        Registration.put_text(img, predicted_name+str(confidence), x, y)
                        Registration.CustomerWelcome(predicted_name)
                    else:
                        Registration.put_text(img,"Unregistred Customer", x, y)
                cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
                cv2.moveWindow("Detection", 650, 150)
                cv2.resizeWindow('Detection', 640,420)
                cv2.imshow('Detection',img)
                if cv2.waitKey(1) & 0xFF == ord("q") :
                    break

=======
            Registration.put_text(img, 'Press Q to quit', 50, 220)
            gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
            facesFound= Registration.face_cascade.detectMultiScale(gray_img,1.32,3)
            for (x,y,w,h) in facesFound:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) 
                faceFound=gray_img[y:y+h,x:x+w]
                face_resized=cv2.resize(faceFound,(int(width),int(height)))
                label,confidence= face_recognizer_model.predict(face_resized)
                Registration.draw_rect(img, (x,y,w,h))
                predicted_name = names[label]
                if confidence<70:
                    Registration.put_text(img, predicted_name+str(confidence), x, y)
                    # Emotion Detection
                    roi_gray = gray_img[y:y + w,x:x + h]  # cropping region of interest i.e. face area from  image
                    roi_gray = cv2.resize(roi_gray, (48, 48))
                    img_pixels = image.img_to_array(roi_gray)
                    img_pixels = numpy.expand_dims(img_pixels, axis=0)
                    img_pixels /= 255
                    predictions = model.predict(img_pixels)
                    # find max indexed array
                    max_index = numpy.argmax(predictions[0])
                    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
                    predicted_emotion = emotions[max_index]
                    if predicted_emotion=='angry' or predicted_emotion=='disgust' or predicted_emotion=='fear'or predicted_emotion=='sad':
                        status = "negative"
                    else:
                        status = "positive"
                    
                    # Set the time
                    if recordCnt==0:
                        recordCnt=1
                        now=datetime.now()
                        endTime=now+timedelta(seconds=60) 
#                         endTimestr = endTime.strftime('%H:%M:%S')
                    # Record emotions
                    recordEmo(predicted_name,  predicted_emotion,endTime,status)
                    cv2.putText(img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)
                    Registration.CustomerWelcome(predicted_name)
                else:
                    Registration.put_text(img,"Unregistred Customer", x, y)
            cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
            cv2.moveWindow("Detection", 650, 150)
            cv2.resizeWindow('Detection', 640,420)
            cv2.imshow('Detection',img)
            if cv2.waitKey(1) & 0xFF == ord("q") :
                break
>>>>>>> Stashed changes
        webcam.release()
        cv2.destroyAllWindows()
def getCustDetails():
    Cust_list.delete(0,END)
    with open('Customer_Details.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        visitTime=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            visitTime.append(entry[1])
            #print(visitTime)
        for i in range(len(nameList)): 
            Cust_list.insert(END, "\t\t - "+str(i) +" |  "+nameList[i]+ " \t\t | "+ str(visitTime[i])+"\n")
            Cust_list.insert(END,"-----------------------------------")
            Cust_list.insert(END,"\n")
def showStats():
    CreateStats.createStats()
    img = cv2.imread("AnalysisEmo2.png")
    cv2.putText(img, "Press Esc to quit", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 1)
    cv2.imshow("image",img) 
    key=cv2.waitKey(0)
    if key==27:
        cv2.destroyAllWindows()

# -------------------------------------------------------------------------------------------------------
MainHead=Label(root,text='Customer Detection System',font=('helvetica',20,'bold',),bg='gray15',fg='azure',pady=10)
MainHead.pack(fill=X)
Reglbl= Label(root,text="Register a customer",fg='white',bg='gray15',font=('times new roman',20,'bold'))
Reglbl.place( x=10,y=70,relwidth=0.48)

Detlbl= Label(root,text="Customer Detection",fg='white',bg='gray15',font=('times new roman',20,'bold'))
Detlbl.place( x=660,y=70,relwidth=0.2)

det_btn=Button(root,text="Detect Customer",font=('times new roman',10,'bold'),bg='pink',fg='black',activebackground='green',activeforeground='white',cursor='hand2',command=customerdetection,padx=5,pady=5)
det_btn.place(x=960,y=70,relwidth=0.1,)

stop_det_btn=Button(root,text="Show Customer Details",font=('times new roman',10,'bold'),bg='yellow',fg='black',activebackground='green',activeforeground='white',cursor='hand2',command=getCustDetails,padx=5,pady=5)
stop_det_btn.place(x=1100,y=70,relwidth=0.1,)

# --------------LEFT WINDOW----------------
Regframe = Frame(root,width=630,height=450,bg='gray10')
Regframe.place( x=10,y=120)
Reglbl= Label(Regframe,text="Enter Name :",fg='white',bg='gray10',font=('times new roman',16,'bold'))
Reglbl.place( x=10,y=15,relwidth=0.3)
# Enter user name
username_input=StringVar()
username_entry=Entry(Regframe,textvariable=username_input,font=('helvetica',15,'bold',),fg='azure',bg='gray27')
username_entry.place(x=200,y=15)
# Regoster Button
reg_btn=Button(Regframe,text="Register",font=('times new roman',10,'bold'),bg='yellow',fg='black',activebackground='green',activeforeground='white',cursor='hand2',command=register,padx=1,pady=1)
reg_btn.place(x=450,y=16,relwidth=0.2,)

suc_reg_lbl=Label(Regframe,text="",fg='white',bg='gray10',font=('times new roman',16,'bold'))
suc_reg_lbl.place( x=20,y=80,relwidth=0.95)

reg_btn=Button(Regframe,text="Show Stats",font=('times new roman',10,'bold'),bg='yellow',fg='black',activebackground='green',activeforeground='white',cursor='hand2',command=showStats,padx=1,pady=1)
reg_btn.place(x=450,y=120,relwidth=0.2,)
# ----------------- CUSTOMER DETAILS LISTBOX-------
cus_det_lbl=Label(Regframe,text="Customer Details",fg='white',bg='gray10',font=('times new roman',15,'bold'))
cus_det_lbl.place( x=20,y=120,relwidth=0.5)
Cust_list=Listbox(Regframe,fg='white',bg='gray15')
Cust_list .place(x=10,y=150,relwidth=0.95,height=290)

# --------------RIGHT WINDOW----------------
clientDframe = Frame(root,width=630,height=450,bg='gray10')
clientDframe.place( x=660,y=120,)
# Camera 
root.mainloop()