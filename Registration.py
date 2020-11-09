import cv2,os
from datetime import datetime
import numpy
haar_file='C:\\Users\\DANIA NIAZI\\Desktop\\GIT_PROJECTS\\OpenCV\\Face Recongnition\\HaarCascade\\haarcascade_frontalface_default.xml'
dataset='datasets'
(images,labels,names,)=([],[],{},)
face_cascade=cv2.CascadeClassifier(haar_file)
id=0

def getCustName():
    subdata=input(f"Input Customer Name")
    return subdata

def collectSamples(dataset,subdata):
    path=os.path.join(dataset,subdata)
    #If path is available or not
    if not os.path.isdir(path):
        os.mkdir(path)
    (width,height)=(130,100)
    #uploaded haar alogrithm to classifier
    face_cascade=cv2.CascadeClassifier(haar_file)
    #initialize camera
    webcam=cv2.VideoCapture(0)
    print(webcam)
    count=1
    while count<31: #Capturing 30 images
        print(count)
        (ret,img)=webcam.read() #read camera

        gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale img
        facesFound= face_cascade.detectMultiScale(gray_img,1.32,3) #get coordinates of faces
        for (x,y,w,h) in facesFound:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle arround faces found
            faceFound=gray_img[y:y+h,x:x+w] #crop face part for dataset
            face_resized=cv2.resize(faceFound,(width,height))
            cv2.imwrite('%s/%s.png'%(path,count),face_resized)
        count+=1
        cv2.namedWindow("Registration", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Registration", 650, 150)
        cv2.resizeWindow('Registration', 640,420)
        cv2.imshow('Registration',img)
        key=cv2.waitKey(10)
        if key==27:
            break

    webcam.release()
    cv2.destroyAllWindows()

def registerCustomer(subdata):
    with open('Registration_Details.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            print(nameList)
        if subdata not in nameList:
            now = datetime.now()
            dt_String = now.strftime('%H:%M:%S')
            f.writelines(f"\n{subdata},{dt_String}")
            return ("Customer Register Succesfuly")
        else:
            return ("Customer Already Registered")

def draw_rect(img, facesFound):
    (x, y, w, h) = facesFound
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), thickness=5)

def put_text(img, text, x, y):
    cv2.putText(img, text, (x -10, y + 230), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0),2 )

def CustomerWelcome(custName):
    with open('Customer_Details.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            print(nameList)
        if custName not in nameList:
            print('Welcome Customer')
            now = datetime.now()
            dt_String = now.strftime('%H:%M:%S')
            f.writelines(f'\n{custName},{dt_String}')
        else:
            print('Customer Already was there')

def loadDataset():
    (images,labels,names,id)=([],[],{},0)
    for (subdirs,dirs,files) in os.walk(dataset):
        for subdir in dirs: #Loop through each person folder
            names[id]=subdir #Assining name of perso
            subjectpath=os.path.join(dataset,subdir)#dataset/person1
            for filename in os.listdir(subjectpath): #Loop through each img name
                imgpath=subjectpath+'/'+filename #datasetperson1/1.png
                label=id
                images.append(cv2.imread(imgpath,0))
                labels.append(int(label))
            id=id+1 #Walk to second person folder
   
    
    #images = contain now 60 images and we have 60 labels
    (images,labels)=[numpy.array(lis) for lis in [images,labels]]
    print(images,labels)
    return images,labels,names
   

def loadAlgorithm(images,labels):
    face_recognizer_model = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer_model.train(images,labels)
    print('Training Complete')
    return face_recognizer_model

def detectCustomer(face_recognizer_model,names):
    webcam=cv2.VideoCapture(0)
    cnt=0
    (width,height)=(130,100)
    while True:
        (ret,img)=webcam.read() #read camera
        gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale img
        facesFound= face_cascade.detectMultiScale(gray_img,1.32,3) #get coordinates of faces
        for (x,y,w,h) in facesFound:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle arround faces found
            faceFound=gray_img[y:y+h,x:x+w] #crop face part for dataset
            face_resized=cv2.resize(faceFound,(width,height))
            label,confidence= face_recognizer_model.predict(face_resized)
            draw_rect(img, (x,y,w,h))
            predicted_name = names[label]
            print(predicted_name)
            print(confidence)
            if confidence<70:
                put_text(img, predicted_name+str(confidence), x, y)
                CustomerWelcome(predicted_name)
            else:
                put_text(img,"Unregistred Customer", x, y)

        cv2.imshow('Detection',img)
        key = cv2.waitKey(10)
        if key == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


# images,labels,names=loadDataset()
# face_recognizer_model=loadAlgorithm(images,labels)
# detectCustomer(face_recognizer_model,names)