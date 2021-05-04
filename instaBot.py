from userInfo import username, password, theirUsername
#don't show userInfo content to others
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request

class Instagram:
    def __init__(self, username,password, theirUsername):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(20)
        #self.browser.maximize_window()
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        #self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.username = username
        self.password = password
        self.theirUsername = theirUsername

    def singIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(5)
        usernameInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        passwordlInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")

        usernameInput.send_keys(self.username)
        passwordlInput.send_keys(self.password)
        passwordlInput.send_keys(Keys.ENTER)
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()
        time.sleep(2)

    def getFollowers(self, listType):
        self.browser.get(f"https://www.instagram.com/{self.theirUsername}")
        time.sleep(2)
        #Followers
        if(listType==1):
            self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        #Following
        else:
            self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        time.sleep(2)

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followersCount = len(dialog.find_elements_by_css_selector("li"))
        print(f'first count:{followersCount}')

        action = webdriver.ActionChains(self.browser)

        while True:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(3)

            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followersCount != newCount: 
                followersCount = newCount
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                print(f'Count Update: {newCount}')
                time.sleep(2)
            else:
                break

            
        followers = dialog.find_elements_by_css_selector("li")

        followerList = []
        for user in followers:
            #if(listType==1):
            #    linkName = user.find_element_by_class_name("wFPL8").text
            #else:
             #   linkName = user.find_elements_by_css_selector("._7UhW9.xLCgt.MMzan._0PwGv.fDxYl")
                #linkName = ""
            #print(linkName)
            link = user.find_element_by_css_selector("a").get_attribute("href")
            #print(link)
            followerList.append(link)

        if(listType==1):
            textFile = theirUsername+"Followers.txt"
        else:
            textFile = theirUsername+"Following.txt"
        with open(textFile, "w", encoding="UTF-8") as file:
            for item in followerList:
                file.write(str(item) + "\n")

    
    #FOLLOW
    def followUser(self, username):
        self.browser.get(username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("//button[@type = 'button']")
        if followButton.text != "Following":
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")

    #UNFOLLOW
    def unFollowUser(self, username):
        self.browser.get("https://www.instagram.com/"+ username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")
        if followButton.text == "Following":
            followButton.click()
            time.sleep(2)
            self.browser.find_element_by_xpath('//button[text()="Unfollow"]').click()
        else:
            print("You are not following this user")

    #DOWNLOAD IMAGE
    def download_image(self, src, image_filename, folder):
        """
        Creates a folder named after a user to to store the image, then downloads the image to the folder.
        """

        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))
    #DOWNLOAD USER IMAGES
    def download_user_images(self, theirUsername):
        """
        Downloads all images from a users profile.
        """
    
        self.browser.get(f"https://www.instagram.com/{self.theirUsername}")

        img_srcs = []
        finished = False
        while not finished:

            finished = self.infinite_scroll() # scroll down

            img_srcs.extend([img.get_attribute('src') for img in self.browser.find_elements_by_class_name('FFVAD')]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates

        for idx, src in enumerate(img_srcs):
            self.download_image(src, idx, theirUsername)
    #SCROLL FUNC
    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media
        Returns:
            bool: True if the bottom of the page has been reached, else false
        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.browser.execute_script("return document.body.scrollHeight")

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.browser.execute_script("return document.body.scrollHeight")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False




ig = Instagram(username,password,theirUsername)
ig.singIn()
# 1 for followers list else for following list
ig.getFollowers(2)
#ig.download_user_images(theirUsername)
#ig.followUser('')
#ig.unFollowUser('')

'''
userFollowers = []
with open("someOneFollowers.txt", "r",encoding="utf-8") as file:
    for item in file:
        userFollowers.append(item)
'''

#userFollowers = ["","","",""]
# for user in userFollowers:
#     print(user)

# for user in userFollowers:
#     ig.followUser(user)
#     time.sleep(2)
