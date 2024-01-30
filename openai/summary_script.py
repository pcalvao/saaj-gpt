import openai
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

"""This script is used to get the summary of a complete document using langchain
For this we use the file summary.txt that was generated in the results_script_en.py or results_script_pt.py script
"""

# place your OpenAI key here
openai.api_key = "secret"

llm = ChatOpenAI(
    openai_api_key=openai.api_key, model_name="gpt-3.5-turbo", temperature=0.5
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)

# change the path of the document you want to analyse here
with open("../test.txt", "r", encoding="utf-8") as f:
    data = f.read()

text = text_splitter.split_text(data)

docs = [Document(page_content=t) for t in text[:3]]

# this prompt will work with portuguese or english documents
prompt_template = """Escreve um sumário conciso do seguinte texto:


{text}


Responde em português:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

model = load_summarize_chain(
    llm=llm,
    chain_type="refine",
    question_prompt=PROMPT,
)
result = model.run(docs)

"""We save the final summary in a file
"""

print("Start Writting")

with open("final_summary.txt", "w", encoding="utf-8") as f:
    f.flush()
    f.write(result.lstrip())
    f.close()

print("Done Writting")
