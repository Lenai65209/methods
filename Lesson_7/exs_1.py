from time import sleep
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

mail_lst = []

my_serviсe = Service('chromedriver.exe')
driver = webdriver.Chrome(service=my_serviсe)
driver.get('https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fmail.yandex.ru')
my_element = driver.find_element(By.ID, 'passp-field-login')
my_element.send_keys('lenai65209@yandex.ru')
my_element.send_keys(Keys.ENTER)
sleep(3)
my_element = driver.find_element(By.ID, 'passp-field-passwd')
my_element.send_keys('Nikita01092004')
my_element.send_keys(Keys.ENTER)
sleep(5)
letters = driver.find_elements(By.XPATH, "//div[@class='ns-view-container-desc mail-MessagesList js-messages-list']/div/div")
# ns-view-container-desc mail-MessagesList js-messages-list
print('len(letters)', len(letters))
for letter in letters:
    sleep(3)
    letter_url = letter.find_element(By.XPATH, './/div/div/a')
    # print('url', url)
    letter_link = letter_url.get_attribute('href')
    # div/div/a/div/span/span/span[@class='mail-MessageSnippet-FromText']
    # print('letter_link', letter_link)
    sleep(3)
    sender = (letter.find_element(By.XPATH, "div/div/a/div/span/span/span[@class='mail-MessageSnippet-FromText']")).text
    # print('sender', sender)
    sleep(3)
    letter_topic_for_lst = (letter.find_element(By.XPATH, './/div')).text
    letter_topic = " ".join(letter_topic_for_lst.split())
    # print('letter_topic', letter_topic)
    # /div/div/a/div/span/div/span[@class='mail-MessageSnippet-Item_dateText']
    sleep(3)
    letter_time = (letter.find_element(By.XPATH, ".//div/div/a/div/span/div/span[@class='mail-MessageSnippet-Item_dateText']")).text
    # print('letter_time', letter_time)
    mail_tuple = (sender, letter_time, letter_topic, letter_link)
    # print(mail_tuple)
    mail_lst.append(mail_tuple)

conn = sqlite3.connect('database.db')
cur = conn.cursor()
# cur.execute("SQL-ЗАПРОС-ЗДЕСЬ;")
cur.execute("""CREATE TABLE IF NOT EXISTS letters(
   sender TEXT,
   letter_time TEXT,
   letter_topic TEXT,
   letter_link TEXT);
""")
conn.commit()

# print(mail_lst)
for letter in mail_lst:
    cur.execute(f"INSERT INTO letters VALUES{letter}")
conn.commit()

cur.execute("SELECT * FROM letters;")
all_results = cur.fetchall()
for letter in all_results:
    print('______________________________ из базы ___________________________________')
    print(letter, end='\n')
print()
