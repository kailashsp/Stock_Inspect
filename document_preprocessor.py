from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from unstructured.cleaners.core import remove_punctuation,clean,clean_extra_whitespace
import markdownify
from unstructured.partition.html import partition_html
from unstructured.staging.base import elements_to_dicts

strategy = "hi_res" 
model_name = "yolox" 

def generate_document(url):
    "Given an URL, return a langchain Document to futher processing"
    loader = UnstructuredURLLoader(urls=[url],
    mode="elements",
    post_processors=[clean,remove_punctuation,clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [e for e in elements]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source":url})

def extract_tables_and_content(url):

    elements = partition_html(url=url, 
                strategy=strategy, 
                infer_table_structure=True, 
                model_name=model_name)
    elements_dict = elements_to_dicts(elements)
    tables = [ ]
    company_details = []
    for element in elements_dict:
        if element['type']=="NarrativeText":
            company_details.append(element["text"])
        elif element['type']=="Table":
            tables.append(markdownify.markdownify(element["metadata"]["text_as_html"]))

    return tables, company_details