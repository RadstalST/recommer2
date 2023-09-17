# this is for searching stuffs
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper, SQLDatabase

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import StructuredOutputParser, ResponseSchema



class productAttribute(BaseModel):
  product_cat: str = Field(description="The input product category")
  product_type: str = Field(description="Identify what type of product")
  list_attribute: list[str] = Field(description="list of attributes")

def getAttribute(product_cat):
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=False)
    parser = PydanticOutputParser(pydantic_object=productAttribute)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    input_variables=["product_cat"],
    template = """You are a consumer that wants to buy {product_cat}. 
    1.Identify what is the product category or type.
    2. What  variations, attributes, or important features would you have to consider to find the best product list out 20.
    3.output as {format_instructions}""",
    partial_variables={'format_instructions':format_instructions})
    output = agent.run(prompt.format_prompt(product_cat))
    return output
    


