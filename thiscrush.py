import requests
from bs4 import BeautifulSoup


def clean_text(text):
    return text.strip().replace('\t', '').replace('\r\n', '')


class Main():

    def __init__(self,user,num_pages):
        self.user = user
        self.num_pages = num_pages

        self.posts = list()

        self.crushes_num = 0
        self.anon_num = 0

        self.priv_crush = 0
        self.likes = 0

    def get(self):

        for num_page in range(int(self.num_pages)):
            page = requests.get('http://www.thiscrush.com/~{}/{}'.format(str(self.user),str(num_page+1))).content

            soup = BeautifulSoup(page, 'lxml')

            boxes = soup.find('div',{'id':'content'}).find_all('div',{'class':'post'})

            if len(boxes) > 1:
                for box in boxes:
                    try:

                        # Obtaining message content, message author and message date
                        msg_content = clean_text(box.find('p',{'class':'txt-user-crush'}).text).encode('utf-8')
                        msg_author = clean_text(box.find('div', {'class':'col-xs-8 col-sm-8'}).find('p', {'class':'no-margin'}).text).encode('utf-8')
                        msg_date = clean_text(box.find('div', {'class':'col-xs-8 col-sm-8'}).find('p', {'class':'posted-date-time txt-grey'}).text)

                        data = {
                            'to_user': self.user,
                        }

                        if msg_content == b'I like you!' and msg_author.startswith(b'Quick Like -'):
                            data['type'] = 'Like'
                            data['author'] = msg_author[11:]
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
            else:
                break

        print('{} has {} likes'.format(self.user,self.likes))
        print('Got',self.crushes_num-self.likes,'crush posts')
        print('{} crushes are private'.format(self.priv_crush))
        print('{} ({:.2%}) crushes are anonymous'.format(self.anon_num,self.anon_num/self.crushes_num))