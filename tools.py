from ast import FormattedValue
from unittest import result
from elevenlabs.conversational_ai.conversation import ClientTools
from websockets.typing import Data
from langchain_community.tools import DuckDuckGoSearchRun

def searchWeb(parameters):
    query = parameters.get("query")
    result = DuckDuckGoSearchRun(query=query)
    return result

def save_to_txt(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")

    formatted_data = f"{data}"

    with open(filename, "a" , encoding="utf-8") as file:
        file.write(formatted_data+"\n")

def create_html_file(parameters):
    filename = parameters.get("filename")
    data= parameters.get("data")
    title = parameters.get("title")

    formatted_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <div>{data}</div>
    </body>
    </html>
    """
    with open(filename, "w" , encoding="utf-8") as file:
        file.write(formatted_html)



client_tools = ClientTools()
client_tools.register("searchWeb",searchWeb)
client_tools.register("saveToTxt",save_to_txt)
client_tools.register("createHTMLFile",create_html_file)
