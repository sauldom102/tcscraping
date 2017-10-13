import requests
from bs4 import BeautifulSoup

user = input('User: ')
num_pages = input('Number of pages to get: ')

crushes_num = 0
anon_num = 0

for num_page in range(int(num_pages)):
    page = requests.get('http://www.thiscrush.com/~{}/{}'.format(str(user),str(num_page+1))).content

    soup = BeautifulSoup(page, 'lxml')

    boxes = soup.find('div',{'class':'row-4'}).find_all('div',{'class':'row'})

    if len(boxes) > 1:
        for box in boxes:
            try:
                msg = box.find("p").text.strip().replace('\t','').replace('\r\n','').split('\n')

                # Obtaining message content, message author and message date
                msg_content = msg[0]
                msg_author = msg[1]
                msg_date = msg[2][13:]

                # Obtaining month, day, time and year
                date_broken = msg_date.split()
                month = date_broken[0]
                day = date_broken[1][:-1]
                year = date_broken[2]
                time = date_broken[3]
                print(month,day,year,time)

                print(msg_content,msg_author,sep='\n',end='\n\n')

                if msg_author == '-Anonymous':
                    anon_num += 1
                crushes_num += 1
            except AttributeError:
                pass
            except IndexError:
                pass
    else:
        break

print('Got',crushes_num,'crushes')
print('{} ({:.2%}) crushes are anonymous'.format(anon_num,anon_num/crushes_num))