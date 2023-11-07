import ccxt
from tqdm import tqdm  # Import tqdm for the progress bar

# Define the list of the five most popular exchanges
popular_exchanges = ['binance', 'coinbasepro', 'kraken', 'bitstamp', 'bitfinex']

# Create a list to store arbitrage opportunities
arbitrage_opportunities = []

# Create a progress bar for the loops
progress_bar = tqdm(total=len(popular_exchanges)**3, desc="Scanning Markets")

# Initialize a dictionary to store exchange instances
exchange_instances = {}

# Initialize exchange instances for the five popular exchanges
for exchange_name in popular_exchanges:
    exchange = getattr(ccxt, exchange_name)()
    exchange_instances[exchange_name] = exchange

# Iterate through the popular exchanges to find arbitrage opportunities
for base_exchange_name in popular_exchanges:
    base_exchange = exchange_instances[base_exchange_name]

    for first_exchange_name in popular_exchanges:
        first_exchange = exchange_instances[first_exchange_name]

        for second_exchange_name in popular_exchanges:
            second_exchange = exchange_instances[second_exchange_name]

            # Update the progress bar
            progress_bar.update(1)

            # Iterate through specific base symbols within each exchange
            for base_symbol in base_exchange.symbols:
                for first_symbol in first_exchange.symbols:
                    for second_symbol in second_exchange.symbols:
                        # Check if it's a valid triangular arbitrage
                        if (
                            base_symbol != first_symbol and
                            first_symbol != second_symbol and
                            second_symbol != base_symbol
                        ):
                            try:
                                # Fetch ticker data for all three currency pairs
                                ticker_base = base_exchange.fetch_ticker(base_symbol)
                                ticker_first = first_exchange.fetch_ticker(first_symbol)
                                ticker_second = second_exchange.fetch_ticker(second_symbol)

                                # Calculate potential arbitrage profit
                                arbitrage_profit = (
                                    (1 / ticker_base['ask']) *
                                    (ticker_first['bid']) *
                                    (ticker_second['bid']) - 1
                                )

                                # Check if there's a profit opportunity
                                if arbitrage_profit > 0:
                                    opportunity = {
                                        'Base Exchange': base_exchange_name,
                                        'First Exchange': first_exchange_name,
                                        'Second Exchange': second_exchange_name,
                                        'Base Symbol': base_symbol,
                                        'First Symbol': first_symbol,
                                        'Second Symbol': second_symbol,
                                        'Arbitrage Profit': arbitrage_profit
                                    }
                                    arbitrage_opportunities.append(opportunity)

                            except Exception as e:
                                pass

# Close the progress bar
progress_bar.close()

# Print the found arbitrage opportunities
if arbitrage_opportunities:
    arbitrage_opportunities.sort(key=lambda x: x['Arbitrage Profit'], reverse=True)
    for opportunity in arbitrage_opportunities:
        print(opportunity)
else:
    print("No arbitrage opportunities found.")
