from flask import Flask, render_template, flash, request, session
import pyttsx3
import mysql.connector

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'





@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('ServerLogin.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fireandsmokedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('ServerHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('ServerLogin.html')



@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sdate =  request.form['sdate']
        edate  =  request.form['edate']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fireandsmokedb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM regtb where date between '" + sdate + "' and '" + edate + "' ")
        data = cur.fetchall()

        return render_template('ServerHome.html', data=data)






@app.route("/ServerHome")
def ServerHome():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fireandsmokedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('ServerHome.html', data=data)

@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fireandsmokedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from regtb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('   Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fireandsmokedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('ServerHome.html', data=data)


@app.route("/Camera")
def Camera():
    import cv2
    from ultralytics import YOLO

    # Load the YOLOv8 model
    model = YOLO('runs/detect/fire/weights/best.pt')
    # Open the video file
    # video_path = "path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(0)
    dd1 = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.4)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name != 'default':
                        dd1 += 1

                    if dd1 == 20:
                        dd1 = 0
                        import winsound

                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        import random
                        loginkey = random.randint(1111, 9999)
                        imgg = "static/upload/" + str(loginkey) + ".jpg"

                        cv2.imwrite("alert.jpg", annotated_frame)
                        cv2.imwrite(imgg, annotated_frame)

                        import datetime
                        date = datetime.datetime.now().strftime('%Y-%m-%d')

                        time = datetime.datetime.now().strftime('%H:%M:%S')

                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='1fireandsmokedb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO regtb VALUES ('','" + date + "','" + time + "','" + object_name + "','" + str(
                                imgg) + "')")
                        conn.commit()
                        conn.close()

                        sendmail()
                        sendmsg("9080725362", "Prediction Name:" + object_name)

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
    return render_template('index.html')



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
    toaddr =  "sujithrasoundarrajan@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Animal  Detection"

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
