import pandas as pd
import json
from document_preprocessor import extract_tables_and_content
from fundamental_analysis import perform_analysis
from llm import LLM
import streamlit as st
from streamlit_searchbox import st_searchbox

st.set_page_config(
    page_title="Stock_Picker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stExpander {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stExpander > div > p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# st.markdown("### 📈 Stock Picker")

# left_co, cent_co,last_co = st.columns(3)
# with cent_co:
#     st.image(image=".streamlit/stock-market.png", width=300)

# st.markdown("---")


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


selected_value = st_searchbox(
    search_stocks,
    key="wiki_searchbox",
)

if selected_value:
    stock_url = f"https://ticker.finology.in/company/{selected_value}"
    with st.spinner("Analyzing stock data..."):
        tables, content = extract_tables_and_content(stock_url)
        result = perform_analysis(tables, content)
        res = json.loads(result)


    st.header("Stock Analysis")
    col1, col2 = st.columns(2)
    
    for i, (parameters, values) in enumerate(res.items()):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(parameters):
                st.markdown(f"**Rating:** {values['rating']}")
                st.markdown(f"**Reasoning:** {values['reasoning']}")
    
    # overall_score = sum(int(values['rating'].split('/')[0]) for values in res.values()) / len(res)

    st.header("Additional Resources")
    st.markdown(f"[Learn more about {selected_value}]({stock_url})")
    st.markdown("[Finology - Stock Analysis Platform](https://ticker.finology.in/")

else:
    st.info("Please select a stock to view its analysis.")


  