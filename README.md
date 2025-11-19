Financial Markets Dashboard
Overview
A comprehensive Streamlit-based financial markets dashboard that tracks and visualizes real-time data for S&P 500, Dow Jones, Nasdaq, Bitcoin, and Ethereum. The dashboard features advanced analytics, technical indicators, AI-powered news summaries, and keyword frequency tracking.

Created: November 9, 2025
Status: Functional and ready for use; missing openai api key, so queries will not track

Features
1. Internal Bar Strength (30 Days)
Visualizes daily internal bar strength for all 5 assets
Measures where closing price falls within the day's trading range
Positive values indicate bullish strength, negative values indicate bearish weakness
Line graph with color-coded assets
2. Volume Analysis (10 Days)
Displays total trading volume trends over the last 10 days
Shows volume statistics with comparisons to average
Multi-asset line chart visualization
3. Interactive Price Charts
Customizable candlestick charts for each asset
Timeframe selection: 1 Week, 1 Month, 3 Months, 6 Months, 1 Year
Technical indicators:
Moving Averages (SMA 20, SMA 50)
Relative Strength Index (RSI)
Moving Average Convergence Divergence (MACD)
Bollinger Bands
Real-time price metrics (Current Price, Volume, 30D High/Low)
4. News Aggregator & AI Analysis
Automatically scrapes financial news from multiple sources
AI-powered market summary using OpenAI GPT-5 (requires API key)
Provides macro market analysis, sentiment, and outlook
View raw news content option
5. Keyword Frequency Tracker
Tracks market-relevant keywords from news sources
Visualizes frequency trends over 30 days
Pre-configured keywords: inflation, recession, interest rate, fed, earnings, volatility, rally, selloff
Note: Historical data is estimated based on current trends; real tracking requires persistent storage
Technical Architecture
Data Sources
Stock Market Data: Yahoo Finance via yfinance library
S&P 500 (^GSPC)
Dow Jones (^DJI)
Nasdaq (^IXIC)
Cryptocurrency Data: CoinGecko API via pycoingecko
Bitcoin (BTC)
Ethereum (ETH)
Data resampled to daily OHLC bars
News Content: Web scraping via trafilatura
Yahoo Finance, MarketWatch, CNBC
AI Summaries: OpenAI GPT-5 (optional, requires API key)
Technology Stack
Framework: Streamlit
Data Processing: Pandas, NumPy
Visualization: Plotly (interactive charts)
Technical Analysis: ta library (RSI, MACD, SMA, Bollinger Bands)
Web Scraping: Trafilatura, BeautifulSoup
AI Integration: OpenAI API (GPT-5)
Project Structure
.
├── app.py                     # Main Streamlit application
├── data_fetcher.py            # Stock and crypto data fetching
├── technical_indicators.py    # Technical analysis calculations
├── web_scraper.py             # News scraping and keyword tracking
├── openai_helper.py           # AI summary generation
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── replit.md                  # This documentation

Key Implementation Details
Data Normalization
Stock data columns normalized to lowercase for consistency
Crypto data resampled from hourly to daily OHLC bars
All DataFrames follow standard OHLC format: open, high, low, close, volume
Caching Strategy
Market data cached for 5 minutes (TTL: 300s)
News content cached for 1 hour (TTL: 3600s)
Keyword tracking cached for 1 hour (TTL: 3600s)
AI summaries cached for 30 minutes (TTL: 1800s)
Error Handling
Graceful degradation when data sources are unavailable
Missing API key handling with clear user notifications
Column validation for data integrity
Configuration
Required Environment Variables
OPENAI_API_KEY (optional): OpenAI API key for AI-powered market summaries
Get your key from: https://platform.openai.com
Without this key, the AI summary feature will show a warning but other features remain functional
Auto-Refresh
Optional auto-refresh toggle in sidebar
Refreshes data every 5 minutes when enabled
Usage
The dashboard runs on port 5000 and is accessible via the webview. Navigate through the 5 tabs to explore different analytics:

Internal Bar Strength: View strength/weakness trends across all assets
Volume Analysis: Monitor trading volume patterns
Interactive Charts: Deep dive into individual assets with technical indicators
News & AI Summary: Stay updated with market news and AI insights
Keyword Tracker: Track market sentiment through keyword frequency
Recent Changes
November 9, 2025: Initial implementation with all core features
Fixed stock data column normalization (lowercase)
Implemented proper crypto data resampling to daily OHLC
Added transparency disclaimers for keyword tracking historical estimates
Updated Plotly charts to use new width parameter (deprecated use_container_width)
Known Limitations
Keyword Tracking: Historical data (past 30 days) is estimated based on current frequency trends. For accurate historical tracking, a persistent database would be required.
CoinGecko API: Rate limits may apply for high-frequency usage
News Scraping: Depends on website structure; may break if sites change their HTML
Future Enhancements
Implement persistent storage for real historical keyword tracking (SQLite or cloud KV store)
Add user watchlists for custom asset tracking
Create alert system for price movements and keyword frequency thresholds
Add portfolio tracking functionality
Implement data export capabilities (CSV, PDF reports)
Add sentiment analysis visualization from news sources
Dependencies
streamlit
yfinance
plotly
ta (technical analysis)
pycoingecko
beautifulsoup4
trafilatura
openai
pandas
requests
