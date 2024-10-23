import openai,json,tiktoken
from dotenv import load_dotenv 
import scraper
from scraper import get_all_links

load_dotenv()

tools = [
    {
        "type":"function",
        "function": {
            "name":"scrape",
            "description":"Use this tool to scrape content of webpages",
            "parameters":{
                "type":"object",
                "properties":{
                    "website":{
                        "type":"string",
                        "description":"Name of the website"
                    }
                },
                "required": ["website"],
                "additionalProperties":False,
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name":"get_all_links",
            "description":"Use this tool to get all links in a webpage",
            "parameters":{
                "type":"object",
                "properties":{
                    "website":{
                        "type":"string",
                        "description":"Name of the website"
                    }
                },
                "required": ["website"],
                "additionalProperties":False,
            }
        }
    }
]

model = "gpt-4o-mini"

def call_function_from_module(module, function_name, args):
    # Get the function from the module
    function = getattr(module, function_name, None)
    output = None 
    if function:
        output = function(**args)
    else:
        print(f"Function {function_name} not found in module {module.__name__}")
    return output 

def main(prompt,website):
    messages = [
    {"role":"system","content":"""You are web scraping agent tasked with extracting specific information from a webpage, these specific information will be given by user.Follow these steps 
    1. Scrape the main page using the scrape tool.
    2. check for the required information, if the current page does not contain required information then proceed to step 3
    3. Identify all the links on the current page, you can use the get_all_links tool. Follow all the links which will contain the required information. repeat step 1-3, until required information is found.
    4. Continue following the links. Priotize the links that are more likely to contain the needed information.
    5. Return the data in JSON format once the required information is found, return it in the following format
    {{"source_url":"URL of the website containing the information".
     "required_information":"Extracted information"}}
    6. Abort condition: if no relevant information is found after scraping all links, return a JSON response indicating no data was found {{"error":"Required information not found"}}"""},
    {"role":"user","content": f"{prompt} Website: {website}"}
    ]
    for _ in range(5): 
        response = openai.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
            )
        if response.choices[0].message.content is not None:
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        elif response.choices[0].message.tool_calls is not None:
            tool_calls = response.choices[0].message.tool_calls
            messages.append(response.choices[0].message)
            for tool in tool_calls:
                print(tool.function.name)
                print(tool.function.arguments)
                function_name = tool.function.name
                arguments = json.loads(tool.function.arguments)
                # Example call from a module
                output = call_function_from_module(scraper, function_name, arguments)
                all_links = get_all_links(**arguments)
                response = openai.chat.completions.create(
                    model=model,
                    messages=[{"role":"user","content":f"Summarize the information of above webpage {output}"}],
                    tools=tools,
                )
                output = f"{response.choices[0].message.content} Links: {all_links}"
                function_call_result_message = {
                    "role": "tool",
                    "content": f"{output}",
                    "tool_call_id": tool.id
                }
                messages.append(function_call_result_message)


if __name__ == "__main__":
    import argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt",help="Provide a prompt for scraper")
    parser.add_argument("--website",help="Main website from which scraping needs to be done")
    args = parser.parse_args()
    print(main(args.prompt,args.website))

    
    