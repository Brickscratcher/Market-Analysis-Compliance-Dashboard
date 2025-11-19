# Using python_openai blueprint integration
import os
from openai import OpenAI
import streamlit as st

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_openai_client():
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)

@st.cache_data(ttl=1800, show_spinner=False)
def generate_market_summary(news_text):
    client = get_openai_client()
    
    if not client:
        return "⚠️ OpenAI API key not configured. Please add your OPENAI_API_KEY to enable AI-powered market summaries."
    
    try:
        prompt = f"""You are a financial market analyst. Analyze the following market news and provide a concise macro summary covering:
1. Overall market sentiment (bullish/bearish/neutral)
2. Key market drivers and themes
3. Major sector movements
4. Important upcoming events or concerns
5. Brief outlook

Keep the summary under 300 words and focus on actionable insights.

News content:
{news_text[:4000]}
"""
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def is_api_key_configured():
    return OPENAI_API_KEY is not None and OPENAI_API_KEY != ""
