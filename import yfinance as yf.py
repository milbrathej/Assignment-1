import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Fetch historical data for Microsoft
msft = yf.Ticker("MSFT")
hist = msft.history(period="10y")

# Calculate moving averages
hist['MA50'] = hist['Close'].rolling(window=50).mean()
hist['MA200'] = hist['Close'].rolling(window=200).mean()

# Define colors for candlesticks
colors = {True: 'green', False: 'red'}

# Plotting candlestick chart
fig, ax = plt.subplots()
ax.set_title('Microsoft Stock Price with Moving Averages')
ax.set_xlabel('Date')
ax.set_ylabel('Price')

# Plotting candlesticks
for date, vals in hist.iterrows():
    color = colors[vals['Close'] > vals['Open']]
    ax.plot([mdates.date2num(date), mdates.date2num(date)], [vals['Low'], vals['High']], color=color)
    ax.plot([mdates.date2num(date) - 0.2, mdates.date2num(date) + 0.2], [vals['Open'], vals['Open']], color=color)
    ax.plot([mdates.date2num(date) - 0.2, mdates.date2num(date) + 0.2], [vals['Close'], vals['Close']], color=color)

# Plotting moving averages
ax.plot(hist.index, hist['MA50'], color='blue', label='50-Day Moving Average')
ax.plot(hist.index, hist['MA200'], color='red', label='200-Day Moving Average')

# Annotation for crossover points
for i in range(1, len(hist)):
    if hist['MA50'][i] > hist['MA200'][i] and hist['MA50'][i - 1] <= hist['MA200'][i - 1]:
        ax.annotate('Golden Cross', xy=(hist.index[i], hist['MA50'][i]), xytext=(-30, 20), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    elif hist['MA50'][i] < hist['MA200'][i] and hist['MA50'][i - 1] >= hist['MA200'][i - 1]:
        ax.annotate('Death Cross', xy=(hist.index[i], hist['MA50'][i]), xytext=(-30, -20), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# Format x-axis
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Add legend
ax.legend()

plt.show()
