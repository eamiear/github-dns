
import requests
from bs4 import BeautifulSoup
import re 
import shutil
import os 
import datetime

sites =[ 
	"github.com",
	"github.global.ssl.fastly.net",
	"assets-cdn.github.com",
	"documentcloud.github.com",
	"gist.github.com",
	"help.github.com",
	"nodeload.github.com",
	"raw.github.com",
	"status.github.com",
	"training.github.com",
	"ithubusercontent.com",
	"avatars1.githubusercontent.com",
	"codeload.github.com",
	"github-production-release-asset-2e65be.s3.amazonaws.com"
	]
	
addr2ip = {}

def getIp(siteAdd):
	
	engine = "https://ipaddress.com/search/"
	headers = headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36','Host':'movie.douban.com'
}	

	url = "http://ip.tool.chinaz.com/"+siteAdd
	try:
		res = requests.get(url)
		soup=BeautifulSoup(res.text,'html.parser')
		result=soup.find_all('span', class_="Whwtdhalf w15-0")
		trueip = None
		for c in result:
			ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
			if len(ip)!= 0:
				trueip = ip[0] 
	except:
		print(" search error: "+siteAdd+"")
		return None
	
	return trueip	
	

# generate data table
def generateDict():

	for site in sites:
		ip = getIp(site)
		if ip != None:
			addr2ip[site] = ip
			print(site+"\t"+ip)
		

def chachong(line):
	flag = False
	for site in sites:
		if site in line:
			flag = flag or True
		else:
			flag = flag or False
	return flag 
	

# update host and flush local DNS

def updateHost():
	generateDict()
	today = datetime.date.today()
	hostLocation = "C:\Windows\System32\drivers\etc\hosts"
	shutil.copy("C:\Windows\System32\drivers\etc\hosts", "C:\Windows\System32\drivers\etc\hosts.bak") # backup host
	f1 = open("C:\Windows\System32\drivers\etc\hosts", "r")
	lines = f1.readlines()
	f2 = open("temphost", "w")
	
	for line in lines:                     
		if chachong(line) == False:
			f2.write(line)
	f2.write("\n\n #*********************github "+str(today) +" updated********************\n")
	for key in addr2ip:
		f2.write(addr2ip[key]+"\t"+key+"\n")
	f1.close()
	f2.close()
	
	shutil.copy("./temphost", "C:\Windows\System32\drivers\etc\hosts") #override host
	os.system("ipconfig /flushdns")
	
updateHost()	