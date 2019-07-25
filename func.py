# func.py
# -*- coding: utf-8 -*-

import requests
import json
import urllib
import re
from bs4 import BeautifulSoup
import const

hapikey = const.apikey

def get_all_companies_properties(target):
	get_all_companies_url = "https://api.hubapi.com/companies/v2/companies/paged?"
	max_results = 500
	limit = 5
	parameter_dict = {'hapikey': hapikey, 'limit': limit, 'properties': target}
	headers = {}
	company_list = []

	has_more = True
	while has_more:
		parameters = urllib.urlencode(parameter_dict)
		get_url = get_all_companies_url + parameters
		r = requests.get(url= get_url, headers = headers)
		response_dict = json.loads(r.text)
		has_more = response_dict['has-more']
		company_list.extend(response_dict['companies'])
		parameter_dict['offset']= response_dict['offset']
		if len(company_list) >= max_results: # Exit pagination, based on whatever value you've set your max results variable to.
			print('maximum number of results exceeded')
			break

	list_length = len(company_list)
	print("You've succesfully parsed through {} company records and added them to a list".format(list_length))
	return company_list

def get_all_favicons():
	company_list = get_all_companies_properties('website')
	for company in company_list:
		favicon_url = 'http://www.google.com/s2/favicons?domain=www.' + company['properties']['website']['value']
		icon = urllib.urlopen(favicon_url)
		path = 'favicons/'
		print(company['properties']['website']['value'])
		with open(path + company['properties']['website']['value'] + ".ico", "wb") as f:
			f.write(icon.read())

def get_all_address():
	company_list = get_all_companies_properties('website')
	for company in company_list:
		print(company['properties']['website']['value'])
		url = 'http://' + company['properties']['website']['value']
		try:
			html = requests.get(url)
		except:
			url = 'http://www.' + company['properties']['website']['value']
		html = urllib.urlopen(url)
		soup = BeautifulSoup(html, "html.parser")
		name = soup.title.string
		print(name)
		#pre = soup.find_all(string=['北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県','茨城県','栃木県','群馬県','埼玉県','千葉県','東京都','神奈川県','新潟県','富山県','石川県','福井県','山梨県','長野県','岐阜県','静岡県','愛知県','三重県','滋賀県','京都府','大阪府','兵庫県','奈良県','和歌山県','鳥取県','島根県','岡山県','広島県','山口県','徳島県','香川県','愛媛県','高知県','福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県'])
		#pre = soup.find_all(text=re.compile('東'))
		#print(pre)

def reset_all_companies():
	if const.production_mode:
		print('Sorry. This command is forbidden in production_mode')
		return 0
	company_list = get_all_companies_properties('website')
	#delete
	for company in company_list:
		company_id = company['companyId']
		print(company_id)
		url = 'https://api.hubapi.com/companies/v2/companies/' + str(company_id) + '?hapikey=' + hapikey
		requests.delete(url)
		print('delete')
	print('delete all company data\n')
	set_companys()

def set_companys():
	#company_list = ['automation.jp','sbigroup.co.jp','aijus.com','hubspot.com','i.softbank.jp','tabio.com','tokyo-shoseki.co.jp','aqua-alta.jp','nadai.jp','kmecs.co.jp','nearme.jp','netcombb.co.jp','ml.nadai.jp','startbahn.jp','vonage.com','lusterworks.co.jp','airport-in-a-box.com','outsourcing.co.jp','s-cubism.jp','oaklawn.co.jp','dn.smbc.co.jp','hrm.nadai.jp','zeal-career.co.jp','higashi-nipponbank.jp','mufg.jp','escco.co.jp','diverta.co.jp','mizuhobank.co.jp','briscola.co.jp','wi2.co.jp','anicecompany.co.jp','w-design.co.jp','inctas.co.jp','totarotanaka.com','tandt1212.com','heartbeats.jp','naked.co.jp','tsunagu.info','yper.co.jp','vow-system.co.jp','47club.jp','ambient-co.jp','jp-md.co.jp','jwa.or.jp','tn-japan.co.jp','wics.co.jp','sankosc.co.jp','nmp-specialist.com','ksk-anl.com','musashino.jp','esteri.it','gmail.co','yohten.com','mail.dnp.co.jp','tokyo-chefs.jp','sbigroup.co.jp','dwango.co.jp','nii.ac.jp','bsy.jfe-eng.co.jp','villanova.edu','ksone.jp','iwanichi.co.jp','zicon.net','amperaxp.com','ims.u-tokyo.ac.jp','starkmind.co.jp','denen.com','life-book.co.jp','guitto.co.jp','hgc.jp','sbsnt.co.jp','fusenetwork.co.jp','blnk.co.jp','jp.fujitsu.com','huynq.net','broadleaf.co.jp','taishukan.co.jp','hackerx.org']
	company_list = ['taishukan.co.jp','broadleaf.co.jp','automation.jp','sbigroup.co.jp','aijus.com','hubspot.com']
	for company in company_list:
		print(company)
		url = 'https://api.hubapi.com/companies/v2/companies?hapikey=' + hapikey
		data = json.dumps({'properties':[{'name':'website','value':company}]})
		#print(data)
		r = requests.post(url,data,headers={'Content-Type': 'application/json'})
		print(r)
	print('finish set process\n')

def show_companys():
	print('show')
	data = '\''
	company_list = get_all_companies_properties('website')
	for company in company_list:
		data += company['properties']['website']['value'] + '\',\''
	print(data)

# def update_companys():
# 	company_list = get_all_companies_properties('hs_avatar_filemanager_key')
# 	for company in company_list:
# 		company_id = company['companyId']
# 		url = 'https://api.hubapi.com/companies/v2/companies/' + str(company_id) + '?hapikey=' + hapikey
# 		#data = json.dumps({'properties':[{'name':'hs_avatar_filemanager_key','value':'hubfs/6181502/test/jp.fujitsu.com.ico'}]})
# 		data = json.dumps({'properties':[{'name':'hs_avatar_filemanager_key','value':'hubfs/6181502/517fa98c-7944-47e9-95a8-e6e3b259c28f.png'}]})
# 		#print(data)
# 		r = requests.put(url,data,headers={'Content-Type': 'application/json'})
# 		print(json.loads(r.text))
#
# def avatar_companys():
# 	company_list = get_all_companies_properties('hs_avatar_filemanager_key')
# 	for company in company_list:
# 		company_av = company['properties']#['hs_avatar_filemanager_key']['value']
# 		print(company_av)
# 		print('')

#test
def test():
	print('test myfunc')

	return 'test'
