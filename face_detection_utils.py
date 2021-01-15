
import cv2
import numpy as np
from PIL import Image #pillow package
import os

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(-1)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.cascade_path = "haarcascade_frontalface_default.xml"
        self.trained_loc = "trainer/trainer.yml" 
        self.recognizer.read(self.trained_loc)
        self.faceCascade = cv2.CascadeClassifier(self.cascade_path)
        self.i = 0


    def __del__(self):
        self.video.release()
        
    def create_dataset(self,face_id):
        self.video.set(3, 640) # set video width
        self.video.set(4, 480) # set video height

        #make sure 'haarcascade_frontalface_default.xml' is in the same folder as this code

        # For ea ch person, enter one numeric face id (must enter number start from 1, this is the lable of person 1)

        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0

        #start detect your face and take 30 pictures
        while(True):

            ret, img = self.video.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])


            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        self.video.release()
        cv2.destroyAllWindows()

    def getImagesAndLabels(self,path):

            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []
            detector = cv2.CascadeClassifier(self.cascade_path)
            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img,'uint8')

                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids
            
    def train_model(self,path):
        camera = VideoCamera()
        # Path for face image database
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = camera.getImagesAndLabels(path)
        self.recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        self.recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        self.video.release()
        cv2.destroyAllWindows()
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    def run_model(self,names,n_of_persons):
        #Parameters
        #n_of_persons--> number of persons which the model should recognise(INT)
        #names --> names of the persons you want to recognise(array)yth

        font = cv2.FONT_HERSHEY_SIMPLEX
        #iniciate id counter, the number of persons you want to include
        # Initialize and start realtime video capture
        self.video.set(3, 640) # set video widht
        self.video.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        minW = 0.1*self.video.get(3)
        minH = 0.1*self.video.get(4)
        
        

        while True:
            ret, img = self.video.read()
            try:
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            except:
                self.video.release()
                cv2.destroyAllWindows()
                self.video = cv2.VideoCapture(0)
                ret, img = self.video.read()
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                confidence_calc = 100-confidence
                if (confidence_calc > 0):
                    id = names[id]
                    confidence = "  {0}%".format(round(confidence_calc))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(confidence_calc))
                
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                #break
            ret , jpeg = cv2.imencode('.jpg',img)
            return jpeg.tobytes()
