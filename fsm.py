from transitions.extensions import GraphMachine
from bug import inputType, fetch_best, fetch_all, fetch_calc_best_sell, fetch_calc_best_buy, fetch_all_bank, fetch_bank_result, fetch_all_calc_bank, fetch_calc_spec_sell, fetch_calc_spec_buy

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.type = ""
        self.money = ""
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    # conditions
    def is_going_to_start(self, update):
        text = update.message.text
        return text.lower() == '/start' or text.lower() == 'start'

    def is_going_to_best(self, update):
        text = update.message.text
        return text.lower() == '/best' or text.lower() == 'best'

    def is_going_to_all(self, update):
        text = update.message.text
        self.type = ""
        return text.lower() == '/all' or text.lower() == 'all'
        
    def is_going_to_calc(self, update):
        text = update.message.text
        self.type = ""
        self.money = ""
        
        return text.lower() == '/calc' or text.lower() == 'calc'
        
    def is_going_to_about(self, update):
        text = update.message.text
        return text.lower() == '/about' or text.lower() == 'about'
        
    def is_going_to_bestRes(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        return int(text) > 0 and int(text) < 20
        
    def is_going_to_all_bank(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        self.type = text
        return int(text) > 0 and int(text) < 20
        
    def is_going_to_allRes(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        return int(text) >= 0 and int(text) < 39
        
    def is_going_to_help(self, update):
        text = update.message.text
        return text.lower() == '/help' or text.lower() == 'help'
        
    def is_going_to_explain(self, update):
        text = update.message.text
        return text.lower() == '/explain' or text.lower() == 'explain'
        
    def is_going_to_info(self, update):
        text = update.message.text
        return text.lower() == '/info' or text.lower() == 'info'
    
    # calc -- best
    def is_going_to_best_sell(self, update):
        text = update.message.text
        return text.lower() == '/best_sell' or text.lower() == 'best_sell'
    
    def is_going_to_best_buy(self, update):
        text = update.message.text
        return text.lower() == '/best_buy' or text.lower() == 'best_buy'
        
    def is_going_to_best_sellRes(self, update):
        text = update.message.text
        c1 = int(text[0:text.find(' ')]) > 0 and int(text[0:text.find(' ')]) < 20
        c2 = int(text[text.find(' ')+1:len(text)]) > 0
        return c1 and c2
        
    def is_going_to_best_buyRes(self, update):
        text = update.message.text
        c1 = int(text[0:text.find(' ')]) > 0 and int(text[0:text.find(' ')]) < 20
        c2 = int(text[text.find(' ')+1:len(text)]) > 0
        return c1 and c2
    
    # calc -- spec
    def is_going_to_spec_sell(self, update):
        text = update.message.text
        return text.lower() == '/spec_sell' or text.lower() == 'spec_sell'
    
    def is_going_to_spec_buy(self, update):
        text = update.message.text
        return text.lower() == '/spec_buy' or text.lower() == 'spec_buy'
        
    def is_going_to_spec_sell_bank(self, update):
        text = update.message.text
        c1 = int(text[0:text.find(' ')]) > 0 and int(text[0:text.find(' ')]) < 20
        c2 = int(text[text.find(' ')+1:len(text)]) > 0
        self.type = text[0:text.find(' ')]
        self.money = text[text.find(' ')+1:len(text)]
        return c1 and c2
        
    def is_going_to_spec_buy_bank(self, update):
        text = update.message.text
        c1 = int(text[0:text.find(' ')]) > 0 and int(text[0:text.find(' ')]) < 20
        c2 = int(text[text.find(' ')+1:len(text)]) > 0
        self.type = text[0:text.find(' ')]
        self.money = text[text.find(' ')+1:len(text)]
        return c1 and c2
        
    def is_going_to_spec_sellRes(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        return int(text) > 0 and int(text) < 39
        
    def is_going_to_spec_buyRes(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        return int(text) > 0 and int(text) < 39    
        
    
    # entering
    def on_enter_start(self, update):
	    update.message.reply_text("-- ExRate bot--\n 💰 查詢貨幣匯率與試算 💰\n/best - 查詢某貨幣最佳匯率\n/all - 查詢某貨幣某銀行之匯率\n/calc - 試算\n/about - 操作說明 & 關於本bot")

    def on_enter_best(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n/1 日幣 JPY 🇯🇵\n/2 美金 USD 🇺🇸\n/3 人民幣 CNY 🇨🇳\n/4 歐元 EUR 🇪🇺\n/5 港幣 HKD 🇭🇰\n/6 英鎊 GBP 🇬🇧\n/7 澳幣 AUD 🇦🇺\n/8 加拿大幣 CAD 🇨🇦\n/9 新家玻幣 SGD 🇸🇬\n/10 瑞士法郎 CHF 🇨🇭\n/11 瑞典幣 SEK 🇸🇪\n/12 泰幣 THB 🇹🇭\n/13 菲國比索 PHP 🇵🇭\n/14 印尼幣 IDR 🇮🇩\n/15 韓元 KRW 🇰🇷\n/16 越南盾 VND 🇻🇳\n/17 馬來幣 MYR 🇲🇾\n/18 紐元 NZD 🇳🇿\n/19 澳門幣 MOP 🇲🇴")
        
    def on_enter_bestRes(self, update):
        text = update.message.text
        first = str(text[0])
        if first == '/':
            text = text[1:len(text)]
        t = inputType(text)
        print(str(t));
        update.message.reply_text(fetch_best(t))
        self.go_back(update)
#    def on_exit_best(self, update):
#        print('Leaving state best')

    def on_enter_all(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n/1 日幣 JPY 🇯🇵\n/2 美金 USD 🇺🇸\n/3 人民幣 CNY 🇨🇳\n/4 歐元 EUR 🇪🇺\n/5 港幣 HKD 🇭🇰\n/6 英鎊 GBP 🇬🇧\n/7 澳幣 AUD 🇦🇺\n/8 加拿大幣 CAD 🇨🇦\n/9 新家玻幣 SGD 🇸🇬\n/10 瑞士法郎 CHF 🇨🇭\n/11 瑞典幣 SEK 🇸🇪\n/12 泰幣 THB 🇹🇭\n/13 菲國比索 PHP 🇵🇭\n/14 印尼幣 IDR 🇮🇩\n/15 韓元 KRW 🇰🇷\n/16 越南盾 VND 🇻🇳\n/17 馬來幣 MYR 🇲🇾\n/18 紐元 NZD 🇳🇿\n/19 澳門幣 MOP 🇲🇴")
        
    def on_enter_all_bank(self, update):
        s = fetch_all_bank(self.type)
        update.message.reply_text("請輸入銀行代碼:\n/0 列出所有\n" + s)
        
    def on_enter_allRes(self, update):
        if update.message.text != "" and self.type != "":
            text = update.message.text
            first = str(text[0])
            if first == '/':
                text = text[1:len(text)]
            t = inputType(self.type)
            print(str(t));
            if text == '0':
                r = fetch_all(t)
                respon = ""
                for i in r:
                	respon += (i)
                	if(i != r[len(r)-1]):
                	    respon += "\n------------------\n"
                update.message.reply_text(respon)
                self.go_back(update)
            else:
                respon = fetch_bank_result(self.type, text)
                update.message.reply_text(respon)
                self.go_back(update)
            
            

#    def on_exit_all(self, update):
#        print('Leaving state all')
        
    def on_enter_calc(self, update):
        update.message.reply_text("--使用最佳匯率--\n/best_sell - 台幣換外幣\n/best_buy - 外幣換台幣\n\n--使用某銀行匯率--\n/spec_sell - 台幣換外幣\n/spec_buy - 外幣換台幣\n\n/start - 回主選單")
        
    def on_enter_calc_best_sell(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n1 日幣 JPY 🇯🇵\n2 美金 USD 🇺🇸\n3 人民幣 CNY 🇨🇳\n4 歐元 EUR 🇪🇺\n5 港幣 HKD 🇭🇰\n6 英鎊 GBP 🇬🇧\n7 澳幣 AUD 🇦🇺\n8 加拿大幣 CAD 🇨🇦\n9 新家玻幣 SGD 🇸🇬\n10 瑞士法郎 CHF 🇨🇭\n11 瑞典幣 SEK 🇸🇪\n12 泰幣 THB 🇹🇭\n13 菲國比索 PHP 🇵🇭\n14 印尼幣 IDR 🇮🇩\n15 韓元 KRW 🇰🇷\n16 越南盾 VND 🇻🇳\n17 馬來幣 MYR 🇲🇾\n18 紐元 NZD 🇳🇿\n19 澳門幣 MOP 🇲🇴\n\n請輸入先輸貨幣代碼再輸試算金額\n例如：台幣1000換日幣，則輸入：\n1 1000")
        
    def on_enter_calc_best_buy(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n1 日幣 JPY 🇯🇵\n2 美金 USD 🇺🇸\n3 人民幣 CNY 🇨🇳\n4 歐元 EUR 🇪🇺\n5 港幣 HKD 🇭🇰\n6 英鎊 GBP 🇬🇧\n7 澳幣 AUD 🇦🇺\n8 加拿大幣 CAD 🇨🇦\n9 新家玻幣 SGD 🇸🇬\n10 瑞士法郎 CHF 🇨🇭\n11 瑞典幣 SEK 🇸🇪\n12 泰幣 THB 🇹🇭\n13 菲國比索 PHP 🇵🇭\n14 印尼幣 IDR 🇮🇩\n15 韓元 KRW 🇰🇷\n16 越南盾 VND 🇻🇳\n17 馬來幣 MYR 🇲🇾\n18 紐元 NZD 🇳🇿\n19 澳門幣 MOP 🇲🇴\n\n請輸入先輸貨幣代碼再輸試算金額\n例如：日幣1000換台幣，則輸入：\n1 1000")
        
    def on_enter_calc_best_sellRes(self, update):
        text = update.message.text
        t = inputType(text[0:text.find(' ')])
        money = text[text.find(' ')+1:len(text)]
        print(str(t));
        update.message.reply_text(fetch_calc_best_sell(t, money))
        self.go_calc(update);
    
    def on_enter_calc_best_buyRes(self, update):
        text = update.message.text
        t = inputType(text[0:text.find(' ')])
        money = text[text.find(' ')+1:len(text)]
        print(str(t));
        update.message.reply_text(fetch_calc_best_buy(t, money))
        self.go_calc(update);
        
    def on_enter_calc_spec_sell(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n1 日幣 JPY 🇯🇵\n2 美金 USD 🇺🇸\n3 人民幣 CNY 🇨🇳\n4 歐元 EUR 🇪🇺\n5 港幣 HKD 🇭🇰\n6 英鎊 GBP 🇬🇧\n7 澳幣 AUD 🇦🇺\n8 加拿大幣 CAD 🇨🇦\n9 新家玻幣 SGD 🇸🇬\n10 瑞士法郎 CHF 🇨🇭\n11 瑞典幣 SEK 🇸🇪\n12 泰幣 THB 🇹🇭\n13 菲國比索 PHP 🇵🇭\n14 印尼幣 IDR 🇮🇩\n15 韓元 KRW 🇰🇷\n16 越南盾 VND 🇻🇳\n17 馬來幣 MYR 🇲🇾\n18 紐元 NZD 🇳🇿\n19 澳門幣 MOP 🇲🇴\n\n請輸入先輸貨幣代碼再輸試算金額\n例如：台幣1000換日幣，則輸入：\n1 1000")
        
    def on_enter_calc_spec_buy(self, update):
        update.message.reply_text("請輸入貨幣代碼:\n1 日幣 JPY 🇯🇵\n2 美金 USD 🇺🇸\n3 人民幣 CNY 🇨🇳\n4 歐元 EUR 🇪🇺\n5 港幣 HKD 🇭🇰\n6 英鎊 GBP 🇬🇧\n7 澳幣 AUD 🇦🇺\n8 加拿大幣 CAD 🇨🇦\n9 新家玻幣 SGD 🇸🇬\n10 瑞士法郎 CHF 🇨🇭\n11 瑞典幣 SEK 🇸🇪\n12 泰幣 THB 🇹🇭\n13 菲國比索 PHP 🇵🇭\n14 印尼幣 IDR 🇮🇩\n15 韓元 KRW 🇰🇷\n16 越南盾 VND 🇻🇳\n17 馬來幣 MYR 🇲🇾\n18 紐元 NZD 🇳🇿\n19 澳門幣 MOP 🇲🇴\n\n請輸入先輸貨幣代碼再輸試算金額\n例如：日幣1000換台幣，則輸入：\n1 1000")
        
    def on_enter_calc_spec_sell_bank(self, update):
        s = fetch_all_calc_bank(self.type)
        update.message.reply_text("請輸入銀行代碼:\n" + s)
    
    def on_enter_calc_spec_buy_bank(self, update):
        s = fetch_all_calc_bank(self.type)
        update.message.reply_text("請輸入銀行代碼:\n" + s)
        
    def on_enter_calc_spec_sellRes(self, update):
        if update.message.text != "" and self.type != "":
            text = update.message.text
            first = str(text[0])
            if first == '/':
                text = text[1:len(text)]
            t = inputType(self.type)
            print(str(t), type(int(text)));
            respon = fetch_calc_spec_sell(self.type, text, self.money)
            update.message.reply_text(respon)
            self.go_calc(update)
            
    def on_enter_calc_spec_buyRes(self, update):
        if update.message.text != "" and self.type != "":
            text = update.message.text
            first = str(text[0])
            if first == '/':
                text = text[1:len(text)]
            t = inputType(self.type)
            print(str(t));
            respon = fetch_calc_spec_buy(self.type, text, self.money)
            update.message.reply_text(respon)
            self.go_calc(update)

#    def on_exit_calc(self, update):
#        print('Leaving state calc')
        
    def on_enter_about(self, update):
        update.message.reply_text("/help - 使用說明\n/explain - 匯率名詞解釋\n/info - Bot資訊\n/start - 回到主選單")
        
    def on_enter_help(self, update):
        update.message.reply_text("在任何時候打上 /start 都能回到選單，若機器人卡住可使用以上方法。\n\n若有任何建議與問題，歡迎回報至：\nsusan31213@gmail.com")
        self.go_about(update)
        
    def on_enter_explain(self, update):
        update.message.reply_text("銀行的匯率牌告，會有四種價位，「現金買入」「即期買入」「即期賣出」「現金賣出」，就針對以上四個匯率，做出解釋：\n銀行牌告中的「買入」、「賣岀」匯率皆是以銀行角度來看。\n\n現金匯率：兌換成貨幣現金、現鈔的價格。價格會比較貴一點，因為銀行還有保管外幣的成本。\n即期匯率：兌換成貨幣存款（存摺）或旅行支票的價格。\n\n------------------------\n\n現金買入：是銀行以新台幣跟您買（換）外幣現鈔的價格，通常這是四個價位當中最低的價格，因為銀行持有外幣現鈔有其一定的持有成本，因此便反映在匯率上面。\n一般通常是用在出國回來之後手上有外幣現鈔沒用完，要換回新台幣時。兌換時找價格最高的銀行更划算。\n\n現金賣出：是您拿新台幣跟銀行買（換）外幣現鈔的價格，這是四個價位當中最高的。\n像出國要換外幣，就是以這個價格換一單位的外幣。兌換時找價格最低的銀行更划算。\n\n即期買入：是銀行以新台幣跟您買（換）外幣的價格，通常這是四個價位當中次低的價格。\n一般通常會用到的情況，就是外幣帳戶存款要轉存成新台幣帳戶存款，或是有收到一筆外幣的匯款要轉成新台幣，或是外幣計價的基金要贖回，也是看這個匯率。\n\n即期賣岀：是您拿新台幣跟銀行買（換）外幣時候的價格，通常是四個價位當中次高的。\n一般通常會用到的情況，是新台幣要轉存外幣存款，或是要外幣匯款時，都是看這個價格。\n\n------------------------\n參考資料: http://www.findrate.tw/glossary.html")
        self.go_about(update)
        
    def on_enter_info(self, update):
        update.message.reply_text("Author: Susan Su\n\n資料來源：比率網 http://www.findrate.tw/\n\n本Bot提供之資料僅供參考\n若有任何建議與問題，歡迎回報至：\nsusan31213@gmail.com")
        self.go_about(update)
#    def on_exit_about(self, update):
#        print('Leaving state about')
