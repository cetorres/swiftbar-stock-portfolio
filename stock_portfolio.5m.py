#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Stock Portfolio</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Carlos E. Torres</xbar.author>
# <xbar.author.github>cetorres</xbar.author.github>
# <xbar.desc>Show your stock portfolio and prices in your menu bar using Yahoo Finance real-time data.</xbar.desc>
# <xbar.dependencies>python3,yfinance</xbar.dependencies>
# <xbar.image>https://github.com/cetorres/swiftbar-stock-portfolio/blob/main/stock_portfolio_preview.png</xbar.image>
# <xbar.abouturl>https://github.com/cetorres/swiftbar-stock-portfolio</xbar.abouturl>

import yfinance as yf

# ANSI color codes for green and red, and reset code to clear formatting
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'
FONT = 'Menlo'

# Define the stock symbols and their corresponding quantities and initial costs in the portfolio
# Format: {'SYMBOL': [quantity, initial_cost]}
# Example: 'AAPL': [100, 250.31] means 100 shares of AAPL bought at $250.31 each.
# The first symbol will be displayed in the menu bar, the rest will be shown in the dropdown.
symbols_quantities = {
    'AAPL': [100, 250.31],
    'MSFT': [50, 300.50],
    'GOOGL': [25, 280.75]
}

def render():
    # Get all symbols tickers at once to minimize API calls
    tickers = yf.Tickers(' '.join(symbols_quantities.keys()))

    # Get first symbol info to display in the menu bar
    first = next(iter(tickers.tickers.values()))
    price = first.info.get('regularMarketPrice', 'N/A')
    change = first.info.get('regularMarketChange', 0)
    print(f"{price:.2f} | sfimage=arrowtriangle.{'up' if change > 0 else 'down'}.fill")
    print("---")

    # Display detailed stock information for all tickers in the dropdown menu
    total = 0
    print(f"Symbol     Price        Change (Percent)     Qty   Cost     Total Value | font='{FONT}'")
    for ticker in tickers.tickers.values():
        symbol_info = symbols_quantities.get(ticker.info.get('symbol', 'N/A'))
        quantity = symbol_info[0]
        initial_cost = symbol_info[1]
        info = ticker.info
        symbol = info.get('symbol', 'N/A')
        current_price = info.get('regularMarketPrice', 'N/A')
        change = info.get('regularMarketChange', 0)
        change_percent = info.get('regularMarketChangePercent', 0)
        color = ''
        if change > 0:
            color = GREEN + '▲'
        if change < 0:
            color = RED + '▼'
        # Format change to decimal with a precision of two and reset ansi color at the end
        change_in_percent = f'({change:.2f}, {change_percent:.2f}%)'
        colored_change = color + change_in_percent + RESET
        stock_info = '{:<10} {:<12} {:<27} {:>5} {:>9} {:>12}'
        sub_total = quantity * current_price
        total += sub_total
        print(stock_info.format(symbol, f'${current_price:.2f}', colored_change, quantity, f'${initial_cost:.2f}', f'${sub_total:.2f}') + f" | font='{FONT}' href=https://finance.yahoo.com/quote/{symbol}/ webview=true ansi=true")

    # Display total value of the portfolio
    total_str = f'${total:.2f}'
    print('.' * 61 + GREEN + total_str.rjust(10) + RESET + f" | font='{FONT}' ansi=true")
    print("---")

    print("Refresh | sfimage=arrow.clockwise refresh=true")
    print(f"Yahoo Finance | sfimage=globe href=https://finance.yahoo.com webview=true")
    print("---")


if __name__ == "__main__":
    render()
