from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir
from urllib.parse import urlparse, parse_qs
from pick import pick
import time
import urllib.request
import zipfile

hacklist = []

def set_hack_list(hl):
	global hacklist
	hacklist = hl

def get_hack_list(browser,first = True,url = "https://www.smwcentral.net/?p=section&s=smwhacks"):
	global hacklist
	if first:
		hacklist = []
		print("Opening SMWC to check for new hacks...")

	browser.get(url)
	print("Trying "+url)
	hackrows = browser.find_elements_by_xpath("//div[@id='list_content']//table//tr[position()>1]")

	for row in hackrows:
		firsttd = row.find_element_by_xpath(".//td[1]")
		infolink = firsttd.find_element_by_xpath(".//a").get_attribute('href')
		downloadlink = row.find_element_by_xpath(".//td[last()]//a").get_attribute('href')
		title = firsttd.find_element_by_xpath(".//a").text
		hack = {
			"id":parse_qs(urlparse(infolink).query).get('id')[0],
			"title": title,
			"added": datetime.strptime(firsttd.find_element_by_xpath(".//span//time").text,"%Y-%m-%d %I:%M:%S %p").strftime('%s'),
			"download-link": downloadlink,
			"detail-link":infolink
		}
		print("Found "+title)
		hacklist.append(hack)

	nextpage = browser.find_element_by_xpath("//td[@id='menu2']//td[1]//a[last()]")
	try:
		imgtest = nextpage.find_element_by_xpath('.//img')
		nextpage = nextpage.get_attribute('href')
		print('Found another page, trying page '+parse_qs(urlparse(nextpage).query).get('n')[0])
		return get_hack_list(browser,False,nextpage)
	except Exception as e:
		print("")

	return {"updated":time.time(), "hack_list": hacklist}

def get_entry_from_title(title):
	global hacklist
	for h in hacklist:
		if h['title'] == title:
			return h

def download_hack(h,path):
	url = h['download-link']
	dlpath = path+'/_smwci.zip'

	opener=urllib.request.build_opener()
	opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
	urllib.request.install_opener(opener)

	print('Downloading file from '+url)
	urllib.request.urlretrieve(url,dlpath)
	return dlpath

def unzip_hack(path,tmpdir):
	zip_ref = zipfile.ZipFile(path, 'r')
	zip_ref.extractall(tmpdir)
	zip_ref.close()
	files = []
	for f in listdir(tmpdir):
		if isdir(join(tmpdir,f)):
			for fd in listdir(join(tmpdir,f)):
				files.append(join(tmpdir,f,fd))
		elif isfile(join(tmpdir, f)):
			files.append(join(tmpdir, f))
	return files

def apply_bps(patch_path,source_path,dest_path):
	from bps.apply import apply_to_files
	source_patch = open(patch_path,'rb')
	source_rom = open(source_path,'rb')
	dest_path = open(dest_path,'wb')
	return apply_to_files(source_patch,source_rom,dest_path)
	
def apply_ips(patch_path,source_path,dest_path):
	ips.applyPatch(source_path,patch_path,dest_path)

def get_title(h):
	return h.get('title')

def draw_table():
	global hacklist
	title = "Please select a Hack:"
	title, index = pick(hacklist,title, indicator='*', options_map_func=get_title)
	return title