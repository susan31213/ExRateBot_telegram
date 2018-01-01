import requests 
from bs4 import BeautifulSoup

d_curr = {1:"http://www.findrate.tw/JPY/", 2:"http://www.findrate.tw/USD/", 3:"http://www.findrate.tw/CNY/", 4:"http://www.findrate.tw/EUR/", 5:"http://www.findrate.tw/HKD/", 6:"http://www.findrate.tw/GBP/", 7:"http://www.findrate.tw/AUD/", 8:"http://www.findrate.tw/CAD/",9:"http://www.findrate.tw/SGD/", 10:"http://www.findrate.tw/CHF/",11:"http://www.findrate.tw/SEK/",12:"http://www.findrate.tw/THB/", 13:"http://www.findrate.tw/PHP/", 14:"http://www.findrate.tw/IDR/", 15:"http://www.findrate.tw/KRW/", 16:"http://www.findrate.tw/VND/", 17:"http://www.findrate.tw/MYR/", 18:"http://www.findrate.tw/NZD/", 19:"http://www.findrate.tw/MOP/"}
d_curr_name = {1: "日幣", 2:"美金", 3:"人民幣", 4:"歐元", 5:"港幣", 6:"英鎊", 7:"澳幣", 8:"加拿大幣", 9:"新家玻幣", 10:"瑞士法郎", 11:"瑞典幣", 12:"泰幣", 13:"菲國比索", 14:"印尼幣", 15:"韓元", 16:"越南盾", 17:"馬來幣", 18:"紐元", 19:"澳門幣"}

def inputType(x):
#	print("1.日幣 JPY\n2.美金 USD\n3.人民幣 CNY\n4.歐元 EUR\n5.港幣 HKD\n6.英鎊 GBP\n7.澳幣 AUD\n8.加拿大幣 CAD\n9.新家玻幣 SGD\n10.瑞士法郎 CHF\n11.瑞典幣 SEK\n12.泰幣 THB\n13.菲國比索 PHP\n14.印尼幣 IDR\n15.韓元 KRW\n16.越南盾 VND\n17.馬來幣 MYR\n18.紐元 NZD\n19.澳門幣 MOP\n")
	if int(x) > 0 and int(x) < 20:
		if x == '1' or x == 'JPY':
			return [1, '日幣']
		elif x == '2' or x == "USD":
			return [2, '美金']
		elif x == '3' or x == "CNY":
			return [3, '人民幣']
		elif x == '4' or x == "EUR":
			return [4, '歐元']
		elif x == '5' or x == "HKD":
			return [5, '港幣']
		elif x == '6' or x == "GBP":
			return [6, '英鎊']
		elif x == '7' or x == "AUD":
			return [7, '澳幣']
		elif x == '8' or x == "CAD":
			return [8, '加拿大幣']
		elif x == '9' or x == "SGD":
			return [9, '新家玻幣']
		elif x == '10' or x == "CHF":
			return [10, '瑞士法郎']
		elif x == '11' or x == "SEK":
			return [11, '瑞典幣']
		elif x == '12' or x == "THB":
			return [12, '泰幣']
		elif x == '13' or x == "PHP":
			return [13, '菲國比索']
		elif x == '14' or x == "IDR":
			return [14, '印尼幣']
		elif x == '15' or x == "KRW":
			return [15, '韓元']
		elif x == '16' or x == "VND":
			return [16, '越南盾']
		elif x == '17' or x == "MYR":
			return [17, '馬來幣']
		elif x == '18' or x == "INR":
			return [18, '紐元']
		elif x == '19' or x == "DKK":
			return [19, '澳門幣']
	else:
		return -1
			
def fetch_best(i):	
	request = requests.get(d_curr[i[0]])
	soup = BeautifulSoup(request.content, "html.parser")
	
	# Best
	sell_set = soup.find_all('table')[0].find_all('tr')[1].find_all('td')
	buy_set = soup.find_all('table')[0].find_all('tr')[2].find_all('td')

	# bank & 匯率
	sell = sell_set[1].get_text()
	sell_price = sell_set[2].get_text()
	buy = buy_set[1].get_text()
	buy_price = buy_set[2].get_text()
	return str("台幣 -> " + i[1] + "\n最佳匯率銀行： " + sell + " " + sell_price + '\n\n' + i[1] + " -> 台幣" + "\n最佳匯率銀行： " + buy + " " + buy_price)

def fetch_all(i):
	request = requests.get(d_curr[i[0]])
	soup = BeautifulSoup(request.content, "html.parser")

	# All bank
	res = []
	all_set = soup.find_all('tbody')[1].find_all('td')
	for k in range(0, len(all_set), 7):
		data = ""
		data += str(int(k/7+1)) + ". " + all_set[k].get_text()[0:all_set[k].get_text().find('\n')] + "\n"
		data += "現鈔買入： " + all_set[k+1].get_text() + "\n"
		data += "現鈔賣出： " + all_set[k+2].get_text() + "\n"
		data += "即期買入： " + all_set[k+3].get_text() + "\n"
		data += "即期賣出： " + all_set[k+4].get_text() + "\n"
		data += "更新時間： " + all_set[k+5].get_text() + "\n"
		if all_set[k+6].get_text().find('提交數據') == -1:
			data += "　手續費：" + all_set[k+6].get_text()
		else:
			data += "　手續費： 請洽尋銀行"
		res.append(data)
	return res
	
def fetch_all_bank(num):
	request = requests.get(d_curr[int(num)])
	soup = BeautifulSoup(request.content, "html.parser")
	all_set = soup.find_all('tbody')[1].find_all('td')
	res = ""
	for k in range(0, len(all_set), 1):
		case = k % 7
		if case == 0:
			res += "/" + str(int(k/7+1)) + " " + all_set[k].get_text()[0:all_set[k].get_text().find('\n')] + "\n"

	return res

def fetch_bank_result(num, bank):
	request = requests.get(d_curr[int(num)])
	soup = BeautifulSoup(request.content, "html.parser")
	all_set = soup.find_all('tbody')[1].find_all('td')
	k = 7*(int(bank) - 1)
	data = ""
	data += all_set[k].get_text()[0:all_set[k].get_text().find('\n')] + "\n"
	data += "現鈔買入： " + all_set[k+1].get_text() + "\n"
	data += "現鈔賣出： " + all_set[k+2].get_text() + "\n"
	data += "即期買入： " + all_set[k+3].get_text() + "\n"
	data += "即期賣出： " + all_set[k+4].get_text() + "\n"
	data += "更新時間： " + all_set[k+5].get_text() + "\n"
	if all_set[k+6].get_text().find('提交數據') == -1:
		data += "　手續費：" + all_set[k+6].get_text()
	else:
		data += "　手續費： 請洽尋銀行"
	return data
	
def fetch_calc_best_sell(i, money):
	request = requests.get(d_curr[i[0]])
	soup = BeautifulSoup(request.content, "html.parser")
	sell_set = soup.find_all('table')[0].find_all('tr')[1].find_all('td')
			
	# bank & 匯率
	data = ""
	sell = sell_set[1].get_text()
	sell_price = float(sell_set[2].get_text())
	result = int(float(money) / sell_price)
	data += "\n$" + money + " 台幣可換 $" + str(result) + " " + i[1] + "\nin " + sell + " 匯率為： " + str(sell_price) + "\n"
	
	# 手續費
	all_set = soup.find_all('tbody')[1].find_all('td')
	for k in range(0, len(all_set), 1):
		case = k % 7
		if case == 0 and all_set[k].get_text().find(sell) != -1:
			data += "\n********************************\n" + "\n"
			data += " 此為不計入手續費情況下之結果" + "\n"
			if all_set[k+6].get_text().find('提交數據') == -1:
				data += " 交易手續費情況：" + all_set[k+6].get_text() + "\n"
			else:
				data += " 交易手續費情況： 請洽尋銀行" + "\n"
			data += "\n********************************\n"
			break
	return data
	
def fetch_calc_best_buy(i, money):
	request = requests.get(d_curr[i[0]])
	soup = BeautifulSoup(request.content, "html.parser")
	buy_set = soup.find_all('table')[0].find_all('tr')[2].find_all('td')
	
	# bank & 匯率
	data = ""
	buy = buy_set[1].get_text()
	buy_price = float(buy_set[2].get_text())
	result = int(float(money) * buy_price)
	data += "\n$" + money + " " + i[1] + "可換 $" + str(result) + " 台幣\nin " + buy + " 匯率為： " + str(buy_price) + "\n"
	
	# 手續費
	all_set = soup.find_all('tbody')[1].find_all('td')
	for k in range(0, len(all_set), 1):
		case = k % 7
		if case == 0 and all_set[k].get_text().find(buy) != -1:
			data += "\n********************************\n" + "\n"
			data += " 此為不計入手續費情況下之結果" + "\n"
			if all_set[k+6].get_text().find('提交數據') == -1:
				data += " 交易手續費情況：" + all_set[k+6].get_text() + "\n"
			else:
				data += " 交易手續費情況： 請洽尋銀行" + "\n"
			data += "\n********************************\n"
			break
	return data

def fetch_all_calc_bank(num):
	request = requests.get(d_curr[int(num)])
	soup = BeautifulSoup(request.content, "html.parser")
	all_set = soup.find_all('tbody')[1].find_all('td')
	res = ""
	for k in range(0, len(all_set), 1):
		case = k % 7
		if case == 0 and all_set[k+2].get_text().find('--') == -1:
			res += "/" + str(int(k/7+1)) + " " + all_set[k].get_text()[0:all_set[k].get_text().find('\n')] + "\n"
	return res

def fetch_calc_spec_sell(num, k, money):
	request = requests.get(d_curr[int(num)])
	soup = BeautifulSoup(request.content, "html.parser")
	all_set = soup.find_all('tbody')[1].find_all('td')
	bank = int(k) - 1
	name = all_set[7*bank].get_text()[0:all_set[7*bank].get_text().find('\n')]
	sell_price = float(all_set[7*bank+2].get_text())
	result = int(float(money) / sell_price)
	data = ("$" + money + " 台幣可換 $" + str(result) + " " + d_curr_name[int(num)] + "\nin " + name + " 匯率為： " + str(sell_price))
	data += "\n********************************\n" + "\n"
	data += " 此為不計入手續費情況下之結果" + "\n"
	if all_set[7*bank+6].get_text().find('提交數據') == -1:
		data += " 交易手續費情況：" + all_set[7*bank+6].get_text() + "\n"
	else:
		data += " 交易手續費情況： 請洽尋銀行" + "\n"
	data += "\n********************************\n"
	return data
	
def fetch_calc_spec_buy(num, k, money):
	request = requests.get(d_curr[int(num)])
	soup = BeautifulSoup(request.content, "html.parser")
	all_set = soup.find_all('tbody')[1].find_all('td')
	bank = int(k) - 1
	name = all_set[7*bank].get_text()[0:all_set[7*bank].get_text().find('\n')]
	buy_price = float(all_set[7*bank+1].get_text())
	result = int(float(money) * buy_price)
	data = ("$" + money + " " + d_curr_name[int(num)] + "可換 $" + str(result) + " 台幣\nin " + name + " 匯率為： " + str(buy_price))
	data += "\n********************************\n" + "\n"
	data += " 此為不計入手續費情況下之結果" + "\n"
	if all_set[7*bank+6].get_text().find('提交數據') == -1:
		data += " 交易手續費情況：" + all_set[7*bank+6].get_text() + "\n"
	else:
		data += " 交易手續費情況： 請洽尋銀行" + "\n"
	data += "\n********************************\n"
	return data

def fetch_calc(i, money):
	# Calculate
	_dir = input(">>> (1) 台幣換" + i[1] + "  (2) " + i[1] + "換台幣? ")
	method = input(">>> (1) Calculate with best exchange rate  (2) Calculate with specific bank? ")
	money = input(">>> How much do you want to exchange? ")
	
	# Best bank
	if method == '1':
		
		# TWD -> ???
		if _dir == '1':
			sell_set = soup.find_all('table')[0].find_all('tr')[1].find_all('td')
			
			# bank & 匯率
			sell = sell_set[1].get_text()
			sell_price = float(sell_set[2].get_text())
			result = int(float(money) / sell_price)
			print(money + " 台幣可換 " + str(result) + " " + i[1] + " in " + sell + " 匯率為： " + str(sell_price))
			
			# 手續費
			all_set = soup.find_all('tbody')[1].find_all('td')
			for k in range(0, len(all_set), 1):
				case = k % 7
				if case == 0 and all_set[k].get_text().find(sell) != -1:
					print("\n********************************\n")
					print(" 此為不計入手續費情況下之結果")
					if all_set[k+6].get_text().find('提交數據') == -1:
						print(" 交易手續費情況：" + all_set[k+6].get_text())
					else:
						print(" 交易手續費情況： 請洽尋銀行")
					print("\n********************************\n")
					break
				
		
		# ??? -> TWD
		elif _dir == '2':
			buy_set = soup.find_all('table')[0].find_all('tr')[2].find_all('td')
			buy = buy_set[1].get_text()
			buy_price = float(buy_set[2].get_text())
			result = int(float(money) * buy_price)
			print(money + " " + i[1] + "可換 " + str(result) + " 台幣 in " + buy + " 匯率為： " + str(buy_price))
			
			# 手續費
			all_set = soup.find_all('tbody')[1].find_all('td')
			for k in range(0, len(all_set), 1):
				case = k % 7
				if case == 0 and all_set[k].get_text().find(buy) != -1:
					print("\n********************************\n")
					print(" 此為不計入手續費情況下之結果")
					if all_set[k+6].get_text().find('提交數據') == -1:
						print(" 交易手續費情況：" + all_set[k+6].get_text())
					else:
						print(" 交易手續費情況： 請洽尋銀行")
					print("\n********************************\n")
					break
	# Specific bank
	elif method == '2':
		all_set = soup.find_all('tbody')[1].find_all('td')
		print("--------------------------------")
		for k in range(0, len(all_set), 1):
			case = k % 7
			if case == 0 and all_set[k+2].get_text().find('--') == -1:
				print(str(int(k/7+1)) + ". " + all_set[k].get_text()[0:all_set[k].get_text().find('\n')])
		bank = int(input(">>> 請選擇育查詢之銀行號碼: ")) - 1
		name = all_set[7*bank].get_text()[0:all_set[k].get_text().find('\n')]
		print("--------------------------------")
		
		# TWD -> ???
		if _dir == '1':
			sell_price = float(all_set[7*bank+2].get_text())
			result = int(float(money) / sell_price)
			print(money + " 台幣可換 " + str(result) + " " + i[1] + " in " + name + " 匯率為： " + str(sell_price))
		# ??? -> TWD	
		elif _dir == '2':
			buy_price = float(all_set[7*bank+1].get_text())
			result = int(float(money) * buy_price)
			print(money + " " + i[1] + "可換 " + str(result) + " 台幣 in " + name + " 匯率為： " + str(buy_price))
		print("\n********************************\n")
		print(" 此為不計入手續費情況下之結果")
		if all_set[7*bank+6].get_text().find('提交數據') == -1:
			print(" 交易手續費情況：" + all_set[7*bank+6].get_text())
		else:
			print(" 交易手續費情況： 請洽尋銀行")
		print("\n********************************\n")
		
#about_section()
#while (True):
#	x = input(">>> currency: ")
#	typenum = inputType(x)
##	print(fetch_best(typenum))
#	print(typenum[1] + " 各家銀行匯率列表")
#	r = fetch_all(typenum)
#	for i in r:
#		print(i)
#mode = input("(1) Best (2) All (3) Calculate, Input mode: ");
#if typenum != -1 and (mode == '1' or mode == '2' or mode == '3'):
#	fetch_data(typenum, mode)
#else:
#	print('Invaild no.\n')
