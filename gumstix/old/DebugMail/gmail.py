def sendGMail(user, pw, to, subject, text, files=[], server='smtp.gmail.com'): 
   """ 
   Send files using GMail.
   to:
   subject:
   text:
   files:
   """ 
   import smtplib 
   from email.MIMEMultipart import MIMEMultipart 
   from email.MIMEBase import MIMEBase 
   from email.MIMEText import MIMEText 
   from email.Utils import formatdate 
   from email import Encoders 
   from string import split 
   import os 
   from socket import sslerror 
   assert type(files)==list 
 
   fro = user+"@gmail.com" 

   msg = MIMEMultipart() 
   msg['From'] = fro 
   msg['To'] = to 
   msg['Date'] = formatdate(localtime=True) 
   msg['Subject'] = subject 
   msg.attach(MIMEText(text)) 

   for file in files: 
      part = MIMEBase('application', 'octet-stream') 
      part.set_payload(open(file, "rb").read()) 
      Encoders.encode_base64(part) 
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
      msg.attach(part) 
   # Connecting...
   print "BBB" 
   smtp = smtplib.SMTP(server,465) 
   print "a"
   smtp.ehlo() 
   print "b"
   smtp.starttls() 
   print "c"
   smtp.ehlo() 
   print "d"
   smtp.login(user, pw) 
   print "Login succeed" 
   try : 
     smtp.sendmail(fro, to, msg.as_string()) 
     print "Successful" 
   except : 
     print "Couldn't send" 

   smtp.close() 

if __name__ == "__main__": 
   import sys 
   import time 
   lt = sys.argv 
   user = 'netcar.diag' 
   passwd = 'yhunkim' 

   if len(lt) == 0 : sys.exit() 
   while len(lt) : 
     arg = lt.pop(0) 
     if arg.startswith('-i') : 
        user = arg[2:] 
     if arg.startswith('-p') : 
        passwd = arg[2:] 
     if user != '' and passwd != '' : 
        break 

   if user == '' or passwd == '' : 
     print 'Usage: python gmail.py -i{id} -p{password} FileList' 
     sys.exit() 

   recipient = user+"@gmail.com" 
   subject = time.strftime('%Y year %m month %d day %H hour %M minute %S second sent', time.localtime(time.time())) 
   msg = subject +"." 

   sendGMail(user, passwd, recipient, subject, msg, lt) 
