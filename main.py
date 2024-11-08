from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
import undetected_chromedriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait


def login(username, password):
    global browser
    global notification_modal_window_path
    global notification_modal_window
    global close_modal_button_path
    global close_modal_window_button
    global followers_list_path
    global follower_container_path
    global all_usernames_refs
    global file_name
    global username_nickname
    global target_user_page
    global create_new_dm_button_path
    global create_new_dm_button
    global dm_section
    global message_button
    global message_input
    global target_dm_username_input
    try:
        browser = webdriver.Chrome()
        browser.get('https://instagram.com')
        time.sleep(2)
        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys(username)
        time.sleep(1)
        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1000)
    except Exception as ex:
        print(ex)
        browser.close()
    try:
        time.sleep(3)
        save_info_window_path='/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div'
        save_info_window=browser.find_element(By.XPATH, save_info_window_path)
        save_info_window.click()
        time.sleep(random.randrange(3, 5))
        notification_modal_window_path = '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div'
        browser.find_element(By.XPATH, notification_modal_window_path)
    except NoSuchElementException:
        print("notification_modal_window not found")
        browser.close()
    try:
        close_modal_window_button_path = '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
        close_modal_window_button = browser.find_element(
            By.XPATH, close_modal_window_button_path)
    except NoSuchElementException:
        print("close_modal_window_button element not found")
    else:
        close_modal_window_button.click()
        time.sleep(random.randrange(3, 5))
def get_all_users(user):
    user_url = f"https://www.instagram.com/{user}"
    global file_name
    file_name = user_url.split('/')[-1]
    try:
        browser.get(user_url)
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(f"{file_name}")
            os.path.join(f"{file_name}", f"{file_name}.txt")
    except ValueError():
        print("User not found.")
    else:
        browser.refresh()
        time.sleep(5)
        followers_button_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a'
    try:
        followers_button = browser.find_element(
            By.XPATH, followers_button_path)
    except NoSuchElementException:
        print("followers_button element not found")
        browser.close()
    else:
        followers_button = browser.find_element(
            By.XPATH, followers_button_path)
        time.sleep(5)
        followers_count = browser.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span')
        followers_count_text = followers_count.text
        followers_count_text = followers_count_text.replace('\xa0', ' ')
        followers_count_text = followers_count_text.replace(" ", "")
        print(followers_count_text)
        if 'тис' in followers_count_text:
            numeric_part = followers_count_text.replace('тис.', '').strip()
            numeric_part = numeric_part.replace(',', '.')
            numeric_part = float(numeric_part) * 100
        elif 'млн' in followers_count_text:
            numeric_part = followers_count_text.replace('млн', '').strip()
            numeric_part = numeric_part.replace(',', '.')
            numeric_part = float(numeric_part) * 100
        else:
            numeric_part = float(followers_count_text)
            print(numeric_part)
        try:
            iteration_count = int(numeric_part / 12)
            followers_button.click()
            time.sleep(3)
        except ValueError():
            print("Invalid value format")
        try:
            followers_list_path = '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div'
            followers_list = browser.find_element(
                By.XPATH, followers_list_path)
            time.sleep(3)
        except NoSuchElementException:
            print("followers_list not found")
            browser.close()
        try:
            followers_list_path = '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div'
            followers_list = browser.find_element(
                By.XPATH, followers_list_path)
        except NoSuchElementException:
            print("followers_list element not found")
            browser.close()
        else:
            followers_list = browser.find_element(
                By.XPATH, followers_list_path)
            scroll_origin = ScrollOrigin.from_element(followers_list)
            followers_nicknames = []
            for i in range(1, 12):
                ActionChains(browser).scroll_from_origin(
                    scroll_origin, 0, i * 100).perform()
                follower_path = f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{
                    i}]/div"
                follower = browser.find_element(By.XPATH, follower_path)
                username = follower.find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                print(username)
                followers_nicknames.append(username)
                time.sleep(1)
                print(file_name)
            with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                for nickname in followers_nicknames:
                    text_file.write(nickname + "\n")
                    print(nickname)


def paste_input(message):
        dm_section_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div'
        dm_section = browser.find_element(By.XPATH, dm_section_path)
        print(dm_section.text)
        print('open direct')
        time.sleep(3)
        message_input_path = '#mount_0_0_14 > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div > div.xjp7ctv > div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k > div > div > div > div > div > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div:nth-child(3) > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1i64zmx.xw3qccf.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.xzsf02u.x1a2a7pz.x1n2onr6.x14wi4xw.x1iyjqo2.x1gh3ibb.xisnujt.xeuugli.x1odjw0f.notranslate'
        message_input = browser.find_element(By.CSS_SELECTOR, message_input_path)
        print(message_input.get_attribute('aria-placeholder'))
        print('found input')
        message_input.send_keys(message)
        time.sleep(2)
        send_button_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]'
        send_button = dm_section.find_element(By.XPATH, send_button_path)
        send_button.click()
        time.sleep(3)


def create_new_message(username):
    time.sleep(2)
    try:
        create_new_dm_button_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div'
        create_new_dm_button = browser.find_element(
            By.XPATH, create_new_dm_button_path)
    except NoSuchElementException:
        print("create_new_dm_button not found")
        browser.close()
    else:
        create_new_dm_button.click()
        time.sleep(5)
    try:
        target_user_input = browser.find_element(By.NAME, "queryBox")
    except NoSuchElementException:
        print("target_user_input not found")
        browser.close()
    else:
        target_user_input.send_keys(username)
        time.sleep(5)


def click_dm():
    try:
        direct_message_button_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[5]/div/div/span/div/a/div/div/div/div[1]'
        direct_message_button = browser.find_element(
            By.XPATH, direct_message_button_path)
    except NoSuchElementException:
        print("direct_message_button not found")
        browser.close()
    else:
        direct_message_button.click()
        time.sleep(random.randrange(5, 7))
    try:
        direct_message_button_path = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[5]/div/div/span/div/a/div/div/div/div[1]'
        direct_message_button = browser.find_element(
            By.XPATH, direct_message_button_path)
    except NoSuchElementException:
        print("direct_message_button not found")
        browser.close()
    else:
        direct_message_button.click()
        time.sleep(random.randrange(5, 7))


def send_messages(message):
    global create_new_dm_box
    homepage = browser.get('https://instagram.com')
    time.sleep(5)
    click_dm()
    global file_name
    with open(f"{file_name}/{file_name}.txt") as f:
        if os.path.exists(f"{file_name}/{file_name}") and os.path.getsize(f"{file_name}/{file_name}") == 0:
            print(f"The file is empty.")
            browser.close()
        else:
            for url in f:
                url = url.strip()
                username = url.split('/')[-2]
                create_new_message(username)
                global target_users_list
                global target_users_boxes
                global target_users_usernames
                global usernames_array_length
                global containers
                time.sleep(10)
                target_users_list_class = 'body > div.x17hbii1.x1kd72b6.x13ywhbb.xahrfoy.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div.x9f619.x1ja2u2z.x1k90msu.x6o7n8i.x1qfuztq.x17qophe.x10l6tqk.x13vifvy.x1hc1fzr.x71s49j.xh8yej3 > div > div.xjp7ctv > div > div'
                target_users_list = browser.find_element(
                    By.CSS_SELECTOR, target_users_list_class)
                wait = WebDriverWait(browser, timeout=10)
                wait.until(lambda d: target_users_list.is_displayed())
                target_users_boxes = str(target_users_list.text).splitlines()
                target_users_usernames = [target_users_boxes[i] for i in range(len(target_users_boxes)) if i % 2 != 0]
                usernames_array_length=len(target_users_usernames)
                print(target_users_boxes)
                print(target_users_usernames)
                print("Element found.")
                for i in range(1, usernames_array_length + 1):
                    print(usernames_array_length)
                    user_container_path=f"/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[{i}]"
                    user_container=browser.find_element(By.XPATH, user_container_path)
                    time.sleep(2)
                    user_container_text=user_container.text
                    print(str(user_container_text))
                    print('text')
                    target_user=str(user_container_text).splitlines()
                    target_user=[target_user[i] for i in range(len(target_user)) if i % 2 != 0]
                    print(f"target user is {target_user[0]}")
                    if target_user[0] in target_users_usernames:
                            user_container.click()
                            print('clicked')
                            time.sleep(2)
                            print('chat button')
                            chat_button_path = 'body > div.x17hbii1.x1kd72b6.x13ywhbb.xahrfoy.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div.x9f619.x1ja2u2z.x1k90msu.x6o7n8i.x1qfuztq.x17qophe.x10l6tqk.x13vifvy.x1hc1fzr.x71s49j.xh8yej3 > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xw7yly9.xktsk01.x1yztbdb.x1d52u69.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div'
                            chat_button = browser.find_element(
                            By.CSS_SELECTOR, chat_button_path)
                            print(chat_button)
                            chat_button.click()
                            time.sleep(3)
                            paste_input(message)     
                         
