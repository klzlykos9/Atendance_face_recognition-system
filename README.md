Face Attendance System (Flask + OpenCV LBPH)

A lightweight, real-time face attendance system built using Flask, OpenCV (LBPH), Haar Cascade, WebcamJS, and SQLite.
The system allows users to register with 30 auto-captured face images, train a recognition model, and mark attendance instantly through a web interface.

📌 Features

Real-time face capture using WebcamJS

Auto-capture of 30 images per student for training

LBPH Face Recognition for high accuracy with low compute

Haar Cascade Face Detection

Modern, responsive UI (Bootstrap 5)

SQLite database for students & attendance records

Model training dashboard

Attendance marking with live camera

Delete student + attendance data

Fully modular folder structure

📂 Project Structure
face_attendance_ui_upgrade/
│── app.py
│── init_db.py
│── requirements.txt
│── /database
│     └── attendance.db
│── /model
│     └── trainer.yml
│── /dataset
│     └── <captured images>
│── /static
│     ├── /css
│     │    └── style.css
│     └── /js
│          ├── register.js
│          ├── attendance.js
│── /templates
│     ├── base.html
│     ├── register.html
│     ├── train_page.html
│     ├── attendance.html
│     └── records.html
└── haarcascade_frontalface_default.xml

🛠️ Technologies Used

Python 3

Flask

OpenCV

LBPH Face Recognizer

Haar Cascade

WebcamJS

Bootstrap 5

SQLite

🚀 Installation
1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Create a virtual environment
python -m venv myenv

3. Activate environment

Windows:

myenv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

5. Initialize the database
python init_db.py

6. Run the app
python app.py


The server will run at:
👉 http://127.0.0.1:5000

📷 How It Works
1. Register Student

Fill the student form

Start camera

System auto-captures 30 images

After capturing, click Save Registration

2. Train Model

Go to Train Model page

Click Train LBPH Model

A new trainer.yml file is created

3. Mark Attendance

Go to Attendance

Camera will detect & recognize your face

Attendance is logged automatically

🧹 Delete Student / Attendance

The system allows deleting:

A student

Their dataset images

Their attendance logs

Their trained model entries
