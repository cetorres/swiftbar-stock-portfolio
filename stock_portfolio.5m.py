#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Stock Portfolio</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Carlos E. Torres</xbar.author>
# <xbar.author.github>cetorres</xbar.author.github>
# <xbar.desc>Show your stock portfolio and prices in your menu bar using Yahoo Finance real-time data.</xbar.desc>
# <xbar.dependencies>python3,yfinance</xbar.dependencies>
# <xbar.image>https://github.com/cetorres/swiftbar-stock-portfolio/blob/main/stock_portfolio_preview.png</xbar.image>
# <xbar.abouturl>https://github.com/cetorres/swiftbar-stock-portfolio</xbar.abouturl>

import subprocess
import sys
from pathlib import Path
import yfinance as yf


# Define the path to the data file that will store the stock symbols, quantities, and initial costs.
DATA_FILE = Path.home() / ".stock_portfolio.txt"

# The script path for the current file
SCRIPT_PATH = str(Path(__file__).resolve())

# ANSI color codes for green and red, and reset code to clear formatting
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'
FONT = 'Menlo'


def load_portfolio():
    """Load the stock portfolio from the data file. If the file does not exist, return an empty dictionary."""
    if not DATA_FILE.exists():
        return {}
    portfolio = {}
    with open(DATA_FILE, 'r') as f:
        for line in f:
            symbol, quantity, initial_cost = line.strip().split(',')
            portfolio[symbol] = [int(quantity), float(initial_cost)]
    return portfolio


def save_portfolio(portfolio):
    """Save the stock portfolio to the data file."""
    with open(DATA_FILE, 'w') as f:
        for symbol, (quantity, initial_cost) in portfolio.items():
            f.write(f"{symbol},{quantity},{initial_cost}\n")


def render_add_stock():
    print(f"Add stock | sfimage=plus shell=\"{SCRIPT_PATH}\" param1=add refresh=true terminal=false")


def render_empty_portfolio():
    print("⚠ Add stocks")
    print("---")
    print("You need to add stocks to your portfolio.")
    print("---")
    render_add_stock()


def render_delete_stock():
    print(f"Delete stock | sfimage=xmark.bin")
    for symbol in portfolio.keys():
        print(f"-- {symbol} | shell=\"{SCRIPT_PATH}\" param1=delete param2={symbol} refresh=true terminal=false")


def render_edit_file():
    print(f"Edit data file | sfimage=pencil shell=open param1=\"{DATA_FILE}\" refresh=true terminal=false")


def render():
    if not portfolio or len(portfolio) == 0:
        render_empty_portfolio()
        print("Refresh | sfimage=arrow.clockwise refresh=true")
        return
    
    # Get all symbols tickers at once to minimize API calls
    tickers = yf.Tickers(' '.join(portfolio.keys()))

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
        symbol_info = portfolio.get(ticker.info.get('symbol', 'N/A'))
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
        print(f"-- View on Yahoo Finance | sfimage=globe href=https://finance.yahoo.com/quote/{symbol}/ webview=true")
        print(f"-- Edit {symbol} | sfimage=pencil shell=\"{SCRIPT_PATH}\" param1=edit param2={symbol} refresh=true terminal=false")
        print(f"-- Delete {symbol} | sfimage=xmark shell=\"{SCRIPT_PATH}\" param1=delete param2={symbol} refresh=true terminal=false")

    # Display total value of the portfolio
    total_str = f'${total:.2f}'
    print('.' * 61 + GREEN + total_str.rjust(10) + RESET + f" | font='{FONT}' ansi=true")
    print("---")

    render_add_stock()
    render_edit_file()
    print("Refresh | sfimage=arrow.clockwise refresh=true")
    print(f"Yahoo Finance | sfimage=globe href=https://finance.yahoo.com webview=true")
    print("---")


def show_add_stock_dialog(symbolToEdit=None):
    if symbolToEdit:
        if symbolToEdit in portfolio:
            symbol = symbolToEdit
        else:
            symbol = ""
    else:
        symbol = ""
        symbol = subprocess.run(['osascript', '-e', f'Tell application "System Events" to display dialog "Enter the stock symbol" default answer "{symbol}" with title "Add Stock"'], capture_output=True, text=True).stdout.strip().split(':')[-1].strip()
    if not symbol or symbol == "":
        return
    
    if symbolToEdit:
        quantity = portfolio[symbol][0]
        initial_cost = portfolio[symbol][1]
    else:
        quantity = ""
        initial_cost = ""
    
    quantity = subprocess.run(['osascript', '-e', f'Tell application "System Events" to display dialog "Enter the quantity" default answer "{quantity}" with title "Add Stock"'], capture_output=True, text=True).stdout.strip().split(':')[-1].strip()
    if not quantity or quantity == "":
        return
   
    initial_cost = subprocess.run(['osascript', '-e', f'Tell application "System Events" to display dialog "Enter the initial cost per share" default answer "{initial_cost}" with title "Add Stock"'], capture_output=True, text=True).stdout.strip().split(':')[-1].strip()
    if not initial_cost or initial_cost == "":
        return
    
    if not symbol or not quantity or not quantity.isdigit() or not initial_cost or not initial_cost.replace('.', '').isdigit():
        # Show an error message if any input is missing
        subprocess.run(['osascript', '-e', 'Tell application "System Events" to display dialog "Please enter all required fields with valid input." buttons {"OK"} default button 1 with title "Add Stock"'], capture_output=True, text=True)
        return
    
    symbol = symbol.upper()
    quantity = int(quantity)
    initial_cost = float(initial_cost)
    portfolio[symbol] = [quantity, initial_cost]
    save_portfolio(portfolio)
    if symbolToEdit:
        message = f"Stock {symbol} updated successfully."
    else:        
        message = f"Stock {symbol} added successfully."
    subprocess.run(['osascript', '-e', f'Tell application "System Events" to display dialog "{message}" buttons {"OK"} default button 1 with title "Add Stock"'], capture_output=True, text=True)


def delete_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        save_portfolio(portfolio)


# Load the portfolio from the data file. This will be used to display the portfolio and to add new stocks.
portfolio = load_portfolio()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        show_add_stock_dialog()
    elif len(sys.argv) > 1 and sys.argv[1] == "delete":
        symbol = sys.argv[2]
        delete_stock(symbol)
    elif len(sys.argv) > 1 and sys.argv[1] == "edit":
        symbol = sys.argv[2]
        show_add_stock_dialog(symbol)
    else:
        render()
