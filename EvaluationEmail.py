import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from q import time_function
from Evaluation import get_passed_and_failed_profiles

def send_email(sender_email, password, receiver_list, subject, text, html):
    for email in receiver_list:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = email

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())

        sleep(3)


@time_function
def send_passed_emails():
    sender_email = "doodlerecruiter@gmail.com"
    password = "esaogflkteymkeyd"
    receiver_list = get_passed_and_failed_profiles()[0]
    subject = "Doodle Cooding Assessment Results"
    text = """\
        Hi,
        this is regarding the coding interview 
        www.doodlerecruiter.com"""
    html = """\
        <html>
          <body>
            <p>Hi,<br>
               this is regarding the coding interview results, Congrats, you have selected for further round.  <br>
               <a href=""></a> 

            </p>
          </body>
        </html>
        """
    send_email(sender_email, password, receiver_list, subject, text, html)


@time_function
def send_failed_emails():
    sender_email = "doodlerecruiter@gmail.com"
    password = "esaogflkteymkeyd"
    receiver_list = get_passed_and_failed_profiles()[1]
    subject = "Doodle Cooding Assessment Results"
    text = """\
        Hi,
        this is regarding the coding interview that has been attached below and link we valid for only 48 hours starting from today
        www.doodlerecruiter.com"""
    html = """\
        <html>
          <body>
            <p>Hi,<br>
               this is regarding the coding interview results, Unfortunately, you have not selected for further rounds <br>
               <a href=""></a> 

            </p>
          </body>
        </html>
        """
    send_email(sender_email, password, receiver_list, subject, text, html)


if __name__ == '__main__':
    send_passed_emails()
    send_failed_emails()
