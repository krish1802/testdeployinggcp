from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify,redirect,session
import os
from FormDetection import TestingMain
from flask_pymongo import PyMongo
import urllib.parse
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    detailedAnalysis = db.Column(db.Boolean, default=False)
    nutritionAnalysis = db.Column(db.Boolean, default=True)
    traingpt = db.Column(db.Boolean, default=False)


    def __init__(self,email,password,name, detailedAnalysis=False, nutritionAnalysis=True, traingpt=False):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.detailedAnalysis = detailedAnalysis
        self.nutritionAnalysis = nutritionAnalysis
        self.traingpt = traingpt
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()



@app.route('/testing')
def testing():
    hello_text = "hello world"
    return render_template('testing_text.html', hello_text=hello_text)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    global user
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            session['nutritionAnalysis'] = user.nutritionAnalysis
            session['detailedAnalysis'] = user.detailedAnalysis
            session['traingpt'] = user.traingpt
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')


def detailed_analysis_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('detailedAnalysis'):
            return redirect(url_for('login'))  # Redirect to login page if detailedAnalysis is not set
        return f(*args, **kwargs)
    return decorated_function

def nutrition_analysis_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('nutritionAnalysis'):
            return redirect(url_for('login'))  # Redirect to login page if detailedAnalysis is not set
        return f(*args, **kwargs)
    
    return decorated_function

def traingpt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('traingpt'):
            return redirect(url_for('login'))  # Redirect to login page if detailedAnalysis is not set
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

@app.route('/indexLoggedin')
def indexLoggedin():
    return render_template('indexLoggedin.html')

@app.route('/grantNutrition')
def grantNutrition():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.nutritionAnalysis = True
            db.session.commit()
            return redirect(url_for('nutrition'))
    
    return redirect(url_for('login'))

@app.route('/grantAnalysis')
def grantAnalysis():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.detailedAnalysis = True
            db.session.commit()
            return redirect(url_for('index'))
    
    return redirect(url_for('login'))

@app.route('/grantTraingpt')
def grantTraingpt():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.traingpt = True
            db.session.commit()
            return redirect(url_for('home'))
    
    return redirect(url_for('login'))

@app.route('/nutrition')
# @nutrition_analysis_required
def nutrition():
    return render_template('nutrition.html')

@app.route('/core')
def core():
    return render_template('core.html')




@app.route('/chest')
def chest():
    return render_template('chest.html')

@app.route('/back')
def back():
    return render_template('back.html')

@app.route('/legs')
def legs():
    return render_template('legs.html')

@app.route('/arms')
def arms():
    return render_template('arms.html')

@app.route('/shoulder')
def shoulder():
    return render_template('shoulder.html')

@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/formdetection')
def formdetection():
    global exercise_name
    exercise_name = request.args.get("my_variable")
    return render_template('formdetection.html')

@app.route('/cs')
def cs():
    return render_template('cs.html')

def remove_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{filename}' removed successfully.")
    else:
        print(f"File '{filename}' does not exist.")

def convert_video_supported(videofile):
    with lock:
        output_file = f'static/outputs/convertedOutput.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            new_filename, extension = os.path.splitext(output_file)
            output_file = f"{new_filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        os.system(f"ffmpeg -i {videofile} -vcodec libx264 -acodec aac -strict -2 {output_file}")
        return output_file



import queue
import threading
import time

filename_queue = queue.Queue()
lock = threading.Lock()
# Function to process tasks

app.config['UPLOAD_FOLDER'] = "uploads/"

@app.route('/upload', methods=['POST'])
def upload_file():
    with lock:
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file:
            global filename
            filename = "formDetection.mp4"
            count = 1
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                # If the filename already exists, append a number to make it unique
                filename, file_extension = os.path.splitext("formDetection.mp4")
                filename = f"{file.filename}{count}{file_extension}"
                count += 1

            file.filename = filename
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('detailedAnalysis'))




@app.route('/download')
def download_file():
    with lock:
        global exercises
        global performanceFile
        global response
        global result
        global performanceSecFile
        result = ""
        exercises = TestingMain()
        performanceFile = None
        performanceSecFile = None
        if exercise_name == "bicepcurls" or exercise_name == "hammercurls":
            exercises.bicepCurls(filename_input=filename)
            result = convert_video_supported(exercises.output_file)
            response = send_file(result, as_attachment=True) # FOR DOWNLOADING
            performanceFile =  exercises.performanceFile
            performanceSecFile = exercises.secPerformanceFile
        else:
            return redirect(url_for('index'))

@app.route('/downloadvideo')
def download_video():
    return response


@app.route('/detailedAnalysis')
def detailedAnalysis():
    if exercise_name == "bicepcurls" or exercise_name == "hammercurls":
        download_file()
    secLines = 0
    with open(performanceFile, "r") as file:
        lines = len(file.readlines())
    if performanceSecFile is not None:
        with open(performanceSecFile, "r") as file:
            secLines = len(file.readlines())
    score = ""
    scoreColor = ""
    if exercise_name in ["bicepcurls", "hammercurls", "benchtricepdips", "cablerows", "ropepushdowns", "triceppushdown", "tbarrows", "dumbbellrows", "bentoverrows", "deadlift"]:
        
        if lines <= 2 and secLines <= 2:
            score = "Your Score 10/10"
            scoreColor = "yellowgreen"
            headingText = ""
            textColor = "greenyellow"
            detailText = "You were stable the whole time"
        else:
            if exercise_name == "deadlift":
                if 5 >= lines >2 or 5 >= secLines > 2:
                    score = "Your Score: 5/10"
                    scoreColor = "red"
                elif lines > 5 or secLines > 5:
                    score = "Your Score: 2/10"
                    scoreColor = "darkred"
            else:
                if 5 > lines >= 3 or 4>= secLines > 2:
                    score = "Your Score:  8/10"
                    scoreColor = "green"
                elif 8> lines >= 5 or 8>= secLines > 4:
                    score = "Your Score:  6/10"
                    scoreColor = "yellow"
                elif 10> lines >= 8 or 14>= secLines > 8:
                    score = "Your Score:  4/10"
                    scoreColor = "red"
                elif lines >= 10 or secLines > 14:
                    score = "Your Score:  2/10"
                    scoreColor = "darkred"
            textColor = "yellow"
            if exercise_name == "bicepcurls" or exercise_name == "hammercurls":
                headingText = "Your back was unstable"
                detailText = "Focus on maintaining a strong, straight posture as you perform each bicep curl. Stand tall with your feet shoulder-width apart, engage your core, and keep your chest lifted. Imagine a string pulling the top of your head toward the ceiling, elongating your spine. Keep your shoulders back and down, away from your ears. As you lift and lower the weights, ensure your back remains straight and your movements controlled. This will not only protect your back but also maximize the effectiveness of your bicep workout. Stay strong, stay focused, and keep your form impeccable!"
            if exercise_name == "benchtricepdips":
                headingText = "Your legs weren't straight"
                detailText = "To keep your legs straight while doing bench tricep dips, start by adjusting your position. Sit on the edge of the bench and place your hands shoulder-width apart on the bench's edge. Slide off the bench and extend your legs out in front of you, placing your heels on the ground with your toes pointing upward to help maintain straight legs. Engage your core muscles to stabilize your body, which aids in keeping your legs straight. As you perform the dip, focus on lowering your body in a straight line from head to heels, avoiding any bending at the knees or hips. If you find it difficult to keep your legs straight, consider placing your feet on another bench or step for added support. Additionally, work on improving your hamstring flexibility and leg strength to make it easier to maintain the correct form. Proper form is crucial for both effectiveness and preventing injury."
            if exercise_name == "cablerows" and lines > 2 and secLines >2:
                headingText = "You hands are too high and your upper body is unstable"
                detailText = "Try to keep your Body entact with your hands coming close to your hips while every rep performed, feeling a squeeze in your back while pulling and stretch in your back while releasing. Your Upper body is moving too much, please refer to the video and analyse where you are going wrong. Try to keep your upper body within the angle range as observed in the analysis video"
            if exercise_name == "cablerows" and lines > 2:
                detailText = "Try to keep your Body entact with your hands coming close to your hips while every rep performed, feeling a squeeze in your back while pulling and stretch in your back while releasing. "
                headingText = "Your hands were too high"
            if exercise_name == "cablerows" and secLines > 2:
                detailText = "Your Upper body is moving too much, please refer to the video and analyse where you are going wrong. Try to keep your upper body within the angle range as observed in the analysis video"
                headingText = "Your upper body was unstable"
            if exercise_name == "deadlift":
                headingText = "Your back was unstable"
                detailText = "To maintain a stable body and a straight back during a deadlift, start by positioning your feet shoulder-width apart with the barbell over the middle of your feet. Bend at the hips and knees to grip the bar with your hands just outside your knees. Ensure your back is flat, your chest is up, and your shoulders are back and down, avoiding any rounding of the upper or lower back. Engage your core muscles to create intra-abdominal pressure, which helps stabilize your spine. As you lift the bar, drive through your heels and extend your hips and knees simultaneously, keeping the bar close to your body and maintaining a neutral spine throughout the lift. Avoid hyperextending your back at the top of the movement. On the way down, reverse the motion by hinging at the hips first, then bending your knees, and always maintaining control and proper form. Proper breathing, bracing, and attention to form are crucial to preventing injury and ensuring a strong, stable back throughout the deadlift."
            if exercise_name == "tbarrows" or exercise_name == "dumbbellrows" or exercise_name == "bentoverrows":
                headingText = "Your back was unstable"
                detailText = "To maintain a stable back during rowing exercises, focus on engaging your core and maintaining proper posture throughout the movement. Start by sitting tall with your shoulders back and down, avoiding any hunching or rounding of the back. Keep your chest lifted and your gaze forward to ensure a neutral spine. As you initiate the row, hinge at the hips rather than rounding your lower back, and use your legs to drive the motion while your upper body follows in a coordinated manner. Engage your abdominal muscles to provide additional support and prevent excessive arching or rounding. Throughout the exercise, be mindful of your form, making necessary adjustments to maintain a straight, strong back, and avoid straining or injuring your spine."
            
            if exercise_name == "triceppushdown" or exercise_name == "ropepushdowns":
                headingText = "Your shoulders were not in place or Your Shoulder was unstable, check the result video for detailed analysis"
                detailText = "To ensure your shoulders are placed correctly during a tricep rope pushdown, start by positioning yourself with a stable stance, feet shoulder-width apart. Adjust the cable machine so that the rope attachment is at chest height. Stand close to the machine and grasp the rope with both hands, palms facing each other. Engage your core and keep your back straight to stabilize your body. Position your shoulders down and back, away from your ears, to avoid shrugging. Keep your elbows close to your sides and maintain a slight bend in them throughout the exercise. As you push the rope down, focus on using your triceps and avoid letting your shoulders roll forward or hunch up. By maintaining this proper alignment, you'll ensure that the tricep rope pushdown is both effective and safe, reducing the risk of shoulder strain."
    else:
        return render_template(url_for("index"))
    return render_template('download.html', detailText=detailText, textColor=textColor, headingText=headingText ,result=result, score=score, scoreColor=scoreColor)


client = OpenAI(api_key="")
# Encode username and password
username = urllib.parse.quote_plus('krish1802')
password = urllib.parse.quote_plus('Krish@1802')

# Construct the MongoDB connection URI with the encoded username and password
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@traingpt.ldaljff.mongodb.net/TrainGPT"

# Initialize PyMongo with the Flask app
mongo = PyMongo(app)

from datetime import datetime
  
date = f"It's now {datetime.now()}"

from bson import json_util

@app.route("/traingpt")
# @traingpt_required
def home(): 
    chats = mongo.db.chats.find({})
    # Convert ObjectId to string for JSON serialization
    myChats = json_util.dumps(chats)
    return render_template("traingpt.html", myChats=myChats)

from bson import ObjectId

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        if chat:
            data = {"answer": chat["answer"]}
            return jsonify(data)
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response.choices[0].message.content
            data = {"question": question, "answer": answer}
            # Convert ObjectId to string before inserting into MongoDB
            data["_id"] = str(ObjectId())
            # mongo.db.chats.insert_one(data)
            print(data['answer'])
            return jsonify(data)
    return jsonify({"error": "Invalid request method"})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

