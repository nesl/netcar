import os
import smtplib

fro = 'netcar.diag@gmail.com'
to = 'yhun.kim@gmail.com'
data = open('/home/SlogModule.log')
data = data.read()

try:
	smtp=smtplib.SMTP('cwmx.com')
	smtp.sendmail(fro,to,data)
        os.popen('rm /home/SlogModule.log')
	smtp.close()
except:
	print "try next time"

