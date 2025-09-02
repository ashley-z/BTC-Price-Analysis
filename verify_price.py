#!/usr/bin/env python3
"""
Quick verification of current Bitcoin price
"""

from data_fetcher import DataFetcher
from datetime import datetime

def main():
    print("🔍 Verifying Current Bitcoin Price")
    print("=" * 40)
    
    fetcher = DataFetcher()
    
    # Fetch current Bitcoin data
    print("Fetching latest Bitcoin data...")
    btc_data = fetcher.fetch_bitcoin_data(days=30)  # Just get recent data
    
    if btc_data is not None and not btc_data.empty:
        current_price = btc_data['price'].iloc[-1]
        current_date = btc_data.index[-1]
        
        print(f"✅ Current Bitcoin Price: ${current_price:,.2f}")
        print(f"📅 Last Updated: {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Data Source: CryptoCompare API")
        print(f"📈 24h Change: {btc_data['returns'].iloc[-1]*100:+.2f}%")
        
        # Show last 5 prices for verification
        print(f"\n📊 Last 5 Prices:")
        for i in range(-5, 0):
            date = btc_data.index[i]
            price = btc_data['price'].iloc[i]
            change = btc_data['returns'].iloc[i] * 100
            print(f"   {date.strftime('%m-%d')}: ${price:,.2f} ({change:+.2f}%)")
            
    else:
        print("❌ Failed to fetch Bitcoin data")

if __name__ == "__main__":
    main()
