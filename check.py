from smtplib import SMTP_SSL
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import Image

def sendEmail(filepath,subject,body):
  smtp_ssl_host = 'smtp.mail.yahoo.com'  # smtp.mail.yahoo.com
  smtp_ssl_port = 465
  username = 'austinjb32@yahoo.com'
  password = 'ityhbptqwfzwpqou'
  sender = 'austinjb32@yahoo.com'
  targets = ['austinjb32@gmail.com']
  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = ', '.join(targets)
  txt = MIMEText(body)
  msg.attach(txt)
  print(filepath)
  img = MIMEImage(Image.fromarray(filepath))
  img.add_header('Content-Disposition',
  'attachment',
  filename="image.jpeg")
  msg.attach(img)

  server = SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
  server.login(username, password)
  server.sendmail(sender, targets, msg.as_string())
  server.quit()
  