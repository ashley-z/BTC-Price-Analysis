# 🚀 Quick Start Guide

## Start the Dashboard (Choose One Method)

### Method 1: Simple Python Command
```bash
python dashboard.py
```

### Method 2: Use the Launcher Script
```bash
./start_dashboard.sh
```

### Method 3: Use the Python Launcher
```bash
python run_dashboard.py
```

## Access the Dashboard

1. **Open your web browser**
2. **Navigate to**: `http://127.0.0.1:8050`
3. **Wait for data to load** (may take a few seconds on first run)

## Dashboard Features

### 📊 **Summary Cards (Top)**
- **Current Price**: Live Bitcoin price with daily change
- **Market Trend**: Current market direction
- **Volatility**: Current volatility status
- **Volume**: Trading volume pattern

### 📈 **Main Charts**
- **Bitcoin Price**: Price chart with moving averages and Bollinger Bands
- **Volume Analysis**: Trading volume patterns
- **Technical Indicators**: RSI, MACD, Stochastic
- **Market Correlations**: Bitcoin vs traditional markets
- **Volatility Analysis**: Volatility trends

### 🎛️ **Controls**
- **Refresh Data**: Update all data from APIs
- **Download Data**: Export analysis to CSV

## Troubleshooting

### Dashboard Won't Start?
```bash
# Check dependencies
pip install -r requirements.txt

# Run tests
python test_data.py
```

### No Data Loading?
- **Check internet connection** - Dashboard needs internet to fetch Bitcoin data
- **Wait a few seconds** for API calls to complete
- **Click "Refresh Data"** button if charts are empty
- **Run quick test**: `python quick_test.py` to verify data fetching

### Charts Not Displaying?
- Refresh the browser page
- Check browser console for errors
- Ensure JavaScript is enabled
- Verify data is loaded by checking summary cards

### API Issues?
- **CoinGecko API**: Primary data source for Bitcoin
- **Fallback**: yfinance and sample data if APIs fail
- **Rate Limits**: Some APIs have usage limits

## Data Sources

- **Bitcoin Data**: CoinGecko API (2 years historical) + yfinance fallback
- **Traditional Markets**: Yahoo Finance (S&P 500, Gold, USD)
- **Updates**: Real-time via refresh button
- **Fallback**: Sample data generation if all APIs fail

## Stop the Dashboard

- **In terminal**: Press `Ctrl+C`
- **Or close the terminal window**

## Quick Data Test

If you're having issues, test data fetching separately:
```bash
python quick_test.py
```

This will show you if the data sources are working correctly.

---

**Need Help?** Check the full `README.md` for detailed documentation.
