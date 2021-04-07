from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as ur
import os
import random

# é importante que seja passada a url de um grupo do facebook
email = ''
password = ''
url = 'https://www.facebook.com/groups/243159702401891/local_members/'
waiting_time = 2
profiles = []
images = []
count = 0

# opção necessaria caso queira desabilitar a janela do navegador, deve ser passada como parametro na função webdriver.chrome()
# option = Options()
# option.headless = True

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

def savePhoto(name, image):
    global count
    """creates a folder with the profile name and saves the received image in that folder
    
    Arguments:
        name string -- name of profile
        image string -- image url
    """
    try:
        time.sleep(random.random())
        resource = ur.urlopen(image['data-starred-src'])
        print("criando diretorio profiles/"+name)
        os.mkdir("profiles/"+name)
        print("fazendo o download da imagem e salvando em profiles/"+name+"/"+str(count)+".jpg")
        output = open("profiles/"+name+"/"+str(count)+".jpg","wb")
        output.write(resource.read())
        output.close()
        count += 1
    except Exception as exception:
        print("diretorio profiles/"+name+" ja existente")
        print(exception)
        savePhoto(name, image)
    
def obtainNameOfProfile(profile):
    """return the name of profile
    
    Arguments:
        profile string -- profile url
    
    Returns:
        string -- name of profile
    """
    # name = str(profile['href']).split("?")[0]
    # name = str(name).split(".com/")[1].replace(".","-")
    # name = str(name)
    # return name
    element = driver.find_element_by_xpath("//h1[@class='_2nlv']//span[@class='_2t_q']")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("a", {"class": "_2nlw _2nlv"})

def getPhotoList():
    """returns a array of urls
    
    Returns:
        array -- array containing a list of urls
    """
    element = driver.find_element_by_xpath("//div//ul[@class='fbStarGrid _69n fbPhotosRedesignBorderOverlay fbStarGridAppendedTo']")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("li", {"class": "fbPhotoStarGridElement fbPhotoStarGridNonStarred focus_target _53s fbPhotoCurationControlWrapper"})

def obtainAtualCity():
    element = driver.find_element_by_xpath("//li[@id='current_city']//div//div//div//span[@class='_2iel _50f7']")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('a')

def obtainNatalCity():
    element = driver.find_element_by_xpath("//li[@id='hometown']//div//div//div//span[@class='_2iel _50f7']")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('a')


def obtainBirth():
    element = driver.find_element_by_xpath("//li[@class='_3pw9 _2pi4 _2ge8 _4vs2']//div//div[@class='_4bl7 _pt5']//div//div")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("span", {"class": "_2iem"})
def obtainGender():
    element = driver.find_element_by_xpath("//li[@class='_3pw9 _2pi4 _2ge8 _3ms8']//div//div[@class='_4bl7 _pt5']//div//div")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("span", {"class": "_2iem"})

def clickAbout():
    driver.find_element_by_xpath("//div//ul//li//a[@class='_6-6']").click()
    
def clickPlacesWhereLived():
    """performs a click on the places where lived button
    """
    driver.find_element_by_xpath("//div//div//a[@class='_5pwr _84vg']//span[@class='_5pws _50f8  _5kx5 _2iem']").click()

def clickContact():
    driver.find_element_by_xpath("//div//div//div//a[@class='_5pwr _84vf']").click()
         
def choosePhotosOfThePerson():
    """performs a click on the photos button containing the profile owner
    """
    driver.find_element_by_xpath("//div//a[@class='_3c_']//span[@class='_3sz']").click()
    
def clickPhotos():
    """performs a click on the photo butthon
    """
    driver.find_element_by_xpath("//ul[@class='_6_7 clearfix']//li//a[@class='_6-6'][@data-tab-key='photos']").click()
    
def saveInfos(path, name, gender, atualcity, natalcity, byrth):
    archive = open(path+"info.txt", "a")
    archive.write("\r\nNome: "+name+" \r\nGenero :"+gender+"\r\ncidade atual: "+atualcity+"\r\ncidade natal :"+natalcity+"\r\nData de nascimento:"+byrth)
    archive.close()    
    
def acessProfile(profile_url):
    """acess the profile
    
    Arguments:
        profile_url string -- profile url
    """
    try:
        driver.get(profile_url)
    except Exception as exception:
        print(exception)
    
def getProfileList():
    """returns a array of profiles urls
    
    Returns:
        array-- array os profiles
    """
    element = driver.find_element_by_xpath("//div//div[@class='fbProfileBrowserList fbProfileBrowserListContainer']")
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("a", {"class": "_60rg _8o _8r lfloat _ohe"})
    
def scrollPage(num_scrolls):
    """performs a scroll on the page
    
    Arguments:
        num_scrolls int -- number of scrolls
    """
    for i in range(0,num_scrolls):
        time.sleep(waiting_time)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
def loginOnFacebook(email, password):
    """performs a login in facebook
    """
    try:
        driver.get(url)
        driver.find_element_by_xpath("//div//input[@class='inputtext _55r1 inputtext _1kbt inputtext _1kbt'][@name='email']").send_keys(email)
        driver.find_element_by_xpath("//div//input[@class='inputtext _55r1 inputtext _1kbt inputtext _1kbt'][@name='pass']").send_keys(password)
        driver.find_element_by_xpath("//div//button[@class='_42ft _4jy0 _52e0 _4jy6 _4jy1 selected _51sy'][@name='login']").click()
        time.sleep(waiting_time)
    except Exception as exception:
        print(exception)

def main():
    loginOnFacebook(email, password)
    scrollPage(1)
    profiles = getProfileList()
    print("encontrados "+ str(len(profiles))+ " perfis")
    for profile in profiles:
        gender = ''
        byrth = ''
        natalcity = ''
        atualcity = ''
        acessProfile(profile['href'])
        time.sleep(waiting_time)
        clickAbout()
        time.sleep(waiting_time)
        clickPlacesWhereLived()
        time.sleep(waiting_time)
        listatualcity = obtainAtualCity()
        listnatalcity = obtainNatalCity()
        for c in listatualcity:
            atualcity = str(c.text)
        for c in listnatalcity:
            natalcity = str(c.text) 
        time.sleep(waiting_time)
        clickContact()
        time.sleep(waiting_time)
        listgender = obtainGender()
        listbyrth = obtainBirth()
        for g in listgender:
            gender = str(g.text)
        for b in listbyrth:
            byrth = str(b.text)
        clickPhotos()
        time.sleep(waiting_time)
        choosePhotosOfThePerson()
        time.sleep(waiting_time)
        scrollPage(3)
        images = getPhotoList()
        listnames = obtainNameOfProfile(profile)
        for n in listnames:
            name = str(n.text)
        count = 0
        print("encontradas "+ str(len(images))+ " imagens no perfil")
        for image in images:
            savePhoto(name, image)
        saveInfos("profiles/"+name+"/",name, gender, atualcity, natalcity, byrth)
        
if __name__ == "__main__":
    main()
    
