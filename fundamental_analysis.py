import pandas as pd
import logging
from document_preprocessor import extract_tables_and_content
from llm import LLM
from prompt import fundamental_analysis_parameter_prompt, fundamental_analysis_sys_prompt, stock_info_prompt
selected_value = "AVANTIFEED"

logger = logging.getLogger('stock_extraction')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('stock.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

stocks = pd.read_excel("MCAP31122023.xlsx").set_index('Company Name')
url = "https://ticker.finology.in/company/"
model = LLM(model_name="Gemini")
stock_url = f"https://ticker.finology.in/company/{selected_value}"

def perform_analysis(tables, page_content):
    
    logger.info(tables)
    logger.info(page_content)
    prompt_with_stock_info = stock_info_prompt.replace("{stock_info}","\n".join(page_content)).replace("{tables}","\n\n".join(tables)) 

    comp_prompt =  fundamental_analysis_sys_prompt.replace("{stock_parameters}",fundamental_analysis_parameter_prompt)+prompt_with_stock_info
    result = model(prompt=comp_prompt).replace('```json',"")
    logger.info(result)
    return result

if __name__=="__main__":
    result  = perform_analysis(stock_url=stock_url)
