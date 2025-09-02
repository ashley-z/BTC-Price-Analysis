#!/usr/bin/env python3
"""
Test script for Bitcoin Price Analysis Dashboard
This script tests the data fetching and technical analysis functionality
"""

import sys
import traceback
from datetime import datetime

def test_data_fetcher():
    """Test the data fetcher module"""
    print("Testing Data Fetcher...")
    print("=" * 50)
    
    try:
        from data_fetcher import DataFetcher
        
        fetcher = DataFetcher()
        
        # Test Bitcoin data fetching
        print("Fetching Bitcoin data...")
        btc_data = fetcher.fetch_bitcoin_data(days=30)  # Test with 30 days first
        
        if btc_data is not None and not btc_data.empty:
            print(f"✅ Successfully fetched {len(btc_data)} days of Bitcoin data")
            print(f"   Date range: {btc_data.index[0].date()} to {btc_data.index[-1].date()}")
            print(f"   Current price: ${btc_data['price'].iloc[-1]:,.2f}")
            print(f"   Data columns: {list(btc_data.columns)}")
            print()
        else:
            print("❌ Failed to fetch Bitcoin data")
            return False
        
        # Test traditional market data fetching
        print("Fetching traditional market data...")
        end_date = datetime.now()
        start_date = end_date.replace(day=1)  # Start of current month
        market_data = fetcher.fetch_traditional_markets(start_date, end_date)
        
        if market_data is not None and not market_data.empty:
            print(f"✅ Successfully fetched traditional market data")
            print(f"   Markets: {list(market_data.columns)}")
            print(f"   Date range: {market_data.index[0].date()} to {market_data.index[-1].date()}")
            print()
        else:
            print("⚠️  Traditional market data fetch failed (this is optional)")
            market_data = None
        
        # Test correlation calculation
        if market_data is not None:
            print("Calculating correlations...")
            correlations = fetcher.calculate_correlations(btc_data, market_data)
            
            if correlations:
                print("✅ Correlations calculated successfully:")
                for market, corr in correlations.items():
                    print(f"   {market}: {corr:.4f}")
                print()
            else:
                print("⚠️  Correlation calculation failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data fetcher: {e}")
        traceback.print_exc()
        return False

def test_technical_analysis():
    """Test the technical analysis module"""
    print("Testing Technical Analysis...")
    print("=" * 50)
    
    try:
        from data_fetcher import DataFetcher
        from technical_analysis import TechnicalAnalysis
        
        # Get some data first
        fetcher = DataFetcher()
        btc_data = fetcher.fetch_bitcoin_data(days=100)  # Need enough data for indicators
        
        if btc_data is None or btc_data.empty:
            print("❌ No Bitcoin data available for technical analysis test")
            return False
        
        print(f"Testing with {len(btc_data)} days of data...")
        
        # Initialize technical analysis
        ta = TechnicalAnalysis(btc_data)
        print("✅ Technical analysis initialized successfully")
        
        # Test trend analysis
        print("\nTesting trend analysis...")
        trend_analysis = ta.get_trend_analysis()
        if isinstance(trend_analysis, dict):
            print(f"   Trend: {trend_analysis.get('trend', 'N/A')}")
            print(f"   Above 20MA: {trend_analysis.get('above_20', 'N/A')}")
            print(f"   Above 50MA: {trend_analysis.get('above_50', 'N/A')}")
            print(f"   Above 200MA: {trend_analysis.get('above_200', 'N/A')}")
        else:
            print(f"   Trend analysis result: {trend_analysis}")
        
        # Test volatility analysis
        print("\nTesting volatility analysis...")
        vol_analysis = ta.get_volatility_analysis()
        if isinstance(vol_analysis, dict):
            print(f"   Status: {vol_analysis.get('status', 'N/A')}")
            print(f"   Current volatility: {vol_analysis.get('current_volatility', 'N/A'):.4f}")
            print(f"   Volatility ratio: {vol_analysis.get('volatility_ratio', 'N/A'):.2f}")
        else:
            print(f"   Volatility analysis result: {vol_analysis}")
        
        # Test momentum analysis
        print("\nTesting momentum analysis...")
        momentum_analysis = ta.get_momentum_analysis()
        if isinstance(momentum_analysis, dict):
            rsi = momentum_analysis.get('RSI', {})
            stoch = momentum_analysis.get('Stochastic', {})
            print(f"   RSI: {rsi.get('value', 'N/A'):.2f} ({rsi.get('signal', 'N/A')})")
            print(f"   Stochastic: {stoch.get('value', 'N/A'):.2f} ({stoch.get('signal', 'N/A')})")
        else:
            print(f"   Momentum analysis result: {momentum_analysis}")
        
        # Test volume analysis
        print("\nTesting volume analysis...")
        volume_analysis = ta.get_volume_analysis()
        if isinstance(volume_analysis, dict):
            print(f"   Pattern: {volume_analysis.get('pattern', 'N/A')}")
            print(f"   Volume ratio: {volume_analysis.get('volume_ratio', 'N/A'):.2f}")
        else:
            print(f"   Volume analysis result: {volume_analysis}")
        
        # Test summary statistics
        print("\nTesting summary statistics...")
        summary = ta.get_summary_statistics()
        if isinstance(summary, dict):
            print(f"   Total days: {summary.get('total_days', 'N/A')}")
            print(f"   Current price: ${summary.get('current_price', 'N/A'):,.2f}")
            print(f"   1-day change: {summary.get('price_change_1d', 'N/A'):+.2f}%")
            print(f"   7-day change: {summary.get('price_change_7d', 'N/A'):+.2f}%")
            print(f"   30-day change: {summary.get('price_change_30d', 'N/A'):+.2f}%")
        else:
            print(f"   Summary statistics result: {summary}")
        
        print("\n✅ Technical analysis tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing technical analysis: {e}")
        traceback.print_exc()
        return False

def test_dashboard_imports():
    """Test that dashboard dependencies can be imported"""
    print("Testing Dashboard Imports...")
    print("=" * 50)
    
    try:
        import dash
        print(f"✅ Dash imported successfully (version: {dash.__version__})")
        
        import dash_bootstrap_components as dbc
        print(f"✅ Dash Bootstrap Components imported successfully")
        
        import plotly
        print(f"✅ Plotly imported successfully (version: {plotly.__version__})")
        
        import pandas as pd
        print(f"✅ Pandas imported successfully (version: {pd.__version__})")
        
        import numpy as np
        print(f"✅ NumPy imported successfully (version: {np.__version__})")
        
        print("\n✅ All dashboard dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please install missing dependencies with: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run all tests"""
    print("Bitcoin Price Analysis Dashboard - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test dashboard imports first
    if not test_dashboard_imports():
        print("\n❌ Dashboard import tests failed. Please fix dependencies first.")
        return False
    
    print()
    
    # Test data fetcher
    if not test_data_fetcher():
        print("\n❌ Data fetcher tests failed.")
        return False
    
    print()
    
    # Test technical analysis
    if not test_technical_analysis():
        print("\n❌ Technical analysis tests failed.")
        return False
    
    print()
    print("🎉 All tests passed successfully!")
    print("The dashboard should work correctly now.")
    print(f"\nTo start the dashboard, run: python dashboard.py")
    print("Then open your browser to: http://127.0.0.1:8050")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

