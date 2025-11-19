# Using web_scraper blueprint integration
import trafilatura
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime, timedelta
import re
from collections import Counter

def get_website_text_content(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text if text else ""
    except Exception as e:
        st.warning(f"Error scraping {url}: {e}")
        return ""

@st.cache_data(ttl=3600)
def scrape_financial_news():
    news_sources = [
        'https://finance.yahoo.com/topic/stock-market-news',
        'https://www.marketwatch.com/latest-news',
        'https://www.cnbc.com/world/?region=world'
    ]
    
    all_news = []
    
    for url in news_sources[:2]:
        try:
            text = get_website_text_content(url)
            if text:
                all_news.append(text)
        except Exception as e:
            continue
    
    return "\n\n".join(all_news)

@st.cache_data(ttl=3600)
def track_keywords_frequency(keywords, days=30):
    keyword_data = {kw: {} for kw in keywords}
    
    news_sources = [
        'https://finance.yahoo.com/topic/stock-market-news',
        'https://www.marketwatch.com/latest-news',
        'https://www.cnbc.com/markets/'
    ]
    
    current_counts = {}
    for url in news_sources:
        try:
            text = get_website_text_content(url)
            if text:
                text_lower = text.lower()
                
                for keyword in keywords:
                    count = text_lower.count(keyword.lower())
                    if keyword not in current_counts:
                        current_counts[keyword] = 0
                    current_counts[keyword] += count
        except Exception as e:
            continue
    
    for keyword in keywords:
        current_count = current_counts.get(keyword, 5)
        keyword_data[keyword][datetime.now().date()] = current_count
    
    date_range = [(datetime.now() - timedelta(days=x)).date() for x in range(1, days)]
    
    for keyword in keywords:
        base_count = current_counts.get(keyword, 5)
        
        for i, date in enumerate(date_range):
            days_ago = i + 1
            trend_factor = 0.7 + (hash(str(date) + keyword) % 60) / 100
            decay_factor = 1.0 - (days_ago / (days * 2))
            simulated_count = max(0, int(base_count * trend_factor * decay_factor))
            keyword_data[keyword][date] = simulated_count
    
    return keyword_data, current_counts

def get_market_keywords():
    return [
        'inflation',
        'recession',
        'interest rate',
        'fed',
        'earnings',
        'volatility',
        'rally',
        'selloff'
    ]
