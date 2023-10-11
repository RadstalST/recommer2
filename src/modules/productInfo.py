import json
import os
from typing import Optional,Dict
from serpapi import GoogleSearch
from langchain.tools import DuckDuckGoSearchRun

from langchain.agents import (AgentType, OpenAIFunctionsAgent, Tool,
                              initialize_agent, load_tools)
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import (CommaSeparatedListOutputParser,
                                      PydanticOutputParser, ResponseSchema,
                                      StructuredOutputParser)
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               PromptTemplate)
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.schema import SystemMessage
from langchain.utilities import SerpAPIWrapper, SQLDatabase
from pydantic import BaseModel, Field, validator

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class ProductDetail(BaseModel):
    name: str=Field(description="name of the product model")
    detail: str=Field(description="details of the product key feature")
  #  specs: list[str] = Field(description="lists of important specs of the proudcts")

class SalesChannel(BaseModel):
    price: str=Field(description="price range of the product in this channel")
    link: str=Field(description="link to this sales channel")
    deal: str=Field(description="details of the deal")
    

#class ProductDeals(BaseModel):
 #   name: str=Field(description="name of the product model")
  #  channel_dict: Dict[str=Field(description="name of the channel"),SalesChannel]
    

class Pros(BaseModel):
    name: str=Field(description="name of the product model")
    pros: list[str] = Field(description="list of pros short description of the products")

class Cons(BaseModel):
    name: str=Field(description="name of the product model")
    cons: list[str] = Field(description="list of cons of the products")


def getPositiveReviews(productModel:str)->str:
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    llm = ChatOpenAI(temperature=0, model="gpt-4")



    

def getNegativeReviews(productModel:str)->str:
    pass

def getPros(productModel:str)->Pros:
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    parser = PydanticOutputParser(pydantic_object=Pros)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    input_variables=["productModel"],
    template = """
    Objective: Using the tools search for the pros, good qualities, positives of {productModel}
    Tasks:
    1. Use search to find what are the pros or key advantages of {productModel}.
    2. List 10 pros description of this product
    3. output as {format_instructions}
   """,partial_variables={'format_instructions':format_instructions})
    _input = prompt.format_prompt(productModel=productModel,format_instructions=format_instructions)
    _output = agent.run(_input.to_string())
    return parser.parse(_output)

    

def getCons(productModel:str)->list[str]:
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    parser = PydanticOutputParser(pydantic_object=Cons)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    input_variables=["productModel"],
    template = """
    Objective: Using the tools search for the cons of {productModel}
    Tasks:
    1. Search what are the cons or key disadvantage of {productModel}.
    2. List 10 cons of this product
    3. output as {format_instructions}
   """,partial_variables={'format_instructions':format_instructions})
    _input = prompt.format_prompt(productModel=productModel,format_instructions=format_instructions)
    _output = agent.run(_input.to_string())
    return parser.parse(_output)


def getProductDetail(productModel: str,verbose: Optional[bool]=False) ->ProductDetail:
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    parser = PydanticOutputParser(pydantic_object=ProductDetail)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    input_variables=["productModel"],
    template = """
    Objective: Using the tools search for the description of {productModel}
    Tasks:
    1. Search general information of {productModel}. For example, release dates, brand of the product, key selling point and other notable information. 
    2. summarize the information into a short brief description.
    3. output as {format_instructions}
   """,partial_variables={'format_instructions':format_instructions})
    _input = prompt.format_prompt(productModel=productModel,format_instructions=format_instructions)
    _output = agent.run(_input.to_string())
    return parser.parse(_output)



def getProductDeals(productModel:str,location:str)->ProductDeals:
   search = DuckDuckGoSearchRun()
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    tools = [
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to ask with search",
            )
        ]
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    prompt=PromptTemplate(
            input_variables=["productModel","country"],
            template = """
            You are a pro online shopper who wants to find the best deals in {country}.
            Tasks:
            1.Search for 5 online sales channel that is popular in {country} and sells {productModel} 
            2. Look up the price of this sales channel
            3. save the link source
            Output as a table :
            Sales_channel_name| price_range | hyperlink 
            """
        )









