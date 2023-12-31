import requests
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def get_trading_data(stockcode):
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30)
    start_date_str = start_date.strftime('%d/%m/%Y')

    url = 'https://finance.vietstock.vn/data/gettradingresult'

    headers = {
        'Host': 'finance.vietstock.vn',
        'Cookie': 'language=vi-VN; Theme=Light; _pbjs_userid_consent_data=3524755945110770; _ga_EXMM0DKVEX=GS1.1.1703145769.7.1.1703146102.59.0.0; _ga=GA1.2.1214440855.1702969900; isShowLogin=true; dable_uid=undefined; AnonymousNotification=; _gid=GA1.2.1021456504.1702969902; __gads=ID=6a033cef9391c91c:T=1702969902:RT=1703146104:S=ALNI_MYzdS6dPNGfckZ4OaQtChqHoXPncw; __gpi=UID=00000cb6097d797e:T=1702969902:RT=1703146104:S=ALNI_MZcM5VnjaxQIehzhw9mpNHSJMViBA; cto_bundle=sjP2NV8xbjdkWEV4WjlGJTJGQWpRbmI0OUk2Q2xYZEhtTW1MZ21LcHdqQmpVUWI3NkZJNnJTRTVGUWZocFFheG03S21wUm9IR3lzYm5RQnNrdnBpTnV2ZDVsayUyQldVTFBRMWo1N2l3VDJkdHJOdXprOGJEVzBXZThDTHd5RWpvY2VNdzMlMkZwMWlrTGNzZlE1RnJ1c013czJ5ZVB0WEElM0QlM0Q; cto_bidid=tBZe6181clRZTkh1TUVhbWVxZlR4UFZ4U0cyMGlXVFNES3ZINTNvQ3huQnJOYVpSMzk3SEFNcHROV2dmcDhmQmZENEJmT0ltUzgxV0dyTnYzZVhuM0d2bjdiOUk3RzdGdkFjVGhja0UyNnpXOFdkZyUzRA; cto_dna_bundle=xwZ0SF8xbjdkWEV4WjlGJTJGQWpRbmI0OUk2Q2tkWjlMZEd5dER3c3VteXh2JTJCeHBkN0p1RWZyTlZzOEdiUU02aWtCNDJJMFFzeGtUQktYV3haMkNMR2hLU0ltV0ElM0QlM0Q; ASP.NET_SessionId=kxqfhim3w1m1xc50xnxsnj5k; __RequestVerificationToken=feSyicPujrXC7o04c_qni_DuDxv91ghjnlZo3Zb0wSorUggkxWuIeZLtcjLAaeQdTU4S7ZY8i0s3tALkj8DmfplRWg-hWH3Qcxn8MAmziko1; finance_viewedstock=HPG',  
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    }

    data = {
        'Code': stockcode,
        'OrderBy': '',
        'OrderDirection': 'desc',
        'PageIndex': '1',
        'PageSize': '30',
        'FromDate': start_date_str,
        'ToDate': current_date,
        'ExportType': 'default',
        'Cols': 'TKLGD,TGTGD,VHTT,TGG,DC,TGPTG,KLGDKL,GTGDKL',
        'ExchangeID': '1',
        '__RequestVerificationToken': 'WcpGXmYqtiiNjIcvN25UeW53XDTWYW6A1dS_33XTuMnj56BKNmdRvJEOPzWvKm_E-VcolXbJRaFELvsVxMEm1DyILQX_X0fivTP0dQxW62U1'
    }

    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()

    return response, response_json

def save_trading_data_to_csv(response_json, output_filepath):
    if "Data" in response_json and len(response_json["Data"]) > 0:
        with open(output_filepath, 'a', newline='') as csvfile:
            fieldnames = ['StockCode', 'Trading Date', 'Close Price']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csv_writer.writeheader()
            for i in range(len(response_json["Data"])):
                stockcode = response_json["Data"][i]["StockCode"]
                close_price = str(response_json["Data"][i]["ClosePrice"])
                trading_date_str = response_json["Data"][i]["TradingDate"]

                timestamp_ms = int(trading_date_str[6:-2]) 
                trading_date_iso = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%d/%m/%Y')

                csv_writer.writerow({'StockCode': stockcode, 'Trading Date': trading_date_iso, 'Close Price': close_price})

                print(f"{trading_date_iso}: {close_price}")

        print(f"Data saved to {output_filepath}")
    else:
        print(f"No trading data found for stock code {stockcode}")

def plot_trading_data(stockcode, date, price):
    if date and price:
        fig, ax = plt.subplots()
        ax.plot_date(date, price, '-', color='cyan')
        ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
        plt.xticks(rotation=45, color='red')
        plt.yticks(color='red')
        plt.title(f"Stock Price of {stockcode}")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.tight_layout()
        plt.show()
    else:
        print(f"No data to plot for stock code {stockcode}")

if __name__  == "__main__":  
    url = 'https://finance.vietstock.vn/data/gettradingresult'

    stockcode_input = input("Input stock code: ")

    output_file_path = "/home/guardian/personal/python/tools/CrawlDataVietstock/Trading_data.csv"

    response, response_json = get_trading_data(stockcode_input)
    date = []
    price = []
    if "Data" in response_json and len(response_json["Data"]) > 0:
        for i in range(len(response_json["Data"])):
            close_price = str(response_json["Data"][i]["ClosePrice"])
            trading_date_str = response_json["Data"][i]["TradingDate"]

            timestamp_ms = int(trading_date_str[6:-2]) 
            trading_date_iso = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%d/%m/%Y')

            print(f"{trading_date_iso}: {close_price}")

            date.append(datetime.strptime(trading_date_iso, '%d/%m/%Y'))
            price.append(float(close_price.replace(',', '')))

        save_trading_data_to_csv(response_json, output_file_path)
        plot_trading_data(stockcode_input, date, price)
    else:
        print(f"No trading data found for stock code {stockcode_input}")
