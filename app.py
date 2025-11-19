import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

from data_fetcher import get_all_assets_data, STOCK_TICKERS, CRYPTO_IDS
from technical_indicators import (calculate_internal_bar_strength,
                                  add_all_indicators)
from web_scraper import scrape_financial_news, track_keywords_frequency, get_market_keywords
from openai_helper import generate_market_summary, is_api_key_configured

st.set_page_config(page_title="Financial Markets Dashboard",
                   page_icon="📈",
                   layout="wide")

st.title("📈 Financial Markets Dashboard")
st.markdown(
    "Real-time analytics for S&P 500, Dow Jones, Nasdaq, Bitcoin, and Ethereum"
)

with st.sidebar:
    st.header("⚙️ Settings")

    auto_refresh = st.checkbox("Auto Refresh Data", value=False)
    if auto_refresh:
        st.info("Data refreshes every 5 minutes")

    st.markdown("---")
    st.markdown("### Assets Tracked")
    st.markdown("**Indices:**")
    st.markdown("- S&P 500")
    st.markdown("- Dow Jones")
    st.markdown("- Nasdaq")
    st.markdown("**Cryptocurrencies:**")
    st.markdown("- Bitcoin")
    st.markdown("- Ethereum")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Internal Bar Strength", "📈 Volume Analysis", "💹 Interactive Charts",
    "📰 News & AI Summary", "🔍 Keyword Tracker"
])

with tab1:
    st.header("Daily Internal Bar Strength (30 Days)")
    st.markdown(
        "*Measures where the closing price falls within the day's range. Positive values indicate strength (close near high), negative values indicate weakness (close near low).*"
    )

    with st.spinner("Loading market data..."):
        data_30d = get_all_assets_data(days=30)

    if data_30d:
        colors = {
            'S&P 500': '#1f77b4',
            'Dow Jones': '#ff7f0e',
            'Nasdaq': '#2ca02c',
            'Bitcoin': '#d62728',
            'Ethereum': '#9467bd'
        }

        st.subheader("📊 Market Indices")

        indices = ['S&P 500', 'Dow Jones', 'Nasdaq']
        for asset_name in indices:
            if asset_name in data_30d:
                df = data_30d[asset_name]
                ibs = calculate_internal_bar_strength(df)

                if ibs is not None:
                    avg_ibs = ibs.mean()
                    recent_ibs = ibs.iloc[-1] if len(ibs) > 0 else 0
                    max_ibs = ibs.max()
                    min_ibs = ibs.min()

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        fig = go.Figure()

                        fig.add_trace(
                            go.Scatter(
                                x=ibs.index,
                                y=ibs.values,
                                mode='lines+markers',
                                name=asset_name,
                                line=dict(color=colors.get(asset_name),
                                          width=2.5),
                                marker=dict(size=5),
                                fill='tozeroy',
                                fillcolor=
                                f'rgba{tuple(list(int(colors.get(asset_name)[i:i+2], 16) for i in (1, 3, 5)) + [0.1])}'
                            ))

                        fig.add_hline(y=0,
                                      line_dash="dash",
                                      line_color="gray",
                                      opacity=0.5)

                        fig.update_layout(
                            title=f"{asset_name} Internal Bar Strength",
                            xaxis_title="Date",
                            yaxis_title="IBS (%)",
                            hovermode='x',
                            height=300,
                            showlegend=False,
                            margin=dict(l=50, r=20, t=40, b=40))

                        st.plotly_chart(fig, width='stretch')

                    with col2:
                        st.metric("Current IBS", f"{recent_ibs:.1f}%")
                        st.metric("30D Average", f"{avg_ibs:.1f}%")
                        st.metric("30D High", f"{max_ibs:.1f}%")
                        st.metric("30D Low", f"{min_ibs:.1f}%")

                    st.markdown("---")

        st.subheader("₿ Cryptocurrencies")

        cryptos = ['Bitcoin', 'Ethereum']
        for asset_name in cryptos:
            if asset_name in data_30d:
                df = data_30d[asset_name]
                ibs = calculate_internal_bar_strength(df)

                if ibs is not None:
                    avg_ibs = ibs.mean()
                    recent_ibs = ibs.iloc[-1] if len(ibs) > 0 else 0
                    max_ibs = ibs.max()
                    min_ibs = ibs.min()

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        fig = go.Figure()

                        fig.add_trace(
                            go.Scatter(
                                x=ibs.index,
                                y=ibs.values,
                                mode='lines+markers',
                                name=asset_name,
                                line=dict(color=colors.get(asset_name),
                                          width=2.5),
                                marker=dict(size=5),
                                fill='tozeroy',
                                fillcolor=
                                f'rgba{tuple(list(int(colors.get(asset_name)[i:i+2], 16) for i in (1, 3, 5)) + [0.1])}'
                            ))

                        fig.add_hline(y=0,
                                      line_dash="dash",
                                      line_color="gray",
                                      opacity=0.5)

                        fig.update_layout(
                            title=f"{asset_name} Internal Bar Strength",
                            xaxis_title="Date",
                            yaxis_title="IBS (%)",
                            hovermode='x',
                            height=300,
                            showlegend=False,
                            margin=dict(l=50, r=20, t=40, b=40))

                        st.plotly_chart(fig, width='stretch')

                    with col2:
                        st.metric("Current IBS", f"{recent_ibs:.1f}%")
                        st.metric("30D Average", f"{avg_ibs:.1f}%")
                        st.metric("30D High", f"{max_ibs:.1f}%")
                        st.metric("30D Low", f"{min_ibs:.1f}%")

                    if asset_name != cryptos[-1]:
                        st.markdown("---")
    else:
        st.error("Unable to load market data. Please try again later.")

with tab2:
    st.header("Total Trading Volume (10 Days)")
    st.markdown(
        "*Displays the total trading volume for each asset over the last 10 days.*"
    )

    with st.spinner("Loading volume data..."):
        data_10d = get_all_assets_data(days=10)

    if data_10d:
        fig = go.Figure()

        colors = {
            'S&P 500': '#1f77b4',
            'Dow Jones': '#ff7f0e',
            'Nasdaq': '#2ca02c',
            'Bitcoin': '#d62728',
            'Ethereum': '#9467bd'
        }

        for asset_name, df in data_10d.items():
            if 'volume' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df.index,
                               y=df['volume'],
                               mode='lines+markers',
                               name=asset_name,
                               line=dict(color=colors.get(asset_name),
                                         width=2),
                               marker=dict(size=6)))

        fig.update_layout(title="Trading Volume Over 10 Days",
                          xaxis_title="Date",
                          yaxis_title="Volume",
                          hovermode='x unified',
                          height=600,
                          legend=dict(orientation="h",
                                      yanchor="bottom",
                                      y=1.02,
                                      xanchor="right",
                                      x=1))

        st.plotly_chart(fig, width='stretch')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Volume Statistics")
            for asset_name, df in data_10d.items():
                if 'volume' in df.columns:
                    avg_vol = df['volume'].mean()
                    recent_vol = df['volume'].iloc[-1] if len(df) > 0 else 0

                    st.metric(
                        label=asset_name,
                        value=f"{recent_vol:,.0f}",
                        delta=f"vs Avg: {((recent_vol/avg_vol - 1) * 100):.1f}%"
                    )
    else:
        st.error("Unable to load volume data. Please try again later.")

with tab3:
    st.header("Interactive Price Charts")
    st.markdown(
        "*Customize timeframes and add technical indicators to analyze price movements.*"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_asset = st.selectbox(
            "Select Asset",
            list(STOCK_TICKERS.keys()) + list(CRYPTO_IDS.keys()))

    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year"],
            index=1)

    timeframe_map = {
        "1 Week": 7,
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365
    }

    days = timeframe_map[timeframe]

    st.subheader("Technical Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_sma = st.checkbox("Moving Averages", value=True)
    with col2:
        show_rsi = st.checkbox("RSI", value=False)
    with col3:
        show_macd = st.checkbox("MACD", value=False)
    with col4:
        show_bb = st.checkbox("Bollinger Bands", value=False)

    with st.spinner(f"Loading {selected_asset} data..."):
        data = get_all_assets_data(days=days)

    if data and selected_asset in data:
        df = data[selected_asset].copy()

        indicators = []
        if show_sma:
            indicators.append('SMA')
        if show_rsi:
            indicators.append('RSI')
        if show_macd:
            indicators.append('MACD')
        if show_bb:
            indicators.append('BB')

        df = add_all_indicators(df, indicators=indicators)

        num_subplots = 1
        if show_rsi:
            num_subplots += 1
        if show_macd:
            num_subplots += 1

        subplot_titles = ["Price"]
        if show_rsi:
            subplot_titles.append("RSI")
        if show_macd:
            subplot_titles.append("MACD")

        row_heights = [0.6] + [0.2] * (num_subplots -
                                       1) if num_subplots > 1 else [1.0]

        fig = make_subplots(rows=num_subplots,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.05,
                            subplot_titles=subplot_titles,
                            row_heights=row_heights)

        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'],
                                     name=selected_asset),
                      row=1,
                      col=1)

        if show_sma:
            if 'SMA_20' in df.columns:
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['SMA_20'],
                                         mode='lines',
                                         name='SMA 20',
                                         line=dict(color='orange', width=1)),
                              row=1,
                              col=1)
            if 'SMA_50' in df.columns:
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['SMA_50'],
                                         mode='lines',
                                         name='SMA 50',
                                         line=dict(color='blue', width=1)),
                              row=1,
                              col=1)

        if show_bb:
            if all(col in df.columns
                   for col in ['BB_High', 'BB_Mid', 'BB_Low']):
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['BB_High'],
                                         mode='lines',
                                         name='BB Upper',
                                         line=dict(color='gray',
                                                   width=1,
                                                   dash='dash')),
                              row=1,
                              col=1)
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['BB_Mid'],
                                         mode='lines',
                                         name='BB Mid',
                                         line=dict(color='gray', width=1)),
                              row=1,
                              col=1)
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['BB_Low'],
                                         mode='lines',
                                         name='BB Lower',
                                         line=dict(color='gray',
                                                   width=1,
                                                   dash='dash')),
                              row=1,
                              col=1)

        current_row = 2

        if show_rsi and 'RSI' in df.columns:
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df['RSI'],
                                     mode='lines',
                                     name='RSI',
                                     line=dict(color='purple', width=2)),
                          row=current_row,
                          col=1)
            fig.add_hline(y=70,
                          line_dash="dash",
                          line_color="red",
                          opacity=0.5,
                          row=current_row,
                          col=1)
            fig.add_hline(y=30,
                          line_dash="dash",
                          line_color="green",
                          opacity=0.5,
                          row=current_row,
                          col=1)
            current_row += 1

        if show_macd and all(col in df.columns
                             for col in ['MACD', 'MACD_Signal']):
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df['MACD'],
                                     mode='lines',
                                     name='MACD',
                                     line=dict(color='blue', width=2)),
                          row=current_row,
                          col=1)
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df['MACD_Signal'],
                                     mode='lines',
                                     name='Signal',
                                     line=dict(color='red', width=2)),
                          row=current_row,
                          col=1)
            if 'MACD_Diff' in df.columns:
                fig.add_trace(go.Bar(x=df.index,
                                     y=df['MACD_Diff'],
                                     name='Histogram',
                                     marker_color='gray'),
                              row=current_row,
                              col=1)

        fig.update_layout(title=f"{selected_asset} - {timeframe}",
                          height=800 if num_subplots > 1 else 600,
                          xaxis_rangeslider_visible=False,
                          hovermode='x unified')

        fig.update_xaxes(title_text="Date", row=num_subplots, col=1)
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)

        st.plotly_chart(fig, width='stretch')

        col1, col2, col3, col4 = st.columns(4)

        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        with col1:
            st.metric(
                "Current Price",
                f"${latest['close']:,.2f}",
                delta=f"{((latest['close']/prev['close'] - 1) * 100):.2f}%")
        with col2:
            st.metric("Volume", f"{latest['volume']:,.0f}")
        with col3:
            high_30d = df['high'].max()
            low_30d = df['low'].min()
            st.metric("30D High", f"${high_30d:,.2f}")
        with col4:
            st.metric("30D Low", f"${low_30d:,.2f}")
    else:
        st.error(f"Unable to load data for {selected_asset}")

with tab4:
    st.header("📰 Market News & AI Analysis")

    if not is_api_key_configured():
        st.warning(
            "⚠️ OpenAI API key not configured. Add your OPENAI_API_KEY in the Secrets panel to enable AI-powered summaries."
        )

    col1, col2 = st.columns([2, 1])

    with col2:
        if st.button("🔄 Refresh News", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with st.spinner("Scraping latest market news..."):
        news_content = scrape_financial_news()

    if news_content:
        st.subheader("🤖 AI-Generated Market Summary")

        with st.spinner("Generating AI summary..."):
            summary = generate_market_summary(news_content)

        st.markdown(summary)

        with st.expander("📄 View Raw News Content"):
            st.text_area("Scraped News", news_content, height=300)
    else:
        st.warning(
            "Unable to fetch news at this time. Please try again later.")

with tab5:
    st.header("🔍 Keyword Frequency Tracker")
    st.markdown(
        "*Tracks the frequency of market-relevant keywords from current news sources.*"
    )
    st.info(
        "ℹ️ Historical data (past 30 days) is estimated based on current keyword frequency trends. For accurate historical tracking, a persistent database would be needed."
    )

    default_keywords = get_market_keywords()

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_keywords = st.multiselect("Select Keywords to Track",
                                           default_keywords,
                                           default=default_keywords[:4])

    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    if selected_keywords:
        with st.spinner("Analyzing keyword frequency..."):
            keyword_data, current_counts = track_keywords_frequency(
                selected_keywords, days=30)

        if keyword_data:
            fig = go.Figure()

            colors = [
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                '#8c564b', '#e377c2', '#7f7f7f'
            ]

            for i, (keyword, data) in enumerate(keyword_data.items()):
                dates = sorted(data.keys())
                counts = [data[date] for date in dates]

                fig.add_trace(
                    go.Scatter(x=dates,
                               y=counts,
                               mode='lines+markers',
                               name=keyword.title(),
                               line=dict(color=colors[i % len(colors)],
                                         width=2),
                               marker=dict(size=6)))

            fig.update_layout(title="Keyword Frequency Over 30 Days",
                              xaxis_title="Date",
                              yaxis_title="Frequency Count",
                              hovermode='x unified',
                              height=500,
                              legend=dict(orientation="h",
                                          yanchor="bottom",
                                          y=1.02,
                                          xanchor="right",
                                          x=1))

            st.plotly_chart(fig, width='stretch')

            st.subheader("Current Keyword Statistics")

            cols = st.columns(len(selected_keywords))
            for i, keyword in enumerate(selected_keywords):
                with cols[i]:
                    data = keyword_data[keyword]
                    recent_count = data.get(datetime.now().date(), 0)
                    avg_count = sum(data.values()) / len(data) if data else 0

                    st.metric(label=keyword.title(),
                              value=int(recent_count),
                              delta=f"Avg: {avg_count:.0f}")
        else:
            st.error("Unable to track keywords at this time.")
    else:
        st.info("Please select at least one keyword to track.")

st.markdown("---")
st.caption(
    "💡 Data sources: Yahoo Finance, CoinGecko, Financial News Sites | Refresh intervals: Market data (5 min), News (1 hour), Keywords (24 hours)"
)

if auto_refresh:
    import time
    time.sleep(300)
    st.rerun()
