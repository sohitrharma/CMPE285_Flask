from flask import Flask, request, render_template
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_info = None
    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        stock_info = get_stock_info(symbol)
    return render_template('index.html', info=stock_info)

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_datetime = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        company_name = info.get('longName', 'N/A')
        stock_price = info.get('currentPrice', 'N/A')
        previous_close = info.get('previousClose', 'N/A')

        if isinstance(stock_price, (int, float)) and isinstance(previous_close, (int, float)):
            change = stock_price - previous_close
            percent_change = (change / previous_close) * 100 if previous_close != 0 else 'N/A'
        else:
            change = percent_change = 'N/A'

        change_str = f"{'+' if change >= 0 else ''}{change:.2f}" if isinstance(change, (int, float)) else "N/A"
        percent_change_str = f"{'+' if percent_change >= 0 else ''}{percent_change:.2f}%" if isinstance(percent_change, (int, float)) else "N/A"

        return {
            'date': current_datetime,
            'company': company_name,
            'price': stock_price,
            'change': change_str,
            'percent_change': percent_change_str
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
