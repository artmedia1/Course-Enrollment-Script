from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import *
import pytz
import datetime


chrome_driver_path = Service("C:\\WebDriver\\bin\\chromedriver.exe")

# Chrome options to avoid the browser closing automatically
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Create a Chrome WebDriver instance
driver=webdriver.Chrome(service=chrome_driver_path,options=options)
wait = WebDriverWait(driver, 600)

def login():
    tkWindow = Tk()  
    tkWindow.geometry('300x200')  
    tkWindow.title('REM Script')
    tkWindow.eval('tk::PlaceWindow . center')

    Label(tkWindow, text="Please enter details below").pack()
    Label(tkWindow, text="").pack()

    #username label and text entry box
    usernameLabel = Label(tkWindow, text="Username")
    usernameLabel.pack()
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username)
    usernameEntry.pack()

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password")
    passwordLabel.pack()
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*')
    passwordEntry.pack()

    def close_tkWindow():
        tkWindow.destroy()

    #login button
    loginButton = Button(tkWindow, text="Login", command=close_tkWindow)
    loginButton.pack()

    tkWindow.mainloop()
    username = username.get()
    password = password.get()

    return username, password

def loginREM(username, password):
    # Replace 'your_website_url' with the URL of the website you want to open
    website_url = 'https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem' 
    # Open the website
    driver.get(website_url)
    element=driver.find_element(By.ID,"mli")        
    element.send_keys(username)
    element=driver.find_element(By.ID,"password")
    element.send_keys(password)
    element=driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div[1]/form/div[2]/div[2]/p[2]/input")
    element.click()  

def academicSessionSelection():
    #REM ACADEMIC SESSION PAGE
    dropdown_element = wait.until(EC.visibility_of_element_located((By.NAME, "5.5.1.27.1.11.0")))
    # Click the dropdown to open it
    dropdown_element.click()

    dropdown_value = Select(dropdown_element)
    dropdown_value.select_by_index(4)

    continue_Button = wait.until(EC.visibility_of_element_located((By.NAME, '5.5.1.27.1.13')))
    continue_Button.click()


def addCourse(catNum):
    add_course_Selection = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.27.1.23')))
    add_course_Selection.click()

    course_CAT_Input = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.27.7.7')))
    course_CAT_Input.send_keys(catNum)

    add_course_Button = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.27.7.9')))
    add_course_Button.click()

    confirm_Button = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.27.11.11')))
    confirm_Button.click()

    continue_button = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.27.27.11')))
    continue_button.click()

def logout():
    logout_button = wait.until(EC.visibility_of_element_located((By.NAME, '5.1.3.1.1')))
    logout_button.click()

def getTime():
    est = pytz.timezone('US/Eastern')

    # Get the current time in EST
    current_time_est = datetime.datetime.now(est)

    # Format the time as "HH:MM AM/PM"
    formatted_time = current_time_est.strftime('%I:%M %p')

    return formatted_time



def main():
    username, password = login()
    while True: 
        loginREM(username, password)
        academicSessionSelection()
        addCourse("N89Y02")
        print("Attempted to enroll in N89Y02 at " + getTime() + "EST")
        addCourse("N89Y03")
        print("Attempted to enroll in N89Y03 at " + getTime() + "EST")
        logout()
        time.sleep(10800)  

if __name__ == '__main__':
    main()

