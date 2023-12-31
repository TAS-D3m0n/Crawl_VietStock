from datetime import datetime, timedelta
from CrawlDone import get_trading_data, plot_trading_data, save_trading_data_to_csv

#input for stock code
stockcode_input = input("Input stock code: ")
#get trading data
respone, response_json = get_trading_data(stockcode=stockcode_input)

#Get trding data function
get_trading_data(stockcode=stockcode_input)
# print(get_trading_data(stockcode=stockcode_input))

#Save trading data to csv function 
output_file_path = "D:\\sd\\personal\\python\\tools\\CrawlVietStock\\Trading_data.csv"
save_trading_data_to_csv(response_json=response_json,output_filepath=output_file_path)

#Plot trading data function
date = []
price = []
if "Data" in response_json and len(response_json["Data"]) > 0:
    for data in response_json["Data"]:
        trading_date_str = data["TradingDate"]
        close_price = str(data["ClosePrice"])
        timestamp_ms = int(trading_date_str[6:-2]) 
        trading_date_iso = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%d/%m/%Y')
        date.append(datetime.strptime(trading_date_iso, '%d/%m/%Y'))
        price.append(float(close_price.replace(',', '')))
plot_trading_data(stockcode=stockcode_input, date=date, price=price)