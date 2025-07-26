from flask import Flask, request, render_template
import yfinance as yf

app = Flask(__name__)

# Rule-based finance chatbot
def get_financial_response(user_input):
    user_input = user_input.lower()

    # Check for ticker
    tickers = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'AMZN', 'META', 'NVDA']
    for ticker in tickers:
        if ticker.lower() in user_input:
            stock = yf.Ticker(ticker)

            if "price" in user_input or "current" in user_input:
                price = stock.info.get("currentPrice", "N/A")
                return f"The current price of {ticker} is ${price}"

            elif "market cap" in user_input:
                market_cap = stock.info.get("marketCap", "N/A")
                return f"The market cap of {ticker} is ${market_cap:,}"

            elif "history" in user_input or "historical" in user_input:
                hist = stock.history(period="5d")
                return hist.to_string()

            else:
                return f"What would you like to know about {ticker}? (price, market cap, history?)"

    # General finance advice
    if "save" in user_input:
        return "Try to save at least 20% of your income monthly."

    elif "invest" in user_input:
        return "Diversify your investments. Consider index funds or ETFs for long-term growth."

    elif "budget" in user_input:
        return "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings."

    return "Sorry, I didn't understand that. Try asking about stock prices or saving/investing tips."

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_financial_response(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
