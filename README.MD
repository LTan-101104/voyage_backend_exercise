## Install packages:

Make sure to create a virtual environment and run the following command

pip install langchain_community pdfminer.six ollama fastapi uvicorn python-multipart PyPDF2 motor pydantic

## Important Note about Ollama
To run Ollama properly, you have to use Ollama CLI to pull llama3 model. This should be really quick and easy. This is required to run the extractor code properly.

Follow this link to install : https://ollama.com

Then it will guide you how to pull down llama 3.2 model, which is sufficient for this project.

## Run the app
Use uvicorn app:app --reload to run the app

