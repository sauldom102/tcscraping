from requests_html import HTMLSession
from math import ceil
import re, traceback

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

		self.session = HTMLSession()

	def get_crushes(self, num_crushes):
		for offset in range(0, num_crushes, 6):
			r = self.session.get('https://www.thiscrush.com/get_posts.php?from={}&id={}&type=user'.format(offset, self.username))

			# boxes = soup.find('div',{'id':'content'}).find_all('div',{'class':'post'})
			iframes = r.html.find('iframe.iframe_posts')

			for iframe in iframes:
				r2 = self.session.get('https://www.thiscrush.com{}'.format(iframe.attrs['src']))

				boxes = r2.html.find('div.post')

				if len(boxes) > 0:
					for box in boxes:
						data = {
							'to_user': self.username,
						}

						# try:
						# Obtaining message content, message author and message date
						msg_tag = box.find('p.txt-user-crush', first=True)
						if msg_tag:
							fake_email = msg_tag.find('a.__cf_email__')
							# msg_pattern = r'.*(\[email_protected\]).*'

							msg_content = clean_text(msg_tag.text).encode('utf-8')
							msg_author = clean_text(box.find('div.col-xs-8.col-sm-8 p.no-margin', first=True).text).encode('utf-8')
							msg_date = clean_text(box.find('div.col-xs-8.col-sm-8 p.posted-date-time.txt-grey', first=True).text)

							# print('Fake email: {}'.format(len(fake_email)))
							# print(re.match(msg_pattern, msg_content).groups())

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
						else:
							try:
								if len(box.find('p i', first=True).text) > 0:
									data['type'] = 'Private'
									self.priv_crush += 1
									self.crushes_num += 1
							except AttributeError:
								pass

						# except (AttributeError, IndexError) as e:
						# 	print(data)
						# 	print(msg_content)
						# 	print(e)
						# 	try:
						# 		if len(box.find('p i', first=True).text) > 0:
						# 			data['type'] = 'Private'
						# 			self.priv_crush += 1
						# 			self.crushes_num += 1
						# 	except AttributeError:
						# 		pass

						self.posts.append(data)
						msg_content = None
						msg_author = None
						msg_date = None

	def update_crushes_num(self):
		user_page = self.session.get('http://www.thiscrush.com/~{}/'.format(self.username))

		self.crushes_num = int(user_page.html.find('p.tag-statistics.txt-pink')[2].text)

		return self.crushes_num
