#!/usr/bin/python
import time

dummy=open('/etc/netcarinit/netcarBOOT')
no = dummy.readline()
dummy.close()
no = int(no)
no = no+1
Date = time.localtime()

dummy=open('/etc/netcarinit/netcarBOOT','w')
dummy.flush()
dummy.write('%d\n'%no)
dummy.write('%d-%d-%d %d:%d:%d\n'%(Date[0],Date[1],Date[2],Date[3],Date[4],Date[5]))
dummy.close()

