from key import openai_api_key
import os
import pandas as pd
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import load_tools
from langchain.agents import initialize_agent
import openai
import argparse
from io import StringIO

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv('OPENAI_API_KEY')

parser = argparse.ArgumentParser()

parser.add_argument('--source')
parser.add_argument('--template')
parser.add_argument('--target')

args = parser.parse_args()

source = pd.read_csv(args.source)
template = pd.read_csv(args.template)
target = pd.read_csv(args.target)

template_copy = template.copy()
template_copy = template_copy.astype(str)
template_copy = ','.join(template_copy)
source_copy_str = source.copy()
source_copy_str = source_copy_str.astype(str)

source = source.iloc[:1].astype(str)
template = template.iloc[:4].astype(str)



source = ','.join(source) + '\n' + ','.join(source.loc[0])
template = ','.join(template) + '\n' + ','.join(template.loc[0]) + '\n' + ','.join(template.loc[1]) + '\n' + ','.join(template.loc[2]) + '\n' + ','.join(template.loc[3])


completion = openai.ChatCompletion.create(
  model = 'gpt-4',
  messages = [
    {'role': 'user', 'content': 'I have a table with data and a table with a template. Here is an example of the data table {}, and here is an example of the template table {}. Write a Python function called convert_csv_format that will convert a csv formatted string from the data table to the template table format, and return the formatted string in csv format. Take as an example the data format of the template table, spaces, numerical data types, etc and change it. Pay attention to the date format and change it to the template format. Dont import libraries. Show me just a function with no description, comments from you or anything else, just a function in text format.'.format(source, template)}
  ],
  temperature = 0  
)

openai_function = completion['choices'][0]['message']['content']

exec(openai_function)

try:
  for i in range(source_copy_str.shape[0] - 1):
    done_data = ','.join(source_copy_str.iloc[i, :])
    template_copy += '\n' + convert_csv_format(done_data)

except Exception:
  print("Something went wrong!")

data = StringIO(template_copy)
dataframe_for_save = pd.read_csv(data)
dataframe_for_save.to_csv(args.target, index=False)