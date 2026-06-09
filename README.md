# Stock Portfolio

A [SwiftBar](https://github.com/swiftbar/SwiftBar)/[xbar](https://github.com/matryer/xbar) plugin written in Python that displays your stock portfolio directly in the macOS menu bar using real-time data from Yahoo Finance.

![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![SwiftBar](https://img.shields.io/badge/SwiftBar-Plugin-orange?style=flat)

---

## Features

- **Menu bar ticker** — shows the price and a live up/down arrow for your primary stock at a glance
- **Portfolio dropdown** — a formatted table with symbol, current price, change (value + percent), quantity held, cost basis, and current total value for every position
- **Color-coded changes** — green (▲) for gains, red (▼) for losses using ANSI colors
- **Portfolio total** — running total of your entire portfolio's current market value
- **Yahoo Finance links** — click any row to open that stock's Yahoo Finance page in a webview
- **Auto-refresh** — data refreshes every 5 minutes automatically
- **Manual refresh** — a Refresh menu item lets you force an immediate update

---

## Preview

```
▼ $296.38

Symbol     Price        Change (Percent)          Qty  Cost      Total Value
AAPL       $296.38      ▼(-5.15, -1.71%)          100  $250.31     $29638.50
MSFT       $410.88      ▼(-0.86, -0.21%)           50  $300.50     $20544.00
GOOGL      $369.69      ▲(+6.38, 1.75%)            25  $280.75      $9242.12
...................................................................$59424.62

↺ Refresh
🌐 Yahoo Finance
```

<img src="stock_portfolio_preview.png" />

---

## Requirements

| Requirement | Version |
|---|---|
| macOS | 12 Monterey or later |
| SwiftBar/xbar | [Latest release](https://github.com/swiftbar/SwiftBar/releases)/[Latest release](https://github.com/matryer/xbar/releases) |
| Python | 3.x |
| yfinance | Latest |

---

## Installation

### 1. Install SwiftBar/xbar

Download and install SwiftBar from the [official releases page](https://github.com/swiftbar/SwiftBar/releases) or via Homebrew:

```bash
brew install swiftbar
```

Or install xbar from its official [website](https://xbarapp.com/).

### 2. Install the Python dependency

```bash
pip3 install yfinance
```

### 3. Add the plugin

Copy `stock_portfolio.5m.py` to your SwiftBar plugins directory (configured when you first launch SwiftBar) and make it executable:

```bash
cp stock_portfolio.5m.py ~/path/to/swiftbar-plugins/
chmod +x ~/path/to/swiftbar-plugins/stock_portfolio.5m.py
```

SwiftBar will detect the new plugin automatically. If it doesn't appear right away, use **SwiftBar → Refresh All** from the menu bar.

---

## Configuration

Open `stock_portfolio.5m.py` and edit the `symbols_quantities` dictionary near the top of the file:

```python
symbols_quantities = {
    'AAPL': [100, 250.31],
    'MSFT': [50, 300.50],
    'GOOGL': [25, 280.75]
}
```

Each entry follows this format:

```python
'TICKER': [shares_owned, cost_per_share]
```

| Field | Description |
|---|---|
| `TICKER` | Stock symbol as listed on Yahoo Finance (e.g. `AAPL`, `TSLA`, `BTC-USD`) |
| `shares_owned` | Number of shares (or units) you hold |
| `cost_per_share` | Your average cost basis per share in USD |

> **Note:** The **first** symbol in the dictionary is the one displayed in the menu bar. Reorder the entries to change which ticker is shown at a glance.

### Changing the refresh interval

The filename encodes the refresh interval. Rename the file to change how often the data updates:

| Filename | Refresh interval |
|---|---|
| `stock_portfolio.1m.py` | Every 1 minute |
| `stock_portfolio.5m.py` | Every 5 minutes (default) |
| `stock_portfolio.15m.py` | Every 15 minutes |
| `stock_portfolio.1h.py` | Every 1 hour |

See the [SwiftBar documentation](https://github.com/swiftbar/SwiftBar#plugin-naming) for the full naming convention.

---

## How It Works

1. On each refresh cycle SwiftBar executes the Python script.
2. The script calls `yfinance.Tickers()` once with all symbols to minimize API requests.
3. The first line printed becomes the menu bar title (price + directional arrow SF Symbol).
4. Lines after `---` populate the dropdown, formatted as a fixed-width table with ANSI color support.
5. Each stock row carries a `href` to its Yahoo Finance page and opens in SwiftBar's built-in webview.

---

## Troubleshooting

**Plugin does not appear in the menu bar**
- Confirm the file is executable: `chmod +x stock_portfolio.5m.py`
- Check that the shebang line (`#!/usr/bin/python3`) points to a valid Python 3 installation: `which python3`

**`ModuleNotFoundError: No module named 'yfinance'`**
- The shebang must use the same Python that has `yfinance` installed. Find the correct path with `which python3` and update the first line of the script accordingly, or install into that interpreter: `pip3 install yfinance`

**Prices show `N/A`**
- Yahoo Finance occasionally returns incomplete data. The plugin will display updated values on the next refresh cycle. Check that the ticker symbols are valid on [finance.yahoo.com](https://finance.yahoo.com).

**Colors not showing**
- Ensure the `ansi=true` parameter is present on each printed row (it is included by default). SwiftBar 1.4+ supports ANSI colors natively.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Carlos E. Torres** — [@cetorres](https://github.com/cetorres)
