import imapclient
import pprint
import pyzmail
from bs4 import BeautifulSoup
import webbrowser

account = input('你的gmail位址：')
pw = input('你的gmail密碼：')

imapObj = imapclient.IMAPClient('imap.gmail.com',ssl=True)
imapObj.login(account, pw)
imapObj.select_folder('INBOX', readonly=True)

UIDs = imapObj.search(['UNSEEN'])
# 開啟每一封郵件
rawMessages = imapObj.fetch(UIDs,['BODY[]'])

# 一個空串列準備放置取消訂閱連結
urls = []

# 瀏覽每一封郵件內容
for UID in UIDs:
	message = pyzmail.PyzMessage.factory(rawMessages[UID][b'BODY[]'])
	# 當郵件為html格式
	if message.html_part != None:
		try:
			content = message.html_part.get_payload().decode(message.html_part.charset)
			bsObj = BeautifulSoup(content,"lxml")
			try:
				# 找到該郵件中所有的連結
				links = bsObj.findAll("a")
				for link in links:
					# 找到取消訂閱連結
					words = ["取消電子報", "取消訂閱", "unsubscribe"]
					if any(word in link.get_text() for word in words):	
						url = link.attrs['href']
						# 確認連結沒有重複
						if url not in urls:
							urls.append(url)		
			except Exception :
				print("沒有連結")
			else:
				pass
		except Exception:
			print('不管它')
		else:
			pass
		finally:
			pass
# print(urls)
for url in urls:
	webbrowser.open(url)

imapObj.logout()		