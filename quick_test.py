#!/usr/bin/env python3
"""
Quick test to verify data fetching is working
"""

from data_fetcher import DataFetcher
from datetime import datetime

def main():
    print("🔍 Quick Data Fetch Test")
    print("=" * 40)
    
    fetcher = DataFetcher()
    
    # Test Bitcoin data fetching
    print("Fetching Bitcoin data...")
    btc_data = fetcher.fetch_bitcoin_data(days=30)  # Start with 30 days
    
    if btc_data is not None and not btc_data.empty:
        print(f"✅ Success! Fetched {len(btc_data)} days of data")
        print(f"   Date range: {btc_data.index[0].date()} to {btc_data.index[-1].date()}")
        print(f"   Current price: ${btc_data['price'].iloc[-1]:,.2f}")
        print(f"   Columns: {list(btc_data.columns)}")
        print()
        
        # Show last 5 days of data
        print("Last 5 days of data:")
        print(btc_data.tail()[['price', 'volume', 'returns']].round(4))
        print()
        
        # Show some statistics
        print("Data Statistics:")
        print(f"   Price range: ${btc_data['price'].min():,.2f} - ${btc_data['price'].max():,.2f}")
        print(f"   Average volume: {btc_data['volume'].mean():,.0f}")
        print(f"   Average daily return: {btc_data['returns'].mean()*100:.2f}%")
        print(f"   Volatility: {btc_data['volatility'].mean()*100:.2f}%")
        
    else:
        print("❌ Failed to fetch Bitcoin data")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Data fetching is working correctly!")
        print("The dashboard should now display data properly.")
    else:
        print("\n❌ Data fetching failed. Check the error messages above.")

