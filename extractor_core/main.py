from pdfminer.high_level import extract_text
from extractor_core.json_helper import InputData as input
#!inspired by https://huggingface.co/foduucom/resume-extractor
def extract_text_from_pdf(pdf_path):
    #! is you are able to extract text from any general file then you can solve the problem of different file type and you don't have to store the resume on your machine
    return extract_text(pdf_path)

def parse_data(path_file):
    text = extract_text_from_pdf(path_file)
    llm = input.llm()
    data = llm.invoke(input.input_data(text))
    print(type(data))
    print(data)
    return data

def parse_text(text):
    llm = input.llm()
    data = llm.invoke(input.input_data(text))
    print(type(data))
    print(data) #!this is a string
    return data


