from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from unstructured.cleaners.core import remove_punctuation,clean,clean_extra_whitespace

def generate_document(url):
    "Given an URL, return a langchain Document to futher processing"
    loader = UnstructuredURLLoader(urls=[url],
    mode="elements",
    post_processors=[clean,remove_punctuation,clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [e for e in elements]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source":url})