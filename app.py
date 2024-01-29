import pandas as pd
import json
from document_preprocessor import generate_document
from llm import LLM
from prompt import stock_analysis_prompt
import streamlit as st
from streamlit_searchbox import st_searchbox

st.set_page_config(
    page_title="Stock_Picker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image=".streamlit/stock-market.png")


stocks = pd.read_excel("MCAP31122023.xlsx").set_index('Symbol')

url = "https://ticker.finology.in/company/"

model = LLM(model_name="Gemini")

# function with list of labels
def search_stocks(searchterm: str):
    if not searchterm:
        return []
    matching_stocks = stocks[stocks.index.str.contains(searchterm, case=False, na=False)]
    return matching_stocks.index.tolist()


selected_value = st_searchbox(
    search_stocks,
    key="wiki_searchbox",
)

if selected_value:
    stock_url = f"https://ticker.finology.in/company/{selected_value}"
    stock_fundamentals = generate_document(stock_url)
    prompt = stock_analysis_prompt.replace(
        "{stock_name}",selected_value).replace("{context}",stock_fundamentals.page_content)
    result = model(prompt=prompt).replace('```',"")
    
    try:
        res = json.loads(result)
        confidence_score = res['buy']
        analysis = res["detailed_analysis"]

        if confidence_score >= 75:
            st.success("High Confidence Score!")
        elif confidence_score > 40:
            st.warning("Moderate Confidence Score.")
        else:
            st.error("Low Confidence Score.")


        col1, col2 = st.columns(2)
        col1.write(f'**Buy Confidence Score:** {str(confidence_score)}')

        with st.expander("See explanation"):
            st.write(f"**Detailed Analysis:** {analysis}")
        st.markdown(f"[Learn more about {selected_value}]({stock_url})")

    except:
        st.write(result)
