import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from q import time_function


@time_function
def Emailsender():
    sender_email = "doodlerecruiter@gmail.com"

    receiver_list = ["rohan.kulkarni2802@gmail.com", "manjunathbhaskar23@gmail.com", "deepaksn.dn@gmail.com"]
    password = "esaogflkteymkeyd"

    for email in receiver_list:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Doodle Cooding Assessment"
        message["From"] = sender_email
        message["To"] = email

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        this is regarding the coding interview that has been attached below and link we valid for only 48 hours starting from today
        www.doodlerecruiter.com"""
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               this is regarding the coding interview that has been attached below and link we valid for only 48 hours starting from today <br>
               <a href="https://presenter.jivrus.com/p/131nxq-9OP4gLGNGhxUNiYfmCrs8H6hptS02aBps9nr4">Coding Assessment</a> 

            </p>
          </body>
        </html>
        """

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


if __name__ == '__main__':
    Emailsender()
