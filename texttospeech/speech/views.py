from django.shortcuts import render
from django.core.mail import EmailMessage
from gtts import gTTS
from django.http import HttpResponse
import PyPDF2
from .models import MyFileModel

def save_files(file,email):
     my_file_instance = MyFileModel()
     email_address = my_file_instance.email_address
     file = my_file_instance.file
     my_file_instance.save()
     print("data saved ")

def speech(request):
    return render(request,"speech/speech.html")

def convert_text_to_speech(email, text):
    print("4")
    # Create a gTTS object with the text
    tts = gTTS(text=text, lang='en')
    print("5")
    # Save the audio as a temporary file
    tts.save('output.mp3')
    print("6")
    # Send the email with the synthesized speech as an attachment
    email_message = EmailMessage(
        'Your synthesized speech', 'Please find your synthesized speech attached.', 'manviraghu357@gmail.com', [email])
    email_message.attach_file('output.mp3')
    email_message.send()
    

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        file = request.FILES.get('file')
        if email and file:
            if file.name.endswith('.pdf'):
                print("came inside if")
                pdf_reader = PyPDF2.PdfReader(file)
                full_text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        print("3")
                        full_text += page_text + " "
                if full_text:
                    tts = gTTS(text=full_text, lang='en')
                    audio_file = "output.mp3"
                    tts.save(audio_file)   
                    email_message = EmailMessage(
                        'Your synthesized speech', 'Please find your synthesized speech attached.', 'manviraghu357@gmail.com', [email])
                    email_message.attach_file(audio_file)
                    email_message.send()
                    save_files(file,email)
                    return HttpResponse("We have sent the audio file. Please check your email.")
                
            else:
                print("Its a text file")
                text = file.read().decode('utf-8')
                print(text)
                save_files(file,email)
                convert_text_to_speech(email, text)
                return HttpResponse("We have sent the audio file. Please check your email.")
    return render(request, 'speech/upload_form.html')