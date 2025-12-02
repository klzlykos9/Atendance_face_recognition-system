from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os,cv2,base64
from io import BytesIO
from PIL import Image
import numpy as np
from datetime import datetime

app=Flask(__name__)
BASE=os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]=f"sqlite:///{os.path.join(BASE,'database','attendance.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,unique=True)
    name=db.Column(db.String(100))
    roll_no=db.Column(db.String(100))
    email=db.Column(db.String(200))

class Attendance(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer)
    time_in=db.Column(db.String(100))

@app.route('/')
def reg(): return render_template("register.html")
@app.route('/train_page')
def tp(): return render_template("train.html")
@app.route('/attendance')
def att(): return render_template("attendance.html")
@app.route('/records')
def rec():
    rows=db.session.query(
        Attendance.student_id,Attendance.time_in,
        Student.name,Student.roll_no,Student.email
    ).join(Student,Student.student_id==Attendance.student_id).all()
    data=[{"student_id":r[0],"time_in":r[1],"name":r[2],"roll_no":r[3],"email":r[4]} for r in rows]
    return render_template("records.html",data=data)

@app.route('/register',methods=["POST"])
def register():
    d=request.get_json()
    sid=int(d["student_id"])
    name=d["name"]
    folder=f"{sid}_{name.replace(' ','_')}"
    path=os.path.join(BASE,"dataset",folder)
    os.makedirs(path,exist_ok=True)
    stu=Student(student_id=sid,name=name,roll_no=d["roll_no"],email=d["email"])
    db.session.add(stu); db.session.commit()
    for i,img in enumerate(d["images"]):
        raw=base64.b64decode(img.split(",")[1])
        Image.open(BytesIO(raw)).convert("L").save(os.path.join(path,f"img_{i+1}.jpg"))
    return {"status":"success","message":"Registered"}

@app.route('/train')
def train():
    dataset=os.path.join(BASE,"dataset")
    model=os.path.join(BASE,"model","trainer.yml")
    face=cv2.CascadeClassifier(os.path.join(BASE,"haarcascade_frontalface_default.xml"))
    rec=cv2.face.LBPHFaceRecognizer_create()
    faces=[]; ids=[]
    for f in os.listdir(dataset):
        fp=os.path.join(dataset,f)
        if not os.path.isdir(fp): continue
        sid=int(f.split("_")[0])
        for im in os.listdir(fp):
            g=cv2.imread(os.path.join(fp,im),0)
            det=face.detectMultiScale(g,1.2,5)
            for (x,y,w,h) in det:
                faces.append(g[y:y+h,x:x+w]); ids.append(sid)
    if not faces: return {"status":"error","message":"No faces"}
    rec.train(faces,np.array(ids)); rec.write(model)
    return {"status":"success","message":"Training Done"}

@app.route('/recognize',methods=["POST"])
def recognize():
    d=request.get_json()
    raw=base64.b64decode(d["image"].split(",")[1])
    g=np.array(Image.open(BytesIO(raw)).convert("L"))
    face=cv2.CascadeClassifier(os.path.join(BASE,"haarcascade_frontalface_default.xml"))
    det=face.detectMultiScale(g,1.3,5)
    if not len(det): return {"found":False}
    rec=cv2.face.LBPHFaceRecognizer_create()
    rec.read(os.path.join(BASE,"model","trainer.yml"))
    for (x,y,w,h) in det:
        roi=g[y:y+h,x:x+w]
        label,conf=rec.predict(roi)
        if conf>75: return {"found":False}
        stu=Student.query.filter_by(student_id=label).first()
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(Attendance(student_id=label,time_in=ts)); db.session.commit()
        return {"found":True,"name":stu.name,"roll_no":stu.roll_no,"email":stu.email,"time":ts}
    return {"found":False}

@app.route('/delete/<int:sid>')
def delete(sid):
    import shutil
    ds=os.path.join(BASE,"dataset")
    for f in os.listdir(ds):
        if f.startswith(str(sid)+"_"):
            shutil.rmtree(os.path.join(ds,f))
    Student.query.filter_by(student_id=sid).delete()
    Attendance.query.filter_by(student_id=sid).delete()
    db.session.commit()
    return "<script>alert('Deleted');window.location='/records'</script>"

if __name__=="__main__":
    app.run(debug=True)
