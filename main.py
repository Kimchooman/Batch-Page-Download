from bs4 import BeautifulSoup
import cfscrape
import os
import requests

class Link:

	def __init__(self, url, iteration):

		self.iter = iteration
		self.url = url

	def __str__(self):
		return self.url

class Page:
	def __init__(self, url, target="text",IUAM=False):

		self.scraper = cfscrape.CloudflareScraper()
		self.IUAM = IUAM # Refers to cloudflare anti-bot protection "im under attack mode"

		self.soup = None

		if target == "text":
			if self.IUAM is True:
				self.html = self.scraper.get(url).text

			else:
				self.html = requests.get(url).text

		elif target == "raw":
			if self.IUAM is True:
				self.html = self.scraper.get(url).raw

			else:
				self.html = requests.get(url).raw

		elif target == "None":
			if self.IUAM is True:
				self.html = self.scraper.get(url)

			else:
				self.html = requests.get(url)

	def pull_txt(self):

		self.soup = BeautifulSoup(self.html, "html.parser")
		self.soup.prettify()

	def write_all_p_to_text(self,file_name):

		with open(f"{file_name}.txt", "w") as fh:

			for p_seg in self.soup.find_all("p"):

				p_seg = p_seg.string

				fh.write(f"{p_seg}\n\n")

class BatchUrlGenerator:

	def __init__(self, url, start=0, stop=None, IUAM=False):

		self.start = start
		self.stop = stop

		self.urls_array = []

		self.chapter_index = None

		self.url_split = url.split("/")

		temp_str = ""
		count = 0

		for seg in self.url_split:

			temp_str += f"{count} --> {seg}\n"
			count += 1

		print(temp_str)

		while self.chapter_index == None: # Finding iterable element of url

			self.chapter_index = input("Which Index does the iterable element belong to: ")

			if self.chapter_index.isnumeric() is False:

				print("Error, the index must be a number")
				self.chapter_index = None

		self.chapter_index = int(self.chapter_index)

		temp = self.url_split[self.chapter_index]
		while temp[-1].isnumeric() is True:
			temp = temp[0:-1]

		for n in range(self.start, self.stop):

			self.url_split[self.chapter_index] = f"{temp}{n}"

			string = ""
			for seg in self.url_split:

				string += f"{seg}/"

			string = string[0:-1]

			self.urls_array.append(Link(string, n))

url = "https://www.lightnovelpub.com/novel/reader-19072354/chapter-0"

urls= BatchUrlGenerator(url,start=0, stop=10)

curr = Page(urls.urls_array[0], IUAM=True)

file_name = input(f"Making File for {urls.urls_array[0]} what should the file be named... ")

os.mkdir(file_name)

for link in urls.urls_array:

	curr_page = Page(link, IUAM=True)

	curr_page.pull_txt()

	name = f"Chapter-{link.iter}"

	curr_page.write_all_p_to_text(f"{file_name}/{name}")
