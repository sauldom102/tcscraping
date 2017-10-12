import requests
from bs4 import BeautifulSoup

user = input('User: ')
num_pages = input('Number of pages to get: ')

for num_page in range(int(num_pages)):
    page = requests.get('http://www.thiscrush.com/~{}/{}'.format(str(user),str(num_page+1))).content

    soup = BeautifulSoup(page, 'lxml')

    boxes = soup.find('div',{'class':'row-4'}).find_all('div',{'class':'row'})

    for box in boxes:
        try:
            message = box.find("p").text.strip().replace('\t','').replace('\r\n','').split('\n')
            print(message[0],message[1],sep='\n',end='\n\n')
        except AttributeError:
            pass
        except IndexError:
            pass
