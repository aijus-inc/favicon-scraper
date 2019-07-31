# func.py
# -*- coding: utf-8 -*-

import requests
import json
import urllib
import re
import csv
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
		if len(company_list) >= max_results:
			print('maximum number of results exceeded')
			break

	list_length = len(company_list)
	print("You've succesfully parsed through {} company records and added them to a list".format(list_length))
	return company_list

def get_all_favicons():
	company_list = get_all_companies_properties('website')
	for company in company_list:
		favicon_url = 'https://www.google.com/s2/favicons?domain=' + company['properties']['website']['value']
		icon = urllib.urlopen(favicon_url)
		path = 'favicons/'
		print(company['properties']['website']['value'])
		with open(path + company['properties']['website']['value'] + ".ico", "wb") as f:
			f.write(icon.read())

def get_all_address():
	company_list = get_all_companies_properties('website')
	with open('address_list.csv', 'w',) as f:
		writer = csv.writer(f)
		writer.writerow(["ドメイン", "ページタイトル", "住所候補"])
		for company in company_list:
			print(company['properties']['website']['value'])
			url = 'http://www.' + company['properties']['website']['value']
			print(url+"にアクセス".decode('utf-8'))
			try:
				html = urllib.urlopen(url)
			except:
				url = 'http://' + company['properties']['website']['value']
				try:
					html = urllib.urlopen(url)
				except:
					print("サイトが見つかりませんでした\n")
					writer.writerow([company['properties']['website']['value'],"サイトが見つかりませんでした"])
					continue
			soup = BeautifulSoup(html, "html.parser")
			name = soup.title.string if soup.title else ''
			#エラーページにひっかかった場合に、トップページを探す特別処理
			error_pattern = re.compile("見つかりません|ERROR|Error|error".decode('utf-8'))
			if error_pattern.search(name):
				url = 'http://' + company['properties']['website']['value']
				print(url+"に改めてアクセス".decode('utf-8'))
				try:
					html = urllib.urlopen(url)
				except:
					print("サイトが見つかりませんでした\n")
					writer.writerow([company['properties']['website']['value'],"サイトが見つかりませんでした"])
					continue
				soup = BeautifulSoup(html, "html.parser")
				name = soup.title.string if soup.title else ''
			print("--タイトル--")
			print(name)

			print("--住所のありそうなリンク--")
			address_set = set()
			row = [company['properties']['website']['value'], name.encode('utf-8')]
			#住所候補を取得、表示
			pattern = re.compile(u".+(都|道|府|県).+(区|市|町|村)")
			for address in soup.find_all(text=pattern):
				address_set.add(address)
			#住所のありそうなリンク先を取得
			linkset = set()
			for link in soup.find_all("a",text=re.compile("会社概要|アクセス|Access|access".decode('utf-8'))):
				if link.get('href'):
					print(link)
					linkset.add(link.get('href'))
			#各ページにアクセス
			print("--住所候補--")
			for dir in linkset:
				url = dir if re.match("http",dir) else url+dir
				try:
					html = urllib.urlopen(url)
				except:
					continue
				soup = BeautifulSoup(html, "html.parser")
				#住所候補の表示
				for address in soup.find_all(text=pattern):
					address_set.add(address)
			for address in address_set:
				print(address.encode('utf-8'))
				row.append(address.encode('utf-8'))
			print('')
			writer.writerow(row)
		#for
	#close
	print("データをaddress_list.csvとして保存しました。")


def reset_all_companies():
	if const.production_mode:
		print('Sorry. This command is forbidden in production_mode')
		return 0
	company_list = get_all_companies_properties('website')
	for company in company_list:
		company_id = company['companyId']
		print(company_id)
		url = 'https://api.hubapi.com/companies/v2/companies/' + str(company_id) + '?hapikey=' + hapikey
		requests.delete(url)
		print('delete')
	print('delete all company data\n')
	set_companys()

def set_companys():
	company_list = ['automation.jp','sbigroup.co.jp','aijus.com','hubspot.com','i.softbank.jp','tabio.com','tokyo-shoseki.co.jp','aqua-alta.jp','nadai.jp','kmecs.co.jp','nearme.jp','netcombb.co.jp','ml.nadai.jp','startbahn.jp','vonage.com','lusterworks.co.jp','airport-in-a-box.com','outsourcing.co.jp','s-cubism.jp','oaklawn.co.jp','dn.smbc.co.jp','hrm.nadai.jp','zeal-career.co.jp','higashi-nipponbank.jp','mufg.jp','escco.co.jp','diverta.co.jp','mizuhobank.co.jp','briscola.co.jp','wi2.co.jp','anicecompany.co.jp','w-design.co.jp','inctas.co.jp','totarotanaka.com','tandt1212.com','heartbeats.jp','naked.co.jp','tsunagu.info','yper.co.jp','vow-system.co.jp','47club.jp','ambient-co.jp','jp-md.co.jp','jwa.or.jp','tn-japan.co.jp','wics.co.jp','sankosc.co.jp','nmp-specialist.com','ksk-anl.com','musashino.jp','esteri.it','gmail.co','yohten.com','mail.dnp.co.jp','tokyo-chefs.jp','sbigroup.co.jp','dwango.co.jp','nii.ac.jp','bsy.jfe-eng.co.jp','villanova.edu','ksone.jp','iwanichi.co.jp','zicon.net','amperaxp.com','ims.u-tokyo.ac.jp','starkmind.co.jp','denen.com','life-book.co.jp','guitto.co.jp','hgc.jp','sbsnt.co.jp','fusenetwork.co.jp','blnk.co.jp','jp.fujitsu.com','huynq.net','broadleaf.co.jp','taishukan.co.jp','hackerx.org']
	#部分テスト用の小リスト
	#company_list = ['taishukan.co.jp','broadleaf.co.jp','automation.jp','sbigroup.co.jp','aijus.com','yper.co.jp','hubspot.com']
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

# アイコンのデータアドレスを書き換えようとした関数。hs_avatar_filemanager_keyがREAD_ONLY_VALUEのため書き換えられなかった。
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

# 各会社に手動で設定された画像データのURLを取得する関数。ただしhubspot側で自動設定されたものは取得できない
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
