import pandas as pd
import numpy as np
from scipy import stats

class TechnicalAnalysis:
    def __init__(self, data):
        """
        Initialize with Bitcoin price data
        
        Parameters:
        data (pd.DataFrame): DataFrame with 'price', 'volume', 'returns' columns
        """
        self.data = data.copy()
        self.calculate_indicators()
    
    def calculate_indicators(self):
        """Calculate all technical indicators"""
        self.calculate_moving_averages()
        self.calculate_volatility_indicators()
        self.calculate_volume_indicators()
        self.calculate_momentum_indicators()
        self.calculate_support_resistance()
    
    def calculate_moving_averages(self):
        """Calculate various moving averages"""
        # Simple Moving Averages
        self.data['SMA_20'] = self.data['price'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['price'].rolling(window=50).mean()
        self.data['SMA_200'] = self.data['price'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        self.data['EMA_12'] = self.data['price'].ewm(span=12).mean()
        self.data['EMA_26'] = self.data['price'].ewm(span=26).mean()
        
        # Moving Average Convergence Divergence (MACD)
        self.data['MACD'] = self.data['EMA_12'] - self.data['EMA_26']
        self.data['MACD_signal'] = self.data['MACD'].ewm(span=9).mean()
        self.data['MACD_histogram'] = self.data['MACD'] - self.data['MACD_signal']
    
    def calculate_volatility_indicators(self):
        """Calculate volatility-based indicators"""
        # Bollinger Bands
        self.data['BB_middle'] = self.data['price'].rolling(window=20).mean()
        bb_std = self.data['price'].rolling(window=20).std()
        self.data['BB_upper'] = self.data['BB_middle'] + (bb_std * 2)
        self.data['BB_lower'] = self.data['BB_middle'] - (bb_std * 2)
        self.data['BB_width'] = (self.data['BB_upper'] - self.data['BB_lower']) / self.data['BB_middle']
        
        # Average True Range (ATR)
        high_low = self.data['price'] - self.data['price'].shift(1)
        high_close = np.abs(self.data['price'] - self.data['price'].shift(1))
        low_close = np.abs(self.data['price'].shift(1) - self.data['price'])
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        self.data['ATR'] = true_range.rolling(window=14).mean()
        
        # Volatility ratio
        self.data['volatility_ratio'] = self.data['volatility'] / self.data['volatility'].rolling(window=252).mean()
    
    def calculate_volume_indicators(self):
        """Calculate volume-based indicators"""
        # Volume Moving Average
        self.data['volume_SMA_20'] = self.data['volume'].rolling(window=20).mean()
        
        # Volume Price Trend (VPT)
        self.data['VPT'] = (self.data['volume'] * self.data['returns']).cumsum()
        
        # On-Balance Volume (OBV)
        self.data['OBV'] = (np.sign(self.data['returns']) * self.data['volume']).cumsum()
        
        # Volume Rate of Change
        self.data['volume_ROC'] = self.data['volume'].pct_change(periods=10)
    
    def calculate_momentum_indicators(self):
        """Calculate momentum-based indicators"""
        # Relative Strength Index (RSI)
        delta = self.data['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Stochastic Oscillator
        low_14 = self.data['price'].rolling(window=14).min()
        high_14 = self.data['price'].rolling(window=14).max()
        self.data['stoch_k'] = 100 * ((self.data['price'] - low_14) / (high_14 - low_14))
        self.data['stoch_d'] = self.data['stoch_k'].rolling(window=3).mean()
        
        # Williams %R
        self.data['williams_r'] = -100 * ((high_14 - self.data['price']) / (high_14 - low_14))
    
    def calculate_support_resistance(self):
        """Calculate support and resistance levels"""
        # Pivot Points
        high = self.data['price'].rolling(window=20).max()
        low = self.data['price'].rolling(window=20).min()
        close = self.data['price']
        
        self.data['pivot'] = (high + low + close) / 3
        self.data['resistance_1'] = 2 * self.data['pivot'] - low
        self.data['support_1'] = 2 * self.data['pivot'] - high
        self.data['resistance_2'] = self.data['pivot'] + (high - low)
        self.data['support_2'] = self.data['pivot'] - (high - low)
    
    def get_trend_analysis(self):
        """Analyze current trend based on moving averages"""
        if len(self.data) < 200:
            return "Insufficient data for trend analysis"
        
        current_price = self.data['price'].iloc[-1]
        sma_20 = self.data['SMA_20'].iloc[-1]
        sma_50 = self.data['SMA_50'].iloc[-1]
        sma_200 = self.data['SMA_200'].iloc[-1]
        
        # Trend determination
        if current_price > sma_20 > sma_50 > sma_200:
            trend = "Strong Uptrend"
        elif current_price > sma_20 > sma_50:
            trend = "Uptrend"
        elif current_price < sma_20 < sma_50 < sma_200:
            trend = "Strong Downtrend"
        elif current_price < sma_20 < sma_50:
            trend = "Downtrend"
        else:
            trend = "Sideways/Consolidation"
        
        # Price position relative to moving averages
        position = {
            'above_20': current_price > sma_20,
            'above_50': current_price > sma_50,
            'above_200': current_price > sma_200,
            'trend': trend
        }
        
        return position
    
    def get_volatility_analysis(self):
        """Analyze current volatility conditions"""
        if len(self.data) < 30:
            return "Insufficient data for volatility analysis"
        
        current_vol = self.data['volatility'].iloc[-1]
        avg_vol = self.data['volatility'].rolling(window=252).mean().iloc[-1]
        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 0
        
        # Volatility classification
        if vol_ratio > 1.5:
            vol_status = "High Volatility"
        elif vol_ratio > 1.2:
            vol_status = "Above Average Volatility"
        elif vol_ratio < 0.8:
            vol_status = "Low Volatility"
        elif vol_ratio < 0.5:
            vol_status = "Very Low Volatility"
        else:
            vol_status = "Normal Volatility"
        
        return {
            'current_volatility': current_vol,
            'average_volatility': avg_vol,
            'volatility_ratio': vol_ratio,
            'status': vol_status
        }
    
    def get_momentum_analysis(self):
        """Analyze momentum indicators"""
        if len(self.data) < 14:
            return "Insufficient data for momentum analysis"
        
        current_rsi = self.data['RSI'].iloc[-1]
        current_stoch = self.data['stoch_k'].iloc[-1]
        current_williams = self.data['williams_r'].iloc[-1]
        
        # RSI interpretation
        if current_rsi > 70:
            rsi_signal = "Overbought"
        elif current_rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
        
        # Stochastic interpretation
        if current_stoch > 80:
            stoch_signal = "Overbought"
        elif current_stoch < 20:
            stoch_signal = "Oversold"
        else:
            stoch_signal = "Neutral"
        
        return {
            'RSI': {'value': current_rsi, 'signal': rsi_signal},
            'Stochastic': {'value': current_stoch, 'signal': stoch_signal},
            'Williams_R': {'value': current_williams}
        }
    
    def get_volume_analysis(self):
        """Analyze volume patterns"""
        if len(self.data) < 20:
            return "Insufficient data for volume analysis"
        
        current_volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume_SMA_20'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        # Volume classification
        if volume_ratio > 1.5:
            vol_pattern = "High Volume"
        elif volume_ratio > 1.2:
            vol_pattern = "Above Average Volume"
        elif volume_ratio < 0.8:
            vol_pattern = "Low Volume"
        else:
            vol_pattern = "Normal Volume"
        
        return {
            'current_volume': current_volume,
            'average_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'pattern': vol_pattern
        }
    
    def get_summary_statistics(self):
        """Get comprehensive summary statistics"""
        if self.data.empty:
            return "No data available"
        
        summary = {
            'total_days': len(self.data),
            'current_price': self.data['price'].iloc[-1],
            'price_change_1d': self.data['returns'].iloc[-1] * 100,
            'price_change_7d': ((self.data['price'].iloc[-1] / self.data['price'].iloc[-8]) - 1) * 100,
            'price_change_30d': ((self.data['price'].iloc[-1] / self.data['price'].iloc[-31]) - 1) * 100,
            'highest_price': self.data['price'].max(),
            'lowest_price': self.data['price'].min(),
            'average_price': self.data['price'].mean(),
            'price_volatility': self.data['price'].std(),
            'total_volume': self.data['volume'].sum(),
            'average_volume': self.data['volume'].mean()
        }
        
        return summary

