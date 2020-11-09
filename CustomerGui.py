from tkinter import *
import cv2,os
from tkinter import messagebox,Canvas
import Registration
from PIL import Image, ImageTk

root = Tk()
root.title=("Customer Detection")
root.geometry('1300x600+0+0')
root.config(bg='gray20')
# ------------VARIABLEs--------------------------------
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

def customerdetection(*args):
        images,labels,names=Registration.loadDataset()
        face_recognizer_model=Registration.loadAlgorithm(images,labels)
        webcam=cv2.VideoCapture(0)
        cnt=0
        (width,height)=(130,100)
        
        while True:
            (ret,img)=webcam.read()
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

        webcam.release()
        cv2.destroyAllWindows()
        Registration.CustomerWelcome(predicted_name)

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
            print(visitTime)
        for i in range(len(nameList)): 
            Cust_list.insert(END, "\t\t - "+str(i) +" |  "+nameList[i]+ " \t\t | "+ str(visitTime[i])+"\n")
            Cust_list.insert(END,"-----------------------------------")
            Cust_list.insert(END,"\n")

# -----------------------------------------------
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

# ----------------- CUSTOMER DETAILS LISTBOX-------
cus_det_lbl=Label(Regframe,text="Customer Details",fg='white',bg='gray10',font=('times new roman',15,'bold'))
cus_det_lbl.place( x=20,y=120,relwidth=0.95)
Cust_list=Listbox(Regframe,fg='white',bg='gray15')
Cust_list .place(x=10,y=150,relwidth=0.95,height=290)

# --------------RIGHT WINDOW----------------
clientDframe = Frame(root,width=630,height=450,bg='gray10')
clientDframe.place( x=660,y=120,)
# Camera 
root.mainloop()