from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
import warnings
import datetime
import cv2
import time
import cv2
import os
import numpy as np
import threading
import mysql.connector


app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Your are Logged In...!")
            return render_template('AdminHome.html', data=data)
        else:
            flash("Username or Password is wrong")
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()

    return render_template('AdminHome.html',data=data)


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + mobile + "','" +  email + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        uname = request.form['uname']
        pas = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + uname + "' and password='" + pas + "'")
        data = cursor.fetchone()
        if data is None:
            flash("UserName or Password is wrong...!")

            return render_template('UserLogin.html')

        else:
            session['mail'] = data[3]
            session['mob'] = data[2]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where UserName='" + uname + "'")
            data = cur.fetchall()
            flash("Your are Logged In...!")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2firedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where UserName='"+ uname +"'")
    data = cur.fetchall()
    return render_template('UserHome.html',data=data)



@app.route("/Test")
def Test():
    import cv2
    from ultralytics import YOLO

    dd1 = 0
    dd2 = 0

    cou1 = 0
    cou2 = 0

    # Load the YOLOv8 model
    model = YOLO('runs/detect/fire/weights/best.pt')

    # video_path = "path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(0)

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.2)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name != 'default':
                        dd1 += 1

                    if dd1 == 30:
                        dd1 = 0
                        cou1 += 1
                        print(cou1)
                        print("Good:" + str(cou1))
                        annotated_frame = results[0].plot()
                        import winsound

                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        cv2.imwrite("alert.jpg", annotated_frame)
                        sendmail()
                        #sendmsg(session['mob'],'Fire Detect')

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    return render_template('UserHome.html')


def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")



def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr =  session['mail']

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Fire  Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)