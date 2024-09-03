import markdownify
from unstructured.partition.html import partition_html
from unstructured.staging.base import elements_to_dicts
url = "https://ticker.finology.in/company/TCS"

strategy = "hi_res" 
model_name = "yolox" 

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


