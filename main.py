# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup as bs
import requests
import selenium
from selenium import webdriver
import time
import smtplib
from email.mime.text import MIMEText
import secret as secret

sin_non_hyun = 'https://booking.naver.com/booking/13/bizes/416181/items/3600073'

calendar_id = 'calendar'
calendar_title = 'calendar-title'
next_month_class = 'calendar-btn-next-mon'
date_class = 'calendar-date'
unselectable_class = 'calendar-unselectable'
clickable_class = 'anchor'
non_clickable_class = 'none'


def mailTo(mail_id, title, content):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(secret.mail_id1, 'xrmhlpxfulfbvhoo')

    msg = MIMEText(content)
    msg['Subject'] = title
    msg['To'] = mail_id
    smtp.sendmail(secret.mail_id1, mail_id, msg.as_string())

    smtp.quit()


def do(url):
    dates = []
    try:
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(executable_path='./chromedriver', options=op)
        driver.get(url=url)
        driver.implicitly_wait(time_to_wait=10)
        calendar = driver.find_element_by_id(calendar_id)

        while True:
            title = driver.find_element_by_class_name(calendar_title)
            month = int(title.text.split('.')[1])
            if month < 7:
                calendar.find_element_by_class_name(next_month_class).click()
                time.sleep(2)
                continue
            if month > 7:
                break

            td_list = calendar.find_elements_by_tag_name('td')
            for td_element in td_list:
                classes = td_element.get_attribute('class').split(' ')
                if unselectable_class in classes:
                    print(f'{td_element.text} is unselectable')
                else:
                    td_element.click()
                    select_dsc = driver.find_element_by_class_name('select_dsc')
                    date = select_dsc.text
                    print(date)

                    time_select = driver.find_element_by_class_name('time_select')

                    time.sleep(1)
                    li_list = time_select.find_elements_by_tag_name('li')
                    print(len(li_list))

                    for li in li_list:
                        a_s = li.find_elements_by_tag_name('a')
                        if len(a_s) != 0:
                            a = a_s[0]
                            a_classes = a.get_attribute('class').split(' ')
                            if 'anchor' in a_classes and 'none' not in a_classes:
                                reservation_time = li.text
                                print(f'{reservation_time} is able to reservation')
                                dates.append(date + ' ' + reservation_time)
                            else:
                                print(f'{li.text} is unable to reservation')

            # next month
            calendar.find_element_by_class_name(next_month_class).click()
            time.sleep(2)

        mailTo(secret.mail_id2, 'balanceButton', '\n'.join(dates))
        mailTo(secret.mail_id1, 'balanceButton', '\n'.join(dates))

    except Exception as e:
        print(e)
    finally:
        driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    do(sin_non_hyun)
