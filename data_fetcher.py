import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
import numpy as np

class DataFetcher:
    def __init__(self):
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.cryptocompare_base_url = "https://min-api.cryptocompare.com/data"
        
    def fetch_bitcoin_data(self, days=730):  # 2 years = 730 days
        """Fetch Bitcoin price data from multiple sources with fallbacks"""
        print("🔍 Fetching Bitcoin data from multiple sources...")
        
        # Try multiple data sources in order of reliability
        data_sources = [
            ("CryptoCompare", self._fetch_from_cryptocompare),
            ("CoinGecko", self._fetch_from_coingecko),
            ("Yahoo Finance", self._fetch_from_yfinance),
            ("Sample Data", self._generate_sample_data)
        ]
        
        for source_name, fetch_func in data_sources:
            try:
                print(f"Trying {source_name}...")
                btc_data = fetch_func(days)
                if btc_data is not None and not btc_data.empty:
                    print(f"✅ Successfully fetched {len(btc_data)} days from {source_name}")
                    return btc_data
                else:
                    print(f"⚠️  {source_name} returned no data")
            except Exception as e:
                print(f"❌ {source_name} failed: {str(e)[:100]}...")
                continue
        
        print("❌ All data sources failed, using sample data")
        return self._generate_sample_data(days)
    
    def _fetch_from_cryptocompare(self, days):
        """Fetch Bitcoin data from CryptoCompare API"""
        try:
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # CryptoCompare historical data endpoint
            url = f"{self.cryptocompare_base_url}/v2/histoday"
            params = {
                'fsym': 'BTC',      # From symbol (Bitcoin)
                'tsym': 'USD',      # To symbol (US Dollar)
                'limit': min(days, 2000),  # Max 2000 days
                'aggregate': 1      # Daily aggregation
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['Response'] == 'Success':
                    # Extract price data
                    prices = data['Data']['Data']
                    
                    # Convert to DataFrame
                    df_data = []
                    for price_point in prices:
                        df_data.append({
                            'date': datetime.fromtimestamp(price_point['time']),
                            'price': price_point['close'],
                            'volume': price_point['volumeto'],  # Volume in USD
                            'market_cap': 0  # CryptoCompare doesn't provide this
                        })
                    
                    df = pd.DataFrame(df_data)
                    df = df.set_index('date')
                    df = df.sort_index()
                    
                    # Add returns and volatility
                    df['returns'] = df['price'].pct_change()
                    df['volatility'] = df['returns'].rolling(window=30).std()
                    
                    return df
                else:
                    print(f"CryptoCompare API error: {data.get('Message', 'Unknown error')}")
                    return None
            else:
                print(f"CryptoCompare API returned status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"CryptoCompare API error: {e}")
            return None
    
    def _fetch_from_coingecko(self, days):
        """Fetch Bitcoin data from CoinGecko API with improved error handling"""
        try:
            # Try the new endpoint format
            url = f"{self.coingecko_base_url}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            # Add headers to avoid rate limiting
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract price data
                prices = data['prices']
                volumes = data.get('total_volumes', [])
                market_caps = data.get('market_caps', [])
                
                # Convert to DataFrame
                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                
                # Add volume if available
                if volumes:
                    df['volume'] = [vol[1] for vol in volumes]
                else:
                    df['volume'] = 0
                
                # Add market cap if available
                if market_caps:
                    df['market_cap'] = [cap[1] for cap in market_caps]
                else:
                    df['market_cap'] = 0
                
                # Clean up
                df = df.drop('timestamp', axis=1)
                df = df.set_index('date')
                df = df.sort_index()
                
                # Add returns and volatility
                df['returns'] = df['price'].pct_change()
                df['volatility'] = df['returns'].rolling(window=30).std()
                
                return df
                
            elif response.status_code == 429:
                print("CoinGecko API rate limited, trying alternative...")
                return None
            else:
                print(f"CoinGecko API returned status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"CoinGecko API error: {e}")
            return None
    
    def _fetch_from_yfinance(self, days):
        """Fetch Bitcoin data from Yahoo Finance with improved error handling"""
        try:
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Try multiple Bitcoin tickers
            tickers = ['BTC-USD', 'BTCUSD=X', 'BTC=X']
            
            for ticker in tickers:
                try:
                    print(f"Trying yfinance ticker: {ticker}")
                    btc = yf.Ticker(ticker)
                    data = btc.history(start=start_date, end=end_date, interval="1d", progress=False)
                    
                    if not data.empty and len(data) > 10:  # Need at least 10 days of data
                        # Rename columns to match expected format
                        df = pd.DataFrame()
                        df['price'] = data['Close']
                        df['volume'] = data['Volume']
                        df['market_cap'] = 0  # yfinance doesn't provide market cap
                        
                        # Add returns and volatility
                        df['returns'] = df['price'].pct_change()
                        df['volatility'] = df['returns'].rolling(window=30).std()
                        
                        print(f"✅ yfinance success with ticker {ticker}")
                        return df
                    else:
                        print(f"Ticker {ticker} returned insufficient data")
                        
                except Exception as e:
                    print(f"Ticker {ticker} failed: {str(e)[:50]}...")
                    continue
            
            print("All yfinance tickers failed")
            return None
            
        except Exception as e:
            print(f"yfinance API error: {e}")
            return None
    
    def _generate_sample_data(self, days):
        """Generate realistic sample Bitcoin data for demonstration"""
        print("Generating realistic sample data for demonstration...")
        
        # Generate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate realistic Bitcoin price data with current market trends
        np.random.seed(42)  # For reproducible results
        
        # Start with a realistic current price (around $110k)
        start_price = 110000
        
        # Generate price movements with realistic volatility and trends
        prices = [start_price]
        current_trend = 0.0001  # Slight upward bias
        
        for i in range(1, len(dates)):
            # Add some trend changes
            if i % 30 == 0:  # Monthly trend change
                current_trend += np.random.normal(0, 0.001)
            
            # Daily return with trend and volatility
            volatility = 0.025 + abs(current_trend) * 2  # Higher volatility during trends
            daily_return = np.random.normal(current_trend, volatility)
            
            # Ensure price doesn't go below reasonable levels
            new_price = prices[-1] * (1 + daily_return)
            new_price = max(new_price, 10000)  # Minimum $10k
            
            prices.append(new_price)
        
        # Create realistic volume data (higher during volatile periods)
        volumes = []
        for i, price in enumerate(prices):
            if i > 0:
                price_change = abs(prices[i] - prices[i-1]) / prices[i-1]
                base_volume = 2e10  # Base volume $20B
                volatility_multiplier = 1 + price_change * 10  # Higher volume during big moves
                volume = base_volume * volatility_multiplier * np.random.lognormal(0, 0.3)
                volumes.append(volume)
            else:
                volumes.append(2e10)
        
        # Create DataFrame
        df = pd.DataFrame({
            'price': prices,
            'volume': volumes,
            'market_cap': [price * 19_000_000 for price in prices],  # Approximate BTC supply
            'returns': pd.Series(prices).pct_change(),
            'volatility': pd.Series(prices).pct_change().rolling(window=30).std()
        }, index=dates)
        
        print(f"✅ Generated {len(df)} days of realistic sample data")
        return df
    
    def fetch_traditional_markets(self, start_date, end_date):
        """Fetch traditional market data for correlation analysis"""
        try:
            # Try multiple ticker formats for better reliability
            ticker_mappings = {
                'S&P 500': ['^GSPC', 'SPY', '^VIX'],
                'Gold': ['GC=F', 'GLD', 'XAUUSD=X'],
                'US Dollar': ['DX-Y.NYB', 'UUP', 'DXY']
            }
            
            market_data = {}
            
            for market_name, tickers in ticker_mappings.items():
                for ticker in tickers:
                    try:
                        print(f"Trying {market_name} ticker: {ticker}")
                        data = yf.download(ticker, start=start_date, end=end_date, progress=False, timeout=30)
                        
                        if not data.empty and len(data) > 10:
                            market_data[market_name] = data['Close']
                            print(f"✅ {market_name} data fetched successfully")
                            break
                        else:
                            print(f"Ticker {ticker} returned insufficient data")
                            
                    except Exception as e:
                        print(f"Ticker {ticker} failed: {str(e)[:50]}...")
                        continue
                
                if market_name not in market_data:
                    print(f"⚠️  Could not fetch {market_name} data")
            
            # Create correlation DataFrame
            if market_data:
                correlation_df = pd.DataFrame(market_data)
                correlation_df = correlation_df.dropna()
                return correlation_df
            
            return None
            
        except Exception as e:
            print(f"Error fetching traditional market data: {e}")
            return None
    
    def calculate_correlations(self, btc_data, market_data):
        """Calculate correlation between Bitcoin and traditional markets"""
        if btc_data is None or market_data is None:
            return None
        
        try:
            # Align data by date
            btc_returns = btc_data['returns'].dropna()
            market_returns = market_data.pct_change().dropna()
            
            # Align indices
            aligned_data = pd.concat([btc_returns, market_returns], axis=1).dropna()
            
            if len(aligned_data) < 30:  # Need sufficient data
                return None
            
            # Calculate correlations
            correlations = {}
            for col in market_returns.columns:
                if col in aligned_data.columns:
                    corr = aligned_data['returns'].corr(aligned_data[col])
                    correlations[col] = corr
            
            return correlations
            
        except Exception as e:
            print(f"Error calculating correlations: {e}")
            return None

if __name__ == "__main__":
    # Test the data fetcher
    fetcher = DataFetcher()
    
    # Fetch Bitcoin data
    print("Testing enhanced data fetcher...")
    btc_data = fetcher.fetch_bitcoin_data()
    
    if btc_data is not None:
        print(f"✅ Successfully fetched {len(btc_data)} days of Bitcoin data")
        print(f"   Date range: {btc_data.index[0].date()} to {btc_data.index[-1].date()}")
        print(f"   Current price: ${btc_data['price'].iloc[-1]:,.2f}")
        print(f"   Data columns: {list(btc_data.columns)}")
        
        # Fetch traditional market data
        print("\nFetching traditional market data...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        market_data = fetcher.fetch_traditional_markets(start_date, end_date)
        
        if market_data is not None:
            print(f"✅ Successfully fetched traditional market data")
            print(f"   Markets: {list(market_data.columns)}")
            
            # Calculate correlations
            correlations = fetcher.calculate_correlations(btc_data, market_data)
            if correlations:
                print("\nCorrelations with Bitcoin:")
                for market, corr in correlations.items():
                    print(f"   {market}: {corr:.4f}")
        else:
            print("⚠️  Traditional market data fetch failed")
    else:
        print("❌ Failed to fetch Bitcoin data")
