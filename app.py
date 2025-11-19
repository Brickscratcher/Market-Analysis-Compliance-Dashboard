import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI
import streamlit as st

cg = CoinGeckoAPI()

STOCK_TICKERS = {
    'S&P 500': '^GSPC',
    'Dow Jones': '^DJI',
    'Nasdaq': '^IXIC'
}

CRYPTO_IDS = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum'
}

@st.cache_data(ttl=300)
def get_stock_data(ticker, period='1mo', interval='1d'):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df is not None and not df.empty:
            df.columns = df.columns.str.lower()
            
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                st.error(f"Missing required columns for {ticker}")
                return None
        
        return df
    except Exception as e:
        st.error(f"Error fetching stock data for {ticker}: {e}")
        return None

@st.cache_data(ttl=300)
def get_crypto_data(crypto_id, days=30):
    try:
        data = cg.get_coin_market_chart_by_id(
            id=crypto_id,
            vs_currency='usd',
            days=days
        )
        
        prices = data['prices']
        volumes = data['total_volumes']
        
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        volume_df = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
        volume_df['timestamp'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
        volume_df.set_index('timestamp', inplace=True)
        
        df['volume'] = volume_df['volume']
        
        daily_df = pd.DataFrame()
        daily_df['open'] = df['price'].resample('1D').first()
        daily_df['high'] = df['price'].resample('1D').max()
        daily_df['low'] = df['price'].resample('1D').min()
        daily_df['close'] = df['price'].resample('1D').last()
        daily_df['volume'] = df['volume'].resample('1D').sum()
        
        daily_df = daily_df.dropna()
        
        return daily_df
    except Exception as e:
        st.error(f"Error fetching crypto data for {crypto_id}: {e}")
        return None

def get_all_assets_data(days=30):
    all_data = {}
    
    for name, ticker in STOCK_TICKERS.items():
        df = get_stock_data(ticker, period=f'{days}d', interval='1d')
        if df is not None and not df.empty:
            all_data[name] = df
    
    for name, crypto_id in CRYPTO_IDS.items():
        df = get_crypto_data(crypto_id, days=days)
        if df is not None and not df.empty:
            all_data[name] = df
    
    return all_data
