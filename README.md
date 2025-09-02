# Bitcoin Price Analysis Dashboard

A comprehensive, interactive dashboard for analyzing Bitcoin price data with technical indicators, volatility analysis, and market correlations.

## Features

### 📊 **Data Analysis**
- **2 Years of Historical Data**: Pulls comprehensive Bitcoin data from CoinGecko API
- **Real-time Updates**: Refresh data with a single click
- **Traditional Market Correlation**: Compare Bitcoin performance with S&P 500, Gold, and US Dollar

### 📈 **Technical Indicators**
- **Moving Averages**: SMA 20, 50, 200 and EMA 12, 26
- **MACD**: Moving Average Convergence Divergence with signal line and histogram
- **RSI**: Relative Strength Index with overbought/oversold levels
- **Stochastic Oscillator**: %K and %D lines with reference levels
- **Bollinger Bands**: Upper, lower, and middle bands with width analysis
- **Williams %R**: Momentum oscillator

### 📊 **Advanced Analytics**
- **Volatility Analysis**: Rolling volatility, ATR, and volatility ratios
- **Volume Analysis**: Volume trends, OBV, VPT, and volume rate of change
- **Support & Resistance**: Dynamic pivot points and support/resistance levels
- **Trend Analysis**: Multi-timeframe trend identification

### 🎨 **Interactive Visualizations**
- **Price Charts**: Candlestick-style with technical overlays
- **Volume Analysis**: Volume patterns and trends
- **Correlation Charts**: Market relationship visualizations
- **Responsive Design**: Bootstrap-based modern UI

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd "BTC Price Analysis"
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   python dashboard.py
   ```

4. **Access the dashboard**
   - Open your web browser
   - Navigate to: `http://127.0.0.1:8050`
   - The dashboard will automatically load with the latest data

## Usage

### Dashboard Navigation

#### **Summary Cards (Top Row)**
- **Current Price**: Live Bitcoin price with 1-day change
- **Market Trend**: Current market direction and moving average status
- **Volatility**: Current volatility status and ratio
- **Volume**: Volume pattern analysis

#### **Main Charts**
- **Bitcoin Price Chart**: Primary price chart with moving averages and Bollinger Bands
- **Volume Analysis**: Trading volume patterns and trends
- **Technical Indicators**: RSI, MACD, and Stochastic oscillators
- **Market Correlations**: Bitcoin correlation with traditional markets
- **Volatility Analysis**: Volatility trends and ratios

#### **Controls**
- **Refresh Data**: Update all data from APIs
- **Download Data**: Export analysis data to CSV format

### Interacting with Charts

- **Zoom**: Click and drag to zoom into specific time periods
- **Pan**: Click and drag to move around the chart
- **Hover**: Hover over data points for detailed information
- **Legend**: Click legend items to show/hide specific indicators
- **Reset**: Double-click to reset zoom and pan

### Data Interpretation

#### **Trend Analysis**
- **Strong Uptrend**: Price above all moving averages
- **Uptrend**: Price above 20 and 50-day moving averages
- **Sideways**: Mixed moving average positions
- **Downtrend**: Price below 20 and 50-day moving averages
- **Strong Downtrend**: Price below all moving averages

#### **Volatility Status**
- **High Volatility**: >1.5x average volatility
- **Above Average**: 1.2-1.5x average volatility
- **Normal**: 0.8-1.2x average volatility
- **Low Volatility**: 0.5-0.8x average volatility
- **Very Low**: <0.5x average volatility

#### **Volume Patterns**
- **High Volume**: >1.5x average volume
- **Above Average**: 1.2-1.5x average volume
- **Normal**: 0.8-1.2x average volume
- **Low Volume**: <0.8x average volume

## API Information

### CoinGecko API
- **Endpoint**: `https://api.coingecko.com/api/v3/coins/bitcoin/market_chart`
- **Rate Limit**: Free tier with reasonable limits
- **Data**: Price, volume, and market cap data

### Yahoo Finance API (via yfinance)
- **Data Sources**: S&P 500, Gold Futures, US Dollar Index
- **Purpose**: Correlation analysis with traditional markets

## Technical Details

### Architecture
- **Frontend**: Dash (React-based Python framework)
- **Styling**: Bootstrap components for responsive design
- **Charts**: Plotly for interactive visualizations
- **Data Processing**: Pandas and NumPy for analysis
- **API Integration**: Requests library for HTTP calls

### Data Flow
1. **Data Fetching**: APIs are called to retrieve market data
2. **Processing**: Raw data is cleaned and technical indicators calculated
3. **Analysis**: Technical analysis and correlation calculations
4. **Visualization**: Interactive charts are generated and displayed
5. **Updates**: Real-time data refresh capabilities

### Performance Considerations
- **Caching**: Data is fetched once and cached for session
- **Efficient Calculations**: Vectorized operations for technical indicators
- **Responsive UI**: Asynchronous data loading and updates

## Analytics Calculation Details

### **Moving Averages**

#### **Simple Moving Average (SMA)**
- **Formula**: `SMA(n) = (P₁ + P₂ + ... + Pₙ) / n`
- **Where**: P = Price, n = Period (20, 50, 200 days)
- **Calculation**: Rolling mean over specified window
- **Purpose**: Smooth price data to identify trends

#### **Exponential Moving Average (EMA)**
- **Formula**: `EMA = Price × k + EMA(previous) × (1 - k)`
- **Where**: `k = 2 / (n + 1)` (n = 12, 26 days)
- **Calculation**: Weighted average giving more importance to recent prices
- **Purpose**: More responsive to recent price changes than SMA

#### **MACD (Moving Average Convergence Divergence)**
- **MACD Line**: `EMA(12) - EMA(26)`
- **Signal Line**: `EMA(9) of MACD Line`
- **Histogram**: `MACD Line - Signal Line`
- **Purpose**: Identify momentum changes and potential trend reversals

### **Momentum Indicators**

#### **Relative Strength Index (RSI)**
- **Formula**: `RSI = 100 - (100 / (1 + RS))`
- **Where**: `RS = Average Gain / Average Loss` over 14 periods
- **Gain**: Sum of positive price changes over 14 days
- **Loss**: Sum of negative price changes over 14 days
- **Interpretation**: 
  - RSI > 70: Overbought (potential sell signal)
  - RSI < 30: Oversold (potential buy signal)
  - RSI 30-70: Neutral zone

#### **Stochastic Oscillator**
- **%K Line**: `100 × (Current Price - Lowest Low) / (Highest High - Lowest Low)`
- **Where**: Highest/Lowest calculated over 14 periods
- **%D Line**: `3-period SMA of %K`
- **Interpretation**:
  - %K > 80: Overbought
  - %K < 20: Oversold
  - %K crossing %D: Potential reversal signals

#### **Williams %R**
- **Formula**: `-100 × (Highest High - Current Price) / (Highest High - Lowest Low)`
- **Where**: Highest/Lowest calculated over 14 periods
- **Interpretation**:
  - %R > -20: Overbought
  - %R < -80: Oversold

### **Volatility Indicators**

#### **Bollinger Bands**
- **Middle Band**: `20-period SMA`
- **Upper Band**: `Middle Band + (2 × 20-period Standard Deviation)`
- **Lower Band**: `Middle Band - (2 × 20-period Standard Deviation)`
- **Bandwidth**: `(Upper Band - Lower Band) / Middle Band`
- **Purpose**: Identify overbought/oversold conditions and volatility expansion/contraction

#### **Average True Range (ATR)**
- **True Range**: `max(High - Low, |High - Previous Close|, |Low - Previous Close|)`
- **ATR**: `14-period SMA of True Range`
- **Purpose**: Measure market volatility regardless of direction

#### **Volatility Ratio**
- **Formula**: `Current Volatility / 252-day Average Volatility`
- **Where**: Volatility = 30-day rolling standard deviation of returns
- **Purpose**: Compare current volatility to historical average

### **Volume Indicators**

#### **On-Balance Volume (OBV)**
- **Formula**: `OBV = Previous OBV + Volume × Sign(Price Change)`
- **Where**: Sign = +1 if price increases, -1 if price decreases
- **Purpose**: Confirm price trends through volume confirmation

#### **Volume Price Trend (VPT)**
- **Formula**: `VPT = Previous VPT + Volume × ((Current Price - Previous Price) / Previous Price)`
- **Purpose**: Measure cumulative volume-price relationship

#### **Volume Rate of Change**
- **Formula**: `(Current Volume - Volume 10 periods ago) / Volume 10 periods ago × 100`
- **Purpose**: Identify volume momentum and potential trend changes

### **Support & Resistance**

#### **Pivot Points**
- **Pivot**: `(High + Low + Close) / 3`
- **Resistance 1**: `2 × Pivot - Low`
- **Support 1**: `2 × Pivot - High`
- **Resistance 2**: `Pivot + (High - Low)`
- **Support 2**: `Pivot - (High - Low)`
- **Where**: High/Low calculated over 20-period rolling window
- **Purpose**: Identify potential reversal levels

### **Correlation Analysis**

#### **Market Correlation**
- **Formula**: `Correlation = Covariance(BTC Returns, Market Returns) / (σ(BTC) × σ(Market))`
- **Where**: 
  - Returns = Percentage change in prices
  - Covariance = Measure of joint variability
  - σ = Standard deviation
- **Calculation**: Pearson correlation coefficient over aligned time periods
- **Interpretation**:
  - +1.0: Perfect positive correlation
  - 0.0: No correlation
  - -1.0: Perfect negative correlation
  - ±0.7+: Strong correlation
  - ±0.3-0.7: Moderate correlation
  - ±0.0-0.3: Weak correlation

### **Trend Analysis Algorithm**

#### **Multi-Timeframe Trend Classification**
```python
if current_price > SMA_20 > SMA_50 > SMA_200:
    trend = "Strong Uptrend"
elif current_price > SMA_20 > SMA_50:
    trend = "Uptrend"
elif current_price < SMA_20 < SMA_50 < SMA_200:
    trend = "Strong Downtrend"
elif current_price < SMA_20 < SMA_50:
    trend = "Downtrend"
else:
    trend = "Sideways/Consolidation"
```

### **Volatility Classification Algorithm**

#### **Volatility Status Determination**
```python
vol_ratio = current_volatility / 252_day_average_volatility

if vol_ratio > 1.5:
    status = "High Volatility"
elif vol_ratio > 1.2:
    status = "Above Average Volatility"
elif vol_ratio < 0.8:
    status = "Low Volatility"
elif vol_ratio < 0.5:
    status = "Very Low Volatility"
else:
    status = "Normal Volatility"
```

### **Volume Pattern Classification**

#### **Volume Status Determination**
```python
volume_ratio = current_volume / 20_day_average_volume

if volume_ratio > 1.5:
    pattern = "High Volume"
elif volume_ratio > 1.2:
    pattern = "Above Average Volume"
elif volume_ratio < 0.8:
    pattern = "Low Volume"
else:
    pattern = "Normal Volume"
```

## Troubleshooting

### Common Issues

#### **Data Not Loading**
- Check internet connection
- Verify API endpoints are accessible
- Check console for error messages

#### **Charts Not Displaying**
- Ensure all dependencies are installed
- Check browser console for JavaScript errors
- Verify data is properly loaded

#### **Performance Issues**
- Reduce data timeframe if needed
- Close other browser tabs
- Check system resources

### Error Messages

- **"Failed to fetch data"**: API connection issue
- **"Insufficient data"**: Not enough historical data for analysis
- **"Error updating charts"**: Data processing issue

## Customization

### Adding New Indicators
1. Modify `technical_analysis.py`
2. Add calculation methods
3. Update dashboard callbacks
4. Add new chart components

### Changing Data Sources
1. Modify `data_fetcher.py`
2. Update API endpoints
3. Adjust data processing logic
4. Test with new data format

### Styling Changes
1. Modify Bootstrap classes in `dashboard.py`
2. Update Plotly chart themes
3. Customize CSS if needed

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include error handling
- Write clear variable names

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review error messages in console
- Ensure all dependencies are properly installed
- Verify API access and rate limits

## Future Enhancements

- **Additional Cryptocurrencies**: Support for other major cryptocurrencies
- **Advanced Analytics**: Machine learning price predictions
- **Portfolio Tracking**: Personal portfolio performance
- **Alerts**: Price and indicator-based notifications
- **Mobile App**: Native mobile application
- **API Keys**: Support for premium API access

---

**Note**: This dashboard is for educational and analysis purposes. Cryptocurrency investments carry significant risk. Always do your own research and consider consulting with financial advisors before making investment decisions.

