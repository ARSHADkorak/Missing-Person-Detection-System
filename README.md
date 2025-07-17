🧠 Missing Person Detection System (Multi-Camera, Django-Based)
This project is a Django-based smart surveillance system to detect and track missing persons in real-time using multiple camera streams. The system uses deep learning for face recognition and integrates with Django for backend management and database operations.

🚀 Key Features
🔍 Face detection and recognition using machine learning

🎥 Supports multi-camera streaming for wide area surveillance

🧑‍💻 Admin panel to manage missing persons and logs

📊 Stores sightings with timestamps and locations in the database

🌐 Web-based dashboard (via Django admin)

⚙️ Prerequisites
Python 3.x

Django 3.x or 4.x

OpenCV

dlib / face_recognition

NumPy

📥 Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/Missing-Person-Detection-System.git
cd Missing-Person-Detection-System/core
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run migrations

bash
Copy
Edit
python manage.py migrate
Create superuser for admin access

bash
Copy
Edit
python manage.py createsuperuser
Run the server

bash
Copy
Edit
python manage.py runserver
🧪 Running Tests
bash
Copy
Edit
python manage.py test
🎥 Multi-Camera Support
Your system now uses multiple camera inputs. To enable that:

Update your camera feed configurations in a module like camera_stream.py (or any equivalent).

Use threading or multiprocessing to read and analyze multiple video feeds concurrently.

Each camera processes frames independently and checks against the encoded face data.

🔐 Django Admin Panel
Visit http://127.0.0.1:8000/admin to:

Add or update MissingPerson profiles

Review captured Location sightings

Manage the face dataset and configure alerts

📌 Future Enhancements
Add REST API for real-time alerts

Integrate Twilio/SMTP for SMS or email notifications

Add public-facing search interface (for family/public access)

Support cloud deployment for scalable camera sources


