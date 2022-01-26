from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == '__main__':
    listpath = 'list.txt'
    cookiepath ='cookie.txt'
    url = "https://eksisozluk.com/"
    driver = webdriver.Chrome()
    driver.get(url)
    lines = [line.rstrip('\n') for line in open(cookiepath)]
    rangeindex = int(len(lines))
    try:
        for line in range(1, rangeindex):
            driver.add_cookie(
            {"name": lines[line].split("\t")[5], "value": lines[line].split("\t")[6]})  # get cookie name and value
    except Exception as exp:
        print("Cookie yüklenirken hata oluştu!")
        print(exp.status_code, flush=True)
        print(exp.message, flush=True)
    count = 0
    erroruser = 0
    blocked = 0
    befblocked = 0
    while True:
        with open(listpath) as us:
         listread = us.read().splitlines()
         rangelist = int(len(listread))
         print("Taranacak toplam kullanıcı sayısı: "+str(rangelist) + "\n")
        try: #read list and block all users
            for line in range(rangelist):
                user = listread[count]
                driver.get("https://eksisozluk.com/biri/" + user) #get user_page
                #user check
                if " " in driver.find_element(By.CLASS_NAME,"field-validation-error").text:
                    print("Böyle bir kullanıcı mevcut değil: " + user)
                    erroruser += 1
                #block user
                elif driver.find_element(By.CLASS_NAME,"profile-relation-button").text == "takip et":
                    driver.find_element(By.XPATH, "//*[name()='use' and @*='#eksico-profile-more']").click() #click profile more
                    driver.find_element(By.LINK_TEXT,"engelle").click()
                    print("Engellenen Kullanıcı: " + user)
                    blocked += 1
                    time.sleep(3)
                #check blocked
                elif driver.find_element(By.CLASS_NAME, "profile-relation-button").text == "engellenmiş":
                    print("Daha önce engellenmiş kullanıcı: " + user)
                    befblocked += 1
                else:
                    count += 1
                count += 1
        except Exception as exp:
          print("Problem oluştu!")
          print(exp.status_code, flush=True)
          print(exp.message, flush=True)
        print("\n***RAPOR***\nEngellenen toplam kullanıcı sayısı: " + str(blocked))
        print("Daha önce engelli olan kullanıcı sayısı: " + str(befblocked))
        print("Hatalı kullanıcı sayısı: " + str(erroruser))
        break
