import requests

USDT_list = []
list_meet = []

def get_all_info():
    USDT_list = []
    # 獲取全部幣種訊息
    exchange_info = "https://api.binance.com/api/v1/exchangeInfo"
    exchange_info_resp = requests.get(exchange_info).json()
    # 檢查交易對是否交易中
    for symbol in exchange_info_resp['symbols']:
        if symbol["status"] == "TRADING":
            if "USDT" in symbol['symbol']:
                USDT_list.append(symbol['symbol'])
    # 過濾up,down代幣
    up_fil = list(filter(lambda x: "UP" in x, USDT_list))
    down_fil = list(filter(lambda x: "DOWN" in x, USDT_list))
    for i in down_fil:
        up_fil.append(i)
    for i in up_fil:
        USDT_list.remove(i)
    return USDT_list





# 輸入持倉量狀況（正數），多空比狀況（正數）
# Ex. 想搜尋持倉量上升20% 多空比下降20%的幣種
# start(20,20)
def start(Postition, Lsr):
    lst = get_all_info()
    print(lst)
    for i in range(len(lst)):
        try:
            # 抓取資料:持倉變化、多空比、資金費率
            symbol = lst[i]
            op = f'https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=1h&limit=8'
            op_resp = requests.get(op).json()
            lsr = f'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}&period=1h&limit=8'
            lsr_resp = requests.get(lsr).json()
            funding_rate = f'https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1'
            fdr_resp = requests.get(funding_rate).json()

            # 計算持倉變化
            op_change = (
                            float(op_resp[7]['sumOpenInterestValue']) - float(
                            op_resp[0]['sumOpenInterestValue'])
                        ) / float(op_resp[0]['sumOpenInterestValue'])
            op_change_ = float('%.2f' % op_change)
            op_100 = round(op_change_ * 100, 1)

            # 計算多空比變化
            lsr_change = (
                             float(lsr_resp[7]['longShortRatio']) - float(lsr_resp[0]['longShortRatio'])
                         ) / float(lsr_resp[0]['longShortRatio'])
            lsr_change_ = float('%.2f' % lsr_change)
            lsr_100 = round(lsr_change_ * 100, 1)

            #  持倉量/1million
            op_divided = float(op_resp[0]['sumOpenInterestValue']) / 1000000
            op_divided_ = float(op_resp[7]['sumOpenInterestValue']) / 1000000

            # 資金費率
            fd = float(fdr_resp[0]['fundingRate']) * 100

            # 列出 幣種、持倉變化、多空比（皆為跟八小時前比））目前資金費率
            print(symbol, op_100,"%", lsr_100,"%", fd,"%")
            if op_100 > Postition and lsr_100 < -Lsr:
                list_meet.append(symbol)
        except:
            pass
    # 符合條件的幣種
    print(list_meet)
