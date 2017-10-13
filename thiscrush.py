import requests
from bs4 import BeautifulSoup

user = input('User: ')
num_pages = input('Number of pages to get: ')

crushes_num = 0
anon_num = 0

priv_crush = 0

out_file = open('{}.txt'.format(user),'a')

for num_page in range(int(num_pages)):
    page = requests.get('http://www.thiscrush.com/~{}/{}'.format(str(user),str(num_page+1))).content

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
                    anon_num += 1
                crushes_num += 1
            except AttributeError as e:
                try:
                    if len(box.find('p').find('i').text) > 0:
                        out_file.write('Private\n\n')
                        priv_crush += 1
                except AttributeError:
                    pass
                pass
            except IndexError as e:
                try:
                    if len(box.find('p').find('i').text) > 0:
                        out_file.write('Private\n\n')
                        priv_crush += 1
                except AttributeError:
                    pass
                pass
    else:
        break

print('{} private crushes'.format(priv_crush))
print('Got',crushes_num,'crushes')
print('{} ({:.2%}) crushes are anonymous'.format(anon_num,anon_num/crushes_num))

out_file.close()