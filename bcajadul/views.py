import sys, os
from pyramid.view import view_config
from time import sleep
from .Filelogger import FileLogger
from .BcaJadulController import BcaJadulController
from datetime import datetime, timedelta

from selenium import webdriver
#from selenium.webdriver.firefox.options import Options as selopt
from selenium.webdriver.chrome.options import Options as selopt
from selenium.webdriver.support.select import Select
from pyquery import PyQuery as pq
from copy import deepcopy

import logging
log = logging.getLogger(__name__)

class MainView(object):
	def __init__(self, request):
		self.request = request
		self.wd = None

	@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
	def my_view(self):
		return {'project': 'bcajadul'}
		
	@view_config(route_name='mutasi', renderer='json')
	def mutasi(self):
		try:
			reqon = BcaJadulController(self.request)
			reqon.checkComplete(reqon.REQ_MUTASI)
			
			username = self.request.params['username']
			password = self.request.params['password']
			rekening = self.request.params['rekening']
			from_date = self.request.params['from_date']
			to_date = self.request.params['to_date']
			
			if ( datetime.now() - timedelta(30) > datetime.strptime( from_date,'%Y-%m-%d') ):
				raise ('Tanggalnya awal minimal 30 hari yang lalu')
			
			if ( datetime.now() - timedelta(30) > datetime.strptime( to_date,'%Y-%m-%d') ):
				raise ('Tanggalnya akhir minimal 30 hari yang lalu')
			
			from_date = datetime.strptime( from_date,'%Y-%m-%d').strftime('%d/%m/%Y')
			to_date = datetime.strptime( to_date,'%Y-%m-%d').strftime('%d/%m/%Y')
			
			return {'code' : 'OK', 'message' : '' , 'data' : {'mutasi' : self.__scraping_mutasi(username, password, rekening, from_date, to_date), 'from_date' : self.request.params['from_date'], 'to_date' : self.request.params['to_date'],  'rekening' : rekening}}
			
		except Exception as e:
			log.exception('view exception error - {}'.format(str(e)))
			return {'code' : 'ERROR', 'message' : 'error - {}'.format(str(e)) , 'data' : None}
			
	
	def __scraping_mutasi(self, user_name, password, rekening, from_date, to_date):
		try:
			#rekening = '1210060608886'
			#date1 = '14/05/2019'
			#date2 = '14/05/2019'
			#username = xxx
			#password = xxx

			#viewSearch
			#fromDate
			#toDate

			#btnReset
			#btnClose
			#btnSearch
			#options = ChrmOpt()
			options = selopt()
			options.set_headless(headless=True)
			
			#self.wd = webdriver.Firefox(firefox_options=options, executable_path='geckodriver.exe')
			self.wd = webdriver.Chrome(chrome_options=options, executable_path='chromedriver.exe')
			
			attempt = 0
			
			self.wd.get('https://ibank.klikbca.com/')
			sleep(1)
			self.wd.find_elements_by_id('user_id')[0].send_keys(user_name)
			sleep(1)
			self.wd.find_elements_by_id('pswd')[0].send_keys(password)
			
			inputs = self.wd.find_elements_by_tag_name('input')
			self.wd.save_screenshot("ss/{}-1-depan.png".format(rekening))
			
			for each_input in inputs:
				if (each_input.get_property('value') == 'LOGIN'):
					each_input.click()
					sleep(1)
					break
			
			self.wd.save_screenshot("ss/{}-2-login.png".format(rekening))
			frames = self.wd.find_elements_by_tag_name('frame')
			
			for each_frame in frames:
				if (each_frame.get_property('name') == 'menu'):
					self.wd.switch_to.frame(each_frame)
					break
			
			links = self.wd.find_elements_by_tag_name('a')
			
			for each_link in links:
				if (each_link.get_property('href').find('account_information_menu.htm') > -1):
					each_link.click()
					sleep(1)
					break
			
			self.wd.save_screenshot("ss/{}-3-akun.png".format(rekening))
			links_continued = self.wd.find_elements_by_tag_name('a')
			
			for each_link in links_continued:
				if (each_link.text.find('utasi') > -1 and each_link.text.find('ekening') > -1):
					each_link.click()
					sleep(1)
					break
			
			self.wd.switch_to_default_content()
			frames = self.wd.find_elements_by_tag_name('frame')
			
			for each_frame in frames:
				if (each_frame.get_property('name') == 'atm'):
					self.wd.switch_to.frame(each_frame)
					break
			
			select_fr = Select(self.wd.find_element_by_id('D1'))
			opts_rekening = select_fr.options
			
			for i, each_option in enumerate(opts_rekening):
				#print("option {} | cari {}".format(each_option.text, rekening))
				if (each_option.text == rekening ):
					print('ada rekeningnya')
					select_fr.select_by_index(i)
					break
			# chk_harian
			self.wd.find_element_by_id('r1').click()
			 
			start_date_split = from_date.split('/')
			
			tmp_select = Select(self.wd.find_element_by_id('startDt'))
			tmp_options = tmp_select.options
			
			for i, each_option in enumerate(tmp_options):
				#print("option {} | cari {}".format(each_option.text, start_date_split[0]))
				if (each_option.text == start_date_split[0] ):
					tmp_select.select_by_index(i)
					break
			
			tmp_select = Select(self.wd.find_element_by_id('startMt'))
			tmp_options = tmp_select.options
			
			def noToMtAbrv(num_str):
				month = 'januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember'
				int_ = int(num_str) - 1
				return month.split('|')[int_]
			
			for i, each_option in enumerate(tmp_options):
				idx = noToMtAbrv(start_date_split[1].lower())
				#print("option {} | cari {}".format(each_option.text, idx))
				if (each_option.text.lower() == idx):
					tmp_select.select_by_index(i)
					break
			
			tmp_select = Select(self.wd.find_element_by_id('startYr'))
			tmp_options = tmp_select.options
			
			for i, each_option in enumerate(tmp_options):
				#print("option {} | cari {}".format(each_option.text, start_date_split[2]))
				if (each_option.text == start_date_split[2] ):
					tmp_select.select_by_index(i)
					break
					
			to_date_split = to_date.split('/')
			
			tmp_select = Select(self.wd.find_element_by_id('endDt'))
			tmp_options = tmp_select.options
			
			for i, each_option in enumerate(tmp_options):
				#print("option {} | cari {}".format(each_option.text, to_date_split[0]))
				if (each_option.text == to_date_split[0] ):
					tmp_select.select_by_index(i)
					break
			
			tmp_select = Select(self.wd.find_element_by_id('endMt'))
			tmp_options = tmp_select.options
			
			for i, each_option in enumerate(tmp_options):
				idx = noToMtAbrv(to_date_split[1].lower())
				#print("option {} | cari {}".format(each_option.text, idx))
				if (each_option.text.lower() == idx):
					tmp_select.select_by_index(i)
					break
			
			tmp_select = Select(self.wd.find_element_by_id('endYr'))
			tmp_options = tmp_select.options
			
			for i, each_option in enumerate(tmp_options):
				#print("option {} | cari {}".format(each_option.text, to_date_split[2]))
				if (each_option.text == to_date_split[2] ):
					tmp_select.select_by_index(i)
					break
			 
			self.wd.save_screenshot("ss/{}-4-cari-mutasi.png".format(rekening))
			inputs = self.wd.find_elements_by_tag_name('input')
			
			for each_input in inputs:
				if (each_input.get_property('value').find('ihat') > -1 and each_input.get_property('value').find('utasi') > -1 and each_input.get_property('value').find('ekening') > -1 ):
					each_input.click()
					sleep(1)
					break
			
			self.wd.save_screenshot("ss/{}-5-daftar-mutasi.png".format(rekening))
			
			entries_mutasi_el = self.wd.find_elements_by_tag_name('table')[4].find_elements_by_tag_name('tr')
			entry_mutasi = []
			
			for i, each_entri in enumerate(entries_mutasi_el, start = 1):
				try:
					tiap_mutasi = {}
					split_entri = each_entri.find_elements_by_tag_name('td')
					tiap_mutasi['tanggal'] = split_entri[0].text
					tiap_mutasi['keterangan'] = split_entri[1].text.replace("\n", "")
					tiap_mutasi['cab'] = split_entri[2].text
					tiap_mutasi['mutasi_col_l'] = split_entri[3].text
					tiap_mutasi['mutasi_col_r'] = split_entri[4].text
					tiap_mutasi['saldo'] = split_entri[5].text
					entry_mutasi.append(deepcopy(tiap_mutasi))
				except:
					pass
			
			self.scrapLogout__()
			self.wd.save_screenshot("ss/{}-6-keluar.png".format(rekening))
			self.wd.quit()
					
			return entry_mutasi
		
		except Exception as e:
			self.scrapLogout__()
			self.wd.save_screenshot("ss/{}-6-keluar.png".format(rekening))
			self.wd.quit()
			
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			
			raise e
			
	
	def scrapLogout__(self):
		self.wd.switch_to_default_content()
			
		frames = self.wd.find_elements_by_tag_name('frame')
		
		for each_frame in frames:
			if (each_frame.get_property('name') == 'menu'):
				self.wd.switch_to.frame(each_frame)
				break
		
		links_continued = self.wd.find_elements_by_tag_name('a')
		
		for each_link in links_continued:
			if (each_link.text.find('embali') > -1 and each_link.text.find('enu') > -1 and each_link.text.find('tama') > -1):
				each_link.click()
				break
		
		
		frames = self.wd.find_elements_by_tag_name('frame')
		
		for each_frame in frames:
			if (each_frame.get_property('name') == 'menu'):
				self.wd.switch_to.frame(each_frame)
				break
		
		links_continued = self.wd.find_elements_by_tag_name('a')
		
		for each_link in links_continued:
			if (each_link.text.find('[') > -1 and each_link.text.find('LOGOUT') > -1 and each_link.text.find(']') > -1):
				each_link.click()
				break
