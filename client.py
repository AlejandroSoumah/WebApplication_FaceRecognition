
from flask import Flask, render_template, Response,request,redirect
from face_detection_utils import VideoCamera

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "POST":
        req = request.form
        User_1 = req["User1"]
        global names
        names = ["",User_1]
        if 'Run' in request.form:
            return render_template('index.html')

        if 'Create_Dataset' in request.form:
            face_id=1
            camera = VideoCamera()
            camera.create_dataset(face_id)
            #Print Image Dataset Created correctly
            return render_template('index.html')
            

        if 'Train_Dataset' in request.form:
            camera = VideoCamera()
            camera.train_model("dataset")
            #Print Image Train done correctly
            return render_template('processing.html')

    return render_template('index.html')

def gen(camera):
    while True:
        #Always use camera.get_frame()
        frame = camera.run_model(names,1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed', methods=["GET","POST"])
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
