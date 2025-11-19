import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_internal_bar_strength(df):
    if df is None or df.empty:
        return None
    
    try:
        df = df.copy()
        
        df['range'] = df['high'] - df['low']
        df['close_position'] = (df['close'] - df['low']) / df['range']
        
        df['close_position'] = df['close_position'].fillna(0.5)
        
        df['internal_bar_strength'] = (df['close_position'] - 0.5) * 100
        
        return df['internal_bar_strength']
    except Exception as e:
        print(f"Error calculating internal bar strength: {e}")
        return None

def add_moving_averages(df, periods=[20, 50]):
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    for period in periods:
        if len(df) >= period:
            sma = SMAIndicator(close=df['close'], window=period)
            df[f'SMA_{period}'] = sma.sma_indicator()
    
    return df

def add_rsi(df, window=14):
    if df is None or df.empty or len(df) < window:
        return df
    
    df = df.copy()
    
    rsi = RSIIndicator(close=df['close'], window=window)
    df['RSI'] = rsi.rsi()
    
    return df

def add_macd(df):
    if df is None or df.empty or len(df) < 26:
        return df
    
    df = df.copy()
    
    macd = MACD(close=df['close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Diff'] = macd.macd_diff()
    
    return df

def add_bollinger_bands(df, window=20):
    if df is None or df.empty or len(df) < window:
        return df
    
    df = df.copy()
    
    bb = BollingerBands(close=df['close'], window=window)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Mid'] = bb.bollinger_mavg()
    df['BB_Low'] = bb.bollinger_lband()
    
    return df

def add_all_indicators(df, indicators=['SMA', 'RSI', 'MACD', 'BB']):
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    if 'SMA' in indicators:
        df = add_moving_averages(df, periods=[20, 50])
    
    if 'RSI' in indicators:
        df = add_rsi(df)
    
    if 'MACD' in indicators:
        df = add_macd(df)
    
    if 'BB' in indicators:
        df = add_bollinger_bands(df)
    
    return df
