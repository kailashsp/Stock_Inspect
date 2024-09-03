import streamlit as st
import pandas as pd
from document_preprocessor import extract_tables_and_content
from llm import LLM
from streamlit_searchbox import st_searchbox

st.set_page_config(page_title="Company Financials", page_icon="📈", layout="wide")

st.title("📈 Stock Financials Dashboard")

@st.cache_data
def stocks_list():
    return pd.read_excel("MCAP31122023.xlsx").set_index('Company Name')

stocks = stocks_list()
url = "https://ticker.finology.in/company/"
model = LLM(model_name="Gemini")

# function with list of labels
def search_stocks(searchterm: str):
    if not searchterm:
        return []
    matching_stocks = stocks[stocks.index.str.contains(searchterm, case=False, na=False)]
    return matching_stocks['Symbol'].tolist()

st.write("Select an Option:")
selected_value = st_searchbox(
    search_stocks,
    key="wiki_searchbox",
)

if selected_value:
    stock_url = f"https://ticker.finology.in/company/{selected_value}"

    with st.spinner("Fetching stock data..."):
        tables, content = extract_tables_and_content(stock_url)
    st.success(f"Data fetched for {selected_value}")

    st.header("Financial Tables")
    for i, table in enumerate(tables):
        with st.expander(f"Table {i+1}"):
            st.markdown(table)

    st.header("Financial Analysis")
    analysis_prompt = f"Provide a brief financial analysis of {selected_value} based on the following data:\n\n{tables}"
    
    with st.spinner("Generating financial analysis..."):
        analysis = model(analysis_prompt)
    
    st.write(analysis)

else:
    st.info("Please select a stock to view its financial information.")