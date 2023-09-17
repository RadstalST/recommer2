import json
from typing import Optional

from langchain.agents import (AgentType, OpenAIFunctionsAgent, Tool,
                              initialize_agent, load_tools)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import (CommaSeparatedListOutputParser,
                                      PydanticOutputParser)
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               PromptTemplate)
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.schema import SystemMessage
from langchain.utilities import SerpAPIWrapper
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper, SQLDatabase

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class ProductScope(BaseModel):
    desire: str
    tags: list[str]
    description: str = "not available"
class ProductInfo(BaseModel):
    name: str= Field(description="name of the product")
    # link: str
    description: str= Field(description="description of the product")

class ProductsLists(BaseModel):
    products : list[ProductInfo]

class productAttribute(BaseModel):
  product_cat: str = Field(description="The input product category")
  product_type: str = Field(description="Identify what type of product")
  list_attribute: list[str] = Field(description="list of attributes")
    
def getProducts(info: ProductScope, verbose: Optional[bool] = False)->ProductsLists:
    llm = ChatOpenAI(temperature=0,model="gpt-4")
    # search = GoogleSerperAPIWrapper()
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS , memory=memory,verbose=verbose)
    parser = PydanticOutputParser(pydantic_object=ProductsLists)
    prompt = PromptTemplate(
        template="What are the top 5 for match the description :{product_scope} \n that matches the format. {format_instructions}\n\n",
        input_variables=["product_scope"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    _input = prompt.format_prompt(product_scope=f"{info.dict()}",format_instructions=parser.get_format_instructions())
    _output = agent.run(_input.to_string())
    # pass
    return parser.parse(_output)

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

