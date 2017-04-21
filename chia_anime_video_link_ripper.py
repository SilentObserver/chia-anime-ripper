from bs4 import BeautifulSoup as bs
import requests as rq

errors = []

def get_next_page_link(web_page_soup):
	next_page_tag = web_page_soup.find('a',{'rel':'next'})
	if next_page_tag is None:
		return False
	else:
		return next_page_tag.get('href')

def get_download_page_link(web_page_soup):
	return web_page_soup.find('a',{'id':'download'}).get('href')

def get_download_link(download_page_link):
	download_page_soup = None
	i=0
	while i<30:
		try:
			download_page_soup = bs(rq.get(download_page_link).content,'lxml')
		except Exception as e:
			i+=1
			print("connection problem. retry ",i)
		if download_page_soup is not None:
			break
	for x in download_page_soup.find_all('a'):
		if x.text == '' and '.mp4' in x.get('href'):
			return x.get('href')

def get_anime_download_links(first_episode_page_link):
	page_link = first_episode_page_link
	download_links = []
	while True:
		print("Scraping link:",page_link)
		web_page_soup = None
		i=0
		while i<30:
			try:
				web_page_soup = bs(rq.get(page_link).content,'lxml')	
			except Exception as e:
				i+=1
				print("connection problem. retry ",i)

			if web_page_soup is not None:
				break;
		if web_page_soup is not None:
			individual_download_link = get_download_link(get_download_page_link(web_page_soup))
			if individual_download_link is not None:
				download_links.append(individual_download_link)
			else:
				download_links.append("/"*30+"\nError obtaining download link\n"+"\\"*30)
			next_page = get_next_page_link(web_page_soup)
		if not next_page:
			break
		else:
			page_link = next_page
	return download_links

if __name__ == '__main__':
	statring_page = input('Enter first episode page link:')
	file_name = input('\nEnter distination file name:')
	download_links = get_anime_download_links(statring_page)
	no_of_errors = 0
	with open(file_name,'a') as f:
		for link in download_links:
			if link is not None:
				f.write(link)
			else:
				no_of_errors+=1
			f.write("\n")
	print("No. of errors =",no_of_errors)
