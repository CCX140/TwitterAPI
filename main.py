from selenium import webdriver
import time
import colorama
from os import system
from colorama import Fore, Style
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

colorama.init()

class TwitterAPI(object):

	##########################################
	#										 #
	#				  INIT				 	 #
	#										 #
	##########################################

	def __init__(self,headless):

		system("cls")

		options = Options()
		if headless :
			options.headless = True

		self.driver = webdriver.Firefox(options=options)

		self.driver.get("https://www.google.com/")
		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.NAME, "q"))
		    )
		finally:
			if (element):
				print(Fore.GREEN +"###### API initialized ! ######\n")
			else:
				print("Error : no connection")
				self.quit()

	##########################################
	#										 #
	#				  QUIT				 	 #
	#										 #
	##########################################

	def quit(self):
		print(Fore.GREEN +"\n#####API Quit#####")
		time.sleep(3)
		self.driver.quit()

	##########################################
	#										 #
	#				 CONNECT				 #
	#										 #
	##########################################

	def connect(self, username, password,getid):
		self.driver.get("https://twitter.com/login")
		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.NAME, "session[username_or_email]"))
		    )
		except:
			print("Error : no connection")
			return
		finally:
			if 'element' in locals():
				print(Fore.CYAN +"Connecting to Account",username,"/",password,"...")
			else:
				print("Error : no connection")
				return

		self.driver.find_element_by_name("session[username_or_email]").send_keys(username)
		self.driver.find_element_by_name("session[password]").send_keys(password)
		self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div/span/span').click()

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]'))
		    )
		except:
			print("Error : no connection")
			return
		finally:
			if 'element' in locals():
				print(Fore.GREEN + "Connected !\n")
				if getid :
					time.sleep(1)
					self.my_id = self.get_id(username)
			else:
				print("Error : Not Connected")
				return

		try:
		    close = WebDriverWait(self.driver, 3).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]"))
		    )
		except:	
			print(Fore.MAGENTA+"No cookies button ?\n")
		finally:
			if 'close' in locals():
				close.click()
				print(Fore.MAGENTA+"Cookies button closed\n")

		time.sleep(1)




	##########################################
	#										 #
	#				  TWEET 				 #
	#										 #
	##########################################
	def tweet(self,text):

		if len(text) > 280 :
			print("Error : Too long text")
			return

		if not(self.driver.current_url == "https://twitter.com/home"):
			self.driver.get("https://twitter.com/home")

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div/span'))
		    )
		except:
			print(Fore.RED+"Error : Tweet Failed")
			return
		finally:
			if 'element' in locals():
				tweet = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div/span')
				if tweet:
					tweet.click()
					action = ActionChains(self.driver) 
					action.key_down(Keys.ARROW_UP).send_keys(text).perform()
					
					self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]').click()
					print(Fore.GREEN + "Tweeted : "+"' "+text+" '\n")
					time.sleep(1)
				else :
 					print(Fore.RED +"Error : Tweet failed")
 					return
				
			else:
				print(Fore.RED+"Error : Tweet failed")
				return



	##########################################
	#										 #
	#				  GET_ID 				 #
	#										 #
	##########################################
		
	def get_id(self,name):
		print(Fore.CYAN+"Getting id of "+name+"...")

		if not(self.driver.current_url == "https://twitter.com/"+name):
			self.driver.get("https://twitter.com/"+name)

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "//*[@id="+'"react-root"'+"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/a/div/div[2]/div/img"))
		    )
		except:

			print(Fore.RED+"Error : Cant get id of "+name)
			return

		finally:

			if 'element' in locals():
				src = element.get_attribute("src")
				split = src.split("/")
				print(Fore.GREEN+"Id of "+name+" is "+split[4]+"\n")
				time.sleep(1)
				return split[4]

			else:
				print(Fore.RED+"Error : Cant get id of "+name)
				time.sleep(1)
				return



	##########################################
	#										 #
	#			   MESSAGE TO ID			 #
	#										 #
	##########################################

	def message_to_id(self,id,text):

		if id == None:
			print(Fore.RED+"Error : Cant send message, no id specified")

		self.driver.get("https://twitter.com/messages/")
		time.sleep(2)

		self.driver.get("https://twitter.com/messages/"+id+"-"+self.my_id)

		print(Fore.CYAN+"Sending message to "+id)

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/div/div/div/aside/div[2]/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div"))
		    )
		except:
			print(Fore.RED+"Error : Cant send message to "+id)
			return
		finally:
			if 'element' in locals():
				element.click()
				action = ActionChains(self.driver) 
				action.key_down(Keys.ARROW_UP).send_keys(text+Keys.ENTER).perform()
				print(Fore.GREEN+"Sent "+text+" to "+id)

		


	##########################################
	#										 #
	#			   GET FOLLOWERS			 #
	#										 #
	##########################################

	def get_followers_from_name(self,name,max):
		self.driver.get("https://twitter.com/"+name+"/followers")
		print(Fore.CYAN+"Getting followers of "+name+"...")

		tab = []
		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[1]"))
		    )
		except:
			print(Fore.RED+"Error : Cant get followers of "+name+"\n")
			return tab

		initialscrollY = 0
		sizetoscroll = 0
		first_follower = None

		while 1:
			try:
				time.sleep(2)
				followers = self.driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div")
			except:
				print(Fore.CYAN+"There is no followers")
				return tab

			if 'followers' in locals():

				#check if we are at the bottom of the followers page
				if followers[0] == first_follower:
					print(Fore.CYAN+"There is no more followers") 
					return tab
				else:
					first_follower = followers[0]

				for i in range(1,len(followers)) :
					
					id_name = []
					id = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div["+str(i)+"]/div/div/div/div[2]/div[1]/div[2]/div").get_attribute("data-testid").split("-")[0]
					name = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div["+str(i)+"]/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div[1]/span").text
					id_name.append(id)
					id_name.append(name)

					if not(id_name in tab):
						tab.append(id_name)

					if len(tab) == 40:
						return tab 

					#print(id_name)
					#print(followers[i].size['height'])
					sizetoscroll = sizetoscroll + int(followers[i].size['height'])

				self.driver.execute_script("window.scrollBy(0,"+str(sizetoscroll)+");")


api = TwitterAPI(headless=False)
api.connect(username="Devccx",password="romain619",getid=True)
#res = api.get_followers_from_name(name="ccx280",max=100)
#for r in res:
#	print(r)
#time.sleep(20)
#api.tweet("@q8_5t test 1 2 test eske tu mrecois  ???? allloo")
id = api.get_id("je_suis_Quidam")
api.message_to_id(id=id,text="test")
#api.quit()
