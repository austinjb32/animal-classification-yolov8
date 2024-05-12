from pathlib import Path
from smtplib import SMTP_SSL
import cv2
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import Image
import mailtrap as mt
import base64
from io import BytesIO
import codecs

# def send_email(frame,subject,body):
#   print("Sending email")
#   smtp_ssl_host = 'smtp.mail.yahoo.com'  # smtp.mail.yahoo.com
#   smtp_ssl_port = 465
#   username = 'austinjb32@yahoo.com'
#   password = 'ityhbptqwfzwpqou'
#   sender = 'austinjb32@yahoo.com'
#   targets = ['austinjb32@gmail.com']
#   msg = MIMEMultipart()
#   msg['Subject'] = subject
#   msg['From'] = sender
#   msg['To'] = ', '.join(targets)
#   txt = MIMEText(body)
#   msg.attach(txt)
#   _, buffer = cv2.imencode(".jpg", frame)
#         # Check if encoding was successful
#   if _:
#         # Convert the buffer to bytes and create a MIMEImage
#         img = MIMEImage(buffer.tobytes())
#         img.add_header('Content-Disposition', 'attachment', filename="image.jpeg")
#         msg.attach(img)
#   else:
#         print("Failed to encode image.")

#   server = SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
#   server.login(username, password)
#   server.sendmail(sender, targets, msg.as_string())
#   print("Sent email successfully")
#   server.quit()


def send_email(frame, subject):
      print("Sending email")

      _, buffer = cv2.imencode(".png", frame)
      img_path = buffer.tobytes()

      mail = mt.MailFromTemplate(
      sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
      to=[mt.Address(email="naveenmoncy05@gmail.com")],
      template_uuid="a0810aad-9a0c-46df-84d7-a5d37a3574b7",
      template_variables={
            "animal": subject,
      },
      attachments=[
            mt.Attachment(
                  filename="animal.png",
                  disposition=mt.Disposition.INLINE,
                  mimetype="image/png",
                  content = base64.b64encode(img_path),
                  content_id="animal.png"
            )
      ],
      )
      client = mt.MailtrapClient(token="f2efe3399bcb4feab576aedebb8c657c")
      client.send(mail)