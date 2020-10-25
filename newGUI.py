# -----------------Importing dependecies
from tkinter import *
import cv2,os
from tkinter import messagebox,Canvas
import Registration
import  time
from PIL import Image, ImageTk
# --------------------------------------------
class App:
    def __init__(self, video_source=0):
        self.appName = 'Customer Detection'
        self.root = Tk()
        self.root.title(self.appName)
        self.root.resizable(0, 0)
        self.root.geometry('1300x600+0+0')
        self.root.config(bg='gray20')
        self.video_source = video_source
        self.webcam = cv2.VideoCapture(0)
        self.width=130
        self.height =100

        # self.vidobj = MyVideoCapture(self.video_source)
        # -----------------------FACE Attribute---------------
        self.dataset = 'datasets'
        self.images = []
        self.labels = []
        self.names = []
        self.id = 0

        # --------------------GUI---------------------
        self.MainHead = Label(self.root, text='Customer Detection System',
                              font=('helvetica', 20, 'bold',), bg='gray15', fg='azure', pady=10)
        self.MainHead.pack(fill=X)
        self.Reglbl = Label(self.root, text="Register a customer", fg='white', bg='gray15',
                       font=('times new roman', 20, 'bold'))
        self.Reglbl.place(x=10, y=70, relwidth=0.48)

        self.Detlbl = Label(self.root, text="Customer Detection", fg='white', bg='gray15',
                            font=('times new roman', 20, 'bold'))
        self.Detlbl.place(x=660, y=70, relwidth=0.2)

        self.det_btn = Button(self.root, text="Detect Customer",
                              font=('times new roman', 10, 'bold'), bg='pink', fg='black',
                              activebackground='green', activeforeground='white', cursor='hand2',
                              command=self.customerdetection, padx=5, pady=5)
        self.det_btn.place(x=960, y=70, relwidth=0.1, )

        self.stop_det_btn = Button(self.root, text="Show Customer Details",
                                   font=('times new roman', 10, 'bold'), bg='yellow', fg='black',
                                   activebackground='green', activeforeground='white',
                                   cursor='hand2', command=self.getCustDetails, padx=5, pady=5)
        self.stop_det_btn.place(x=1100, y=70, relwidth=0.1, )

        # --------------LEFT WINDOW----------------
        self.Regframe = Frame(self.root, width=630, height=450, bg='gray10')
        self.Regframe.place(x=10, y=120)
        self.Reglbl = Label(self.Regframe, text="Enter Name :", fg='white', bg='gray10',
                            font=('times new roman', 16, 'bold'))
        self.Reglbl.place(x=10, y=15, relwidth=0.3)
        # Enter user name
        self.username_input = StringVar()
        self.username_entry = Entry(self.Regframe, textvariable=self.username_input,
                                    font=('helvetica', 15, 'bold',), fg='azure', bg='gray27')
        self.username_entry.place(x=200, y=15)
        # Regoster Button
        self.reg_btn = Button(self.Regframe, text="Register", font=('times new roman', 10, 'bold'),
                              bg='yellow', fg='black', activebackground='green',
                              activeforeground='white', cursor='hand2', command=self.register,
                              padx=1, pady=1)
        self.reg_btn.place(x=450, y=16, relwidth=0.2, )

        self.suc_reg_lbl = Label(self.Regframe, text="", fg='white', bg='gray10',
                                 font=('times new roman', 16, 'bold'))
        self.suc_reg_lbl.place(x=20, y=80, relwidth=0.95)

        # ----------------- CUSTOMER DETAILS LISTBOX-------
        self.cus_det_lbl = Label(self.Regframe, text="Customer Details", fg='white', bg='gray10',
                                 font=('times new roman', 15, 'bold'))
        self.cus_det_lbl.place(x=20, y=120, relwidth=0.95)
        self.Cust_list = Listbox(self.Regframe, fg='white', bg='gray15')
        self.Cust_list.place(x=10, y=150, relwidth=0.95, height=290)

        # --------------RIGHT WINDOW----------------
        self.clientDframe = Frame(self.root, width=630,height=450, bg='gray10')
        self.clientDframe.place(x=660, y=120, )
        # Camera
        #CREATE CANVAS TO FIT THE VIDEO SOURCE

        self.canvas = Canvas(self.clientDframe, width=630,height=450,)
        self.canvas.pack()
        # # ----------------------------------------------------------
        # self.update()
        self.root.mainloop()
    # ----------------FUNCTIONS----------------------------
    # def update(self):
    #     check, frame = self.webcam.read()
    #     if check:
    #         self.photo=ImageTk.PhotoImage(image=Image.fromarray(frame))
    #         self.canvas.create_image(0,0,image=self.photo,anchor=NW)
    #     self.root.after(15,self.update)

    def removeSuccesMessage(self):
        self.suc_reg_lbl.config(text='', bg='gray10')

    def register(self):
        cust_name = self.username_input.get()
        path = os.path.join(self.dataset, cust_name)
        if not os.path.isdir(path):
            os.mkdir(path)
            face_cascade = cv2.CascadeClassifier(Registration.haar_file)
            count = 1
            while count < 31:
                if count==31:
                    self.webcam.release()
                    break

                else:
                    print(count)
                    self.reg(face_cascade,path,count)
                    count += 1
            res = Registration.registerCustomer(cust_name)
            if res == 'Customer Register Succesfuly':
                self.suc_reg_lbl.config(text=cust_name + ' Registered Succesfully', bg='sea green')
                self.root.after(5000, self.removeSuccesMessage)
                self.username_entry.delete(0, END)
        else:
            messagebox.showerror('Error', "Customer was already registered")
    def reg(self,face_cascade,path,count):
        check, frame = self.webcam.read()
        if check:
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facesFound = face_cascade.detectMultiScale(gray_img, 1.32, 3)
            for (x, y, w, h) in facesFound:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                faceFound = gray_img[y:y + h, x:x + w]
                face_resized = cv2.resize(faceFound, (self.width, self.height))
                cv2.imwrite('%s/%s.png' % (path, count), face_resized)
            # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.root.after(15, self.reg(face_cascade,path,count))



    def customerdetection(self,*args):
        self.images, self.labels, self.names = Registration.loadDataset()
        face_recognizer_model = Registration.loadAlgorithm(self.images, self.labels)
        while True:
            self.CDupdate(face_recognizer_model)
    def CDupdate(self,face_recognizer_model,):
        check, frame = self.webcam.read()
        if check:
            Registration.put_text(frame, 'Press Q to quit', 50, 220)
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facesFound = Registration.face_cascade.detectMultiScale(gray_img, 1.32, 3)
            for (x, y, w, h) in facesFound:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                faceFound = gray_img[y:y + h, x:x + w]
                face_resized = cv2.resize(faceFound, (int(self.width), int(self.height)))
                label, confidence = face_recognizer_model.predict(face_resized)
                Registration.draw_rect(frame, (x, y, w, h))
                predicted_name = self.names[label]
                if confidence < 70:
                    Registration.put_text(frame, predicted_name + str(confidence), x, y)
                else:
                    Registration.put_text(frame, "Unregistred Customer", x, y)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.root.after(15, self.CDupdate(face_recognizer_model))


    def getCustDetails(self):
        self.Cust_list.delete(0, END)
        with open('Customer_Details.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            visitTime = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                visitTime.append(entry[1])
                print(visitTime)
            for i in range(len(nameList)):
                self.Cust_list.insert(END,
                                 "\t\t - " + str(i) + " |  " + nameList[i] + " \t\t | " + str(
                                     visitTime[i]) + "\n")
                self.Cust_list.insert(END, "-----------------------------------")
                self.Cust_list.insert(END, "\n")

# ----------------------- MAIN -----------------------
if __name__ == '__main__':
    App()