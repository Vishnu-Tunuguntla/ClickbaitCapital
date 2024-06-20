from finvizfinance.screener.performance import Performance

fperf = Performance()
filters_dict = {'Performance': 'Today +10%', 'Performance 2': 'Today +10%', 'Change from Open': 'Up 20%'}  # Use a valid filter key
fperf.set_filter(filters_dict=filters_dict)
top_gainers_df = fperf.screener_view()

# Get the top 5 tickers
top_5_gainers = top_gainers_df['Ticker'].head(5).tolist()
print(top_5_gainers)
