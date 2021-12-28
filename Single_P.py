import httplib2
import os
import re
import threading
import urllib
import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class CrawlerSingleton(object):
	def __new__(cls):
		""" создает одноэлементный объект, если он не создан, или возвращает предыдущий одноэлементный объект"""
		if not hasattr(cls, 'instance'):
			cls.instance = super(CrawlerSingleton, cls).__new__(cls)
		return cls.instance

def navigate_site(max_links = 5):
	""" перемещаться по сайту с помощью алгоритма BFS, находить ссылки и размещать их для загрузки изображений """

	# одиночный экземпляр
	parser_crawlersingleton = CrawlerSingleton()
	
	# На начальном этапе url_queue имеет main_url.
	# При разборе страницы main_url новые ссылки, принадлежащие
	# тот же веб-сайт добавляется в url_queue до тех пор, пока
	# равно max _links.
	while parser_crawlersingleton.url_queue:

		# проверяет, достиг ли он макс. ссылка на сайт
		if len(parser_crawlersingleton.visited_url) == max_links:
			return

		# вытащить URL из очереди
		url = parser_crawlersingleton.url_queue.pop()

		# подключиться к веб-странице
		http = httplib2.Http()
		try:
			status, response = http.request(url)
		except Exception:
			continue
		
		# добавьте ссылку для загрузки изображений
		parser_crawlersingleton.visited_url.add(url)
		print(url)

		# сканировать веб-страницу и получать ссылки внутри
		# главная страница
		bs = BeautifulSoup(response, "html.parser")

		for link in BeautifulSoup.findAll(bs, 'a'):
			link_url = link.get('href')
			if not link_url:
				continue

			# проанализировать полученную ссылку
			parsed = urlparse(link_url)
			
			# пропустите ссылку, если она ведет на внешнюю страницу
			if parsed.netloc and parsed.netloc != parsed_url.netloc:
				continue

			scheme = parsed_url.scheme
			netloc = parsed.netloc or parsed_url.netloc
			path = parsed.path
			
			# создать полный URL
			link_url = scheme +'://' +netloc + path

			
			# пропускает, если ссылка уже добавлена
			if link_url in parser_crawlersingleton.visited_url:
				continue
			
			# Добавить новую полученную ссылку, чтобы цикл while продолжался со следующей итерации.
			parser_crawlersingleton.url_queue = [link_url] +\
												parser_crawlersingleton.url_queue
			
class ParallelDownloader(threading.Thread):
	""" Download the images parallelly """
	def __init__(self, thread_id, name, counter):
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		print('Starting thread', self.name)
		# function to download the images
		download_images(self.name)
		print('Finished thread', self.name)
			
def download_images(thread_name):
	# singleton instance
	singleton = CrawlerSingleton()
	# visited_url has a set of URLs.
	# Here we will fetch each URL and
	# download the images in it.
	while singleton.visited_url:
		# pop the url to download the images
		url = singleton.visited_url.pop()

		http = httplib2.Http()
		print(thread_name, 'Downloading images from', url)

		try:
			status, response = http.request(url)
		except Exception:
			continue

		# проанализировать веб-страницу, чтобы найти все изображения
		bs = BeautifulSoup(response, "html.parser")

		# Найти все теги <img>
		images = BeautifulSoup.findAll(bs, 'img')

		for image in images:
			src = image.get('src')
			src = urljoin(url, src)

			basename = os.path.basename(src)
			print('basename:', basename)

			if basename != '':
				if src not in singleton.image_downloaded:
					singleton.image_downloaded.add(src)
					print('Downloading', src)
					# Download the images to local system
					urllib.request.urlretrieve(src, os.path.join('images', basename))
					print(thread_name, 'finished downloading images from', url)

def main():
	# одиночный экземпляр
	crwSingltn = CrawlerSingleton()

	# добавление url-адреса в очередь на парсинг
	crwSingltn.url_queue = [main_url]

	# инициализация набора для хранения всех посещенных URL
    # для загрузки изображений.
	crwSingltn.visited_url = set()

	# инициализация набора для хранения пути загруженных изображений
	crwSingltn.image_downloaded = set()
	
	# вызов метода для сканирования веб-сайта
	navigate_site()

	## создать каталог изображений, если он не существует
	if not os.path.exists('images'):
		os.makedirs('images')

	thread1 = ParallelDownloader(1, "Thread-1", 1)
	thread2 = ParallelDownloader(2, "Thread-2", 2)

	# Начать новые темы
	thread1.start()
	thread2.start()

	
if __name__ == "__main__":
	main_url = ("https://www.geeksforgeeks.org/")
	parsed_url = urlparse(main_url)
	main()
