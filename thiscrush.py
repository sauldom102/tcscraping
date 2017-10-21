import requests
from bs4 import BeautifulSoup

class Main():

    def __init__(self,user,num_pages):
        self.user = user
        self.num_pages = num_pages

        self.crushes_num = 0
        self.anon_num = 0

        self.priv_crush = 0
        self.likes = 0

    def get(self):
        out_file = open('{}.txt'.format(self.user),'a')

        for num_page in range(int(self.num_pages)):
            page = requests.get('http://www.thiscrush.com/~{}/{}'.format(str(self.user),str(num_page+1))).content

            soup = BeautifulSoup(page, 'lxml')

            boxes = soup.find('div',{'class':'row-4'}).find_all('div',{'class':'row'})

            if len(boxes) > 1:
                for box in boxes:
                    try:
                        msg = box.find("p").text.strip().replace('\t','').replace('\r\n','').split('\n')
                        try:
                            msg.remove('')
                        except ValueError:
                            pass

                        # Obtaining message content, message author and message date
                        msg_content = msg[0].encode('utf-8')
                        msg_author = msg[1][1:].encode('utf-8')
                        msg_date = box.find('span').text[13:]

                        if msg_content == b'Quick Like -I like you!':
                            msg_content = 'Like'
                            self.likes += 1

                        # Obtaining month, day, time and year
                        date_broken = msg_date.split()
                        month = date_broken[0]
                        day = date_broken[1][:-1]
                        year = date_broken[2]
                        time = date_broken[3]

                        out_file.write('{} - {} - {} | {}\n'.format(day,month,year,time))
                        out_file.write('{}\n'.format(msg_content))
                        out_file.write('{}\n'.format(msg_author))
                        out_file.write('\n')

                        if msg_author == b'Anonymous':
                            self.anon_num += 1
                        self.crushes_num += 1
                    except (AttributeError, IndexError) as e:
                        try:
                            if len(box.find('p').find('i').text) > 0:
                                out_file.write('Private\n\n')
                                self.priv_crush += 1
                                self.crushes_num += 1
                        except AttributeError:
                            pass
            else:
                break

        print('{} has {} likes'.format(self.user,self.likes))
        print('Got',self.crushes_num-self.likes,'crush posts')
        print('{} crushes are private'.format(self.priv_crush))
        print('{} ({:.2%}) crushes are anonymous'.format(self.anon_num,self.anon_num/self.crushes_num))

        out_file.close()
