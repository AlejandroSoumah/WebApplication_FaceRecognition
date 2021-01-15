from flask import Flask
from flask import render_template, Response,request,redirect,flash
from face_detection_utils import VideoCamera
import os
import os.path
#import flask_profiler
app = Flask(__name__)
app.secret_key = 'eRqUle$'

global names,n_of_users
#Assume he specifies the number of users correctly
Instance = VideoCamera()
@app.route('/',methods=["GET","POST"])
def index():
    try:
        if request.method == "POST":
            req = request.form
            user_1 = req["User1"]
            user_2 = req["User2"]
            

            if 'Erase_Data' in request.form:
                dirs = os.listdir("dataset/")
                for file in dirs:
                    os.remove("dataset/"+file)

            if 'Create_Dataset_User1' in request.form:
                if user_1 == "":
                    error = "You need to type the name of User 1 in order to create the dataset"
                    flash(error)
                    return render_template('index.html')
                else:
                    face_id=1
                    print("1")
                    Instance.create_dataset(face_id)
                    print("Creating Dataset User1")
                    Instance.train_model("dataset")
                    print("Training Dataset")
                    #trained completed
                    return render_template('index.html')

            if 'Create_Dataset_User2' in request.form:
                if user_2 == "":
                    error = "You need to type the name of User 2 in order to create the dataset"
                    flash(error)
                    return render_template('index.html')
                else:
                    face_id=2
                    Instance_Dataset2 = VideoCamera()
                    Instance_Dataset2.create_dataset(face_id)
                    print("Creating Dataset User2")
                    Instance_Dataset2.train_model("dataset")
                    print("Training Dataset")
                    return render_template('index.html')

            if 'Run' in request.form:  
                if user_1 == "" and user_2 == "":
                    error = "You need to type the names of User 1 and User 2 in order to execute" 
                    flash(error)
                    return render_template('index.html')         

                if user_1 == "":
                    error = "You need to type the name of User 1 in order to execute"
                    flash(error)
                    return render_template('index.html')

                if user_2 == "":
                    user_1_path = "dataset/User.1.2.jpg"
                    if os.path.exists(user_1_path):
                        global names,n_of_users
                        names = ["",user_1]
                        n_of_users = 1
                        return render_template('index_camera.html')
                    else:
                        error = "You need to create dataset of User 1 in order to execute" 
                        flash(error)
                        return render_template('index.html')         

                else:
                    user_1_path = "dataset/User.1.2.jpg"
                    user_2_path = "dataset/User.2.2.jpg"
                    if os.path.exists(user_1_path) and os.path.exists(user_2_path):
                        names = ["",user_1,user_2]
                        n_of_users = 2
                        return render_template('index_camera.html')
                    else:
                        error = "You need to create dataset of User 1 and User 2 in order to execute" 
                        flash(error)
                        return render_template('index.html') 
                    
#Check that everything works perfectly
#Then the video and notifications


    except Exception as e :
        
        error = "An error has occured, read the instructions and repeat the process"
        print(e)
        flash(error)
        return render_template('ErrorPage.html')

    return render_template('index.html')

def gen():
        while True:
            #Always use camera.get_frame()
            frame = Instance.run_model(names,n_of_users)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed', methods=["GET","POST"])
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    #Profiler(app)
    app.run(host='127.0.0.1', debug=False)
    
