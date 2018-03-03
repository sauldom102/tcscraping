import requests
from bs4 import BeautifulSoup
from math import ceil
import re

def clean_text(text):
    return text.strip().replace('\t', '').replace('\r\n', '')

# This function is to get some words that people write with '@' and an email protection encrypts
def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

class ThisCrush:

    def __init__(self,username):
        self.username = username

        self.posts = list()

        self.crushes_num = 0
        self.anon_num = 0

        self.priv_crush = 0
        self.likes = 0

    def get_page(self, num_page):
        page = requests.get('http://www.thiscrush.com/~{}/{}'.format(self.username,num_page+1)).content

        soup = BeautifulSoup(page, 'lxml')

        boxes = soup.find('div',{'id':'content'}).find_all('div',{'class':'post'})

        if len(boxes) > 1:
            for box in boxes:

                data = {
                    'to_user': self.username,
                }

                try:

                    # Obtaining message content, message author and message date
                    msg_tag = box.find('p',{'class':'txt-user-crush'})
                    fake_email = msg_tag.find_all('a', {'class': '__cf_email__'})
                    msg_pattern = r'.*(\[email_protected\]).*'

                    msg_content = clean_text(msg_tag.text).encode('utf-8')
                    msg_author = clean_text(box.find('div', {'class':'col-xs-8 col-sm-8'}).find('p', {'class':'no-margin'}).text).encode('utf-8')
                    msg_date = clean_text(box.find('div', {'class':'col-xs-8 col-sm-8'}).find('p', {'class':'posted-date-time txt-grey'}).text)

                    print('Fake email: {}'.format(len(fake_email)))
                    print(re.match(msg_pattern, msg_content).groups())

                    if msg_content == b'I like you!' and msg_author.startswith(b'Quick Like -'):
                        data['type'] = 'Like'
                        data['author'] = msg_author[12:]
                        self.likes += 1
                    elif msg_author == b'Anonymous':
                        data['type'] = 'Anonymous'
                        data['content'] = msg_content
                        self.anon_num += 1
                    else:
                        data['type'] = 'Public'
                        data['author'] = msg_author
                        data['content'] = msg_content

                    # Obtaining month, day, time and year
                    date_broken = msg_date.split()
                    month = date_broken[0]
                    day = date_broken[1][:-1]
                    year = date_broken[2]
                    time = date_broken[3]
                    time_broken = time.split(':')
                    hour = time_broken[0]
                    minute = time_broken[1][:-2] + time_broken[1][-2:].upper()

                    data['datetime'] = {
                        'month': month,
                        'day': day,
                        'year': year,
                        'hour': hour,
                        'minute': minute,
                    }

                    self.crushes_num += 1

                except (AttributeError, IndexError):
                    try:
                        if len(box.find('p').find('i').text) > 0:
                            data['type'] = 'Private'
                            self.priv_crush += 1
                            self.crushes_num += 1
                    except AttributeError:
                        pass

                self.posts.append(data)

    def get_crushes(self, num_crushes):
        for p in range(ceil(num_crushes/10)):
            self.get_page(p)

    def update_crushes_num(self):

        user_page = requests.get('http://www.thiscrush.com/~{}/'.format(self.username)).content

        soup = BeautifulSoup(user_page, 'lxml')

        self.crushes_num = int(soup.find_all('p', {'class':'tag-statistics txt-pink'})[2].text)

        return self.crushes_num
