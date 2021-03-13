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

EN = "England"
FR = "France"
US = "United States"
IN = "India"
KR = "Korea"
JP = "Japan"
RS = "Russia"
SP = "Spain"
IT = "Italy"

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
					self.my_id = self.get_id_from_banner(username)
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
		
	def get_id_from_banner(self,name):
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


	def get_id(self,name):

		self.driver.get("https://twitter.com/home")
		time.sleep(1)

		print(Fore.CYAN+"Getting id of "+name+"...")

		if not(self.driver.current_url == "https://twitter.com/"+name):
			self.driver.get("https://twitter.com/"+name)
			time.sleep(1)

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div"))

		    )
		except:
			print(Fore.RED+"Error : Cant get id of "+name)
			return

		finally:

			elements = self.driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div")
			element = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div["+str(len(elements))+"]/div/div")

			if 'element' in locals():
				time.sleep(1)
				src = element.get_attribute("data-testid")
				split = src.split("-")
				print(Fore.GREEN+"Id of "+name+" is "+split[0]+"\n")
				return split[0]

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
			return

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
				time.sleep(3)
				followers = self.driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div")															
			except:
				print(Fore.CYAN+"There is no followers\n")
				return tab

			if 'followers' in locals():

				#check if we are at the bottom of the followers page
				if followers[0] == first_follower:
					print(Fore.CYAN+"There is no more followers") 
					print(Fore.GREEN+"Done !\n")
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

					if len(tab) == max:
						print(Fore.GREEN+"Done !\n")
						return tab 

					#print(id_name)
					#print(followers[i].size['height'])
					sizetoscroll = sizetoscroll + int(followers[i].size['height'])

				self.driver.execute_script("window.scrollBy(0,"+str(sizetoscroll)+");")



	##########################################
	#										 #
	#			   GET TRENDS			 	 #
	#										 #
	##########################################

	def get_trends(self,location):
		print(Fore.CYAN+"Getting Trends from..."+location)

		self.driver.get("https://twitter.com/settings/explore/location")

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/input"))
		    )
		except:
			print(Fore.RED+"Error : Cant select location\n")
			return
		finally:

			element.send_keys(location)
			time.sleep(3)

			try:
			    element = WebDriverWait(self.driver, 5).until(
			        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div"))
			    )
			except:
				print(Fore.RED+"Error : Wrong location\n")
				return

			finally:
				element.click()
				time.sleep(1)


		self.driver.get("https://twitter.com/i/trends")

		try:
		    element = WebDriverWait(self.driver, 5).until(
		        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[2]/div/div"))
		    )
		except:
			print(Fore.RED+"Error : Cant get trends\n")
			return
		finally:
			tab = []
			time.sleep(1)
			elements = self.driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div")
			for i in range(2,len(elements)):
				text = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div["+str(i)+"]/div/div/div/div[2]/span").text																  												  
				print(text)
				tab.append(text)

			return(tab)



	##########################################
	#										 #
	#			   TWEET TRENDS			 	 #
	#										 #
	##########################################

	def tweet_trends(self,location,text):

		trends = self.get_trends(location)

		for i in range(0,len(trends)-1):
			api.tweet(text=(text+trends[i]+" "))
			time.sleep(10)

	def tweet_with_all_trends(self,location,text):
		trends = self.get_trends(location)

		t = text
		for i in range(0,len(trends)-1):
			t = t+" "+trends[i]

		t = t+" "
		api.tweet(text=t)


api = TwitterAPI(headless=False)
api.connect(username="Devccx",password="romain619",getid=True)

#res = api.get_followers_from_name(name="elonmusk",max=1000)
#for r in res:
#	print(r)
#print(len(res))


#api.tweet("@q8_5t test 1 2 test eske tu mrecois  ???? allloo")

#id = api.get_id("elonmusk")
#api.message_to_id(id=id,text="test")

#api.get_trends(location=US)

api.tweet_with_all_trends(location=FR,text="Je vends des bots Twitter ! Si vous êtes interessés -> DM ")

api.quit()
