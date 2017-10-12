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

    for box in boxes:
        try:
            msg = box.find("p").text.strip().replace('\t','').replace('\r\n','').split('\n')
            msg_content = msg[0]
            msg_author = msg[1]
            msg_date = msg[2][12:]
            print(msg_content,msg_author,msg_date,sep='\n',end='\n\n')

            if msg_author == '-Anonymous':
                anon_num += 1
            crushes_num += 1
        except AttributeError:
            pass
        except IndexError:
            pass

print(crushes_num)
print(anon_num)
print(anon_num/crushes_num*100,"%")