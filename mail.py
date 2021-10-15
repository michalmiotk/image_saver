import smtplib
import imghdr
from email.message import EmailMessage
from email.mime.image import MIMEImage

def send_mail(sender_mail, sender_pass, image_bytes,  image_name='some.jpeg'):
    Sender_Email = sender_mail
    Reciever_Email = sender_mail
    Password = sender_pass
    newMessage = EmailMessage()
    newMessage['Subject'] = "Check out the new logo"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    newMessage.set_content('Let me know what you think. Image attached!')
    newMessage.add_attachment(image_bytes, maintype='image',
                    subtype=imghdr.what(None, image_bytes), filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)