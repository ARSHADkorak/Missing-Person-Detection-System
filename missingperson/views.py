from django.shortcuts import render,redirect
from .models import* 
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
import face_recognition
import cv2
from django.shortcuts import get_object_or_404, redirect
from .models import MissingPerson
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request,"index.html")
def detect(request):
    video_capture_0 = cv2.VideoCapture(0)
    video_capture_1 = cv2.VideoCapture(1)
    desired_width = 640
    desired_height = 480
    # Initialize a flag to track if a face has been detected in the current video stream
    face_detected = False
    scanning_active = False

    while True:

        ret0, frame0 = video_capture_0.read()
        ret1, frame1 = video_capture_1.read()
        frame0 = cv2.resize(frame0, (desired_width, desired_height))
        frame1 = cv2.resize(frame1, (desired_width, desired_height))
        # Find face locations and encodings in the current frame
        face_locations_0 = face_recognition.face_locations(frame0)
        face_locations_1 = face_recognition.face_locations(frame1)
        face_encodings_0 = face_recognition.face_encodings(frame0, face_locations_0)
        face_encodings_1 = face_recognition.face_encodings(frame1, face_locations_1)
        
        face_encodings = face_encodings_0 + face_encodings_1
        face_locations = face_locations_0 + face_locations_1
        
        for i, (face_encoding, (top, right, bottom, left)) in enumerate(zip(face_encodings, face_locations)):
            # Compare detected face with stored face images
            for person in MissingPerson.objects.all():
                stored_image = face_recognition.load_image_file(person.image.path)
                stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

                # Compare face encodings using a tolerance value
                #tolerance = 0.6  # Adjust this tolerance as needed
                matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)

                if any(matches):
                    name = person.first_name + " " + person.last_name
                    
                    if i < len(face_locations_0):
                        camera_number = 0
                    else:
                        camera_number = 1

                    if (camera_number==0):  # If camera 0 is capturing frames
                        cv2.rectangle(frame0, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame0, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        cv2.imshow('Camera Feed0', frame0)
                    elif (camera_number==1):  # If camera 1 is capturing frames
                        cv2.rectangle(frame1, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame1, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        cv2.imshow('Camera Feed1', frame1)

                    # Check if a face has already been detected in this video stream
                    if not face_detected:
                        print("Hi " + name + " is found")
                        
                        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
                        subject = 'Missing Person Found'
                        from_email = 'arshad712003@gmail'
                        recipientmail = person.email
                        recipient_phone_number = '+91'+str(person.phone_number)
                        print(recipient_phone_number)
                        context = {"first_name":person.first_name,"last_name":person.last_name,
                                    'fathers_name':person.father_name,"aadhar_number":person.aadhar_number,
                                    "missing_from":person.missing_from,"date_time":current_time,"location":"India","camera_number":camera_number}
                        html_message1 = render_to_string('findemail.html',context = context)
                        # Send the email
                        send_mail(subject,'', from_email, [recipientmail], fail_silently=False, html_message=html_message1)
                        face_detected = True  # Set the flag to True to indicate a face has been detected
                        # Break the loop once a match is found        
                        break
                        # Check if no face was detected in the current frame
        cv2.imshow('Camera Feed0', frame0)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_detected = False
            print("Redirecting...")
            return redirect('detect')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Camera Feed1', frame1)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_detected = False
            print("Redirecting...")
            return redirect('detect')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture_0.release()
    video_capture_1.release()
    cv2.destroyAllWindows()
    return render(request, "surveillance.html")

def surveillance(request):
    return render(request,"surveillance.html")


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('fathers_name')
        date_of_birth = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenum')
        aadhar_number = request.POST.get('aadhar_number')
        missing_from = request.POST.get('missing_date')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        aadhar = MissingPerson.objects.filter(aadhar_number=aadhar_number)
        if aadhar.exists():
            messages.info(request, 'Aadhar Number already exists')
            return redirect('/register')
        person = MissingPerson.objects.create(
            first_name = first_name,
            last_name = last_name,
            father_name = father_name,
            date_of_birth = date_of_birth,
            address = address,
            phone_number = phone_number,
            aadhar_number = aadhar_number,
            missing_from = missing_from,
            email = email,
            image = image,
            gender = gender,
        )
        person.save()
        messages.success(request,'Case Registered Successfully')
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        subject = 'Case Registered Successfully'
        from_email = 'arshad712003@gmail'
        recipientmail = person.email
        context = {"first_name":person.first_name,"last_name":person.last_name,
                    'fathers_name':person.father_name,"aadhar_number":person.aadhar_number,
                    "missing_from":person.missing_from,"date_time":current_time}
        html_message2 = render_to_string('regmail.html',context = context)
        # Send the email
        send_mail(subject,'', from_email, [recipientmail], fail_silently=False, html_message=html_message2)

    return render(request,"register.html")


def  missing(request):
    queryset = MissingPerson.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(aadhar_number__icontains=search_query)
    
    context = {'missingperson': queryset}
    return render(request,"missing.html",context)

def delete_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)
    person.delete()
    return redirect('missing')  # Redirect to the missing view after deleting


def update_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)

    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.POST.get('first_name', person.first_name)
        last_name = request.POST.get('last_name', person.last_name)
        fathers_name = request.POST.get('fathers_name', person.father_name)
        dob = request.POST.get('dob', person.date_of_birth)
        address = request.POST.get('address', person.address)
        email = request.POST.get('email', person.email)
        phonenum = request.POST.get('phonenum', person.phone_number)
        aadhar_number = request.POST.get('aadhar_number', person.aadhar_number)
        missing_date = request.POST.get('missing_date', person.missing_from)
        gender = request.POST.get('gender', person.gender)

        # Check if a new image is provided
        new_image = request.FILES.get('image')
        if new_image:
            person.image = new_image

        # Update the person instance
        person.first_name = first_name
        person.last_name = last_name
        person.father_name = fathers_name
        person.date_of_birth = dob
        person.address = address
        person.email = email
        person.phone_number = phonenum
        person.aadhar_number = aadhar_number
        person.missing_from = missing_date
        person.gender = gender

        # Save the changes
        person.save()

        return redirect('missing')  # Redirect to the missing view after editing

    return render(request, 'edit.html', {'person': person})
