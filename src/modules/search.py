# this is for searching stuffs
#import pydantic
from typing import Optional

from langchain.agents import (AgentType, OpenAIFunctionsAgent, Tool,
                              initialize_agent, load_tools)
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
# from langchain.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
import json
from langchain.pydantic_v1 import BaseModel, Field, validator


# import load dotenv
from dotenv import load_dotenv

system_message = SystemMessage(content="You are very powerful assistant, but bad at calculating lengths of words.")

# example 

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5




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
    
def getProducts(info: ProductScope, verbose: Optional[bool] = False):
    load_dotenv()
    llm = ChatOpenAI(temperature=0,model="gpt-3.5-turbo-0613")
    # search = GoogleSerperAPIWrapper()
    tools = load_tools(["serpapi"], llm=llm)


    # tools = [
    #     Tool(
    #         name="Intermediate Answer",
    #         func=search.run,
    #         description="useful for when you need to ask with search",
    #     )
    # ]
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=verbose)
    # parser = CommaSeparatedListOutputParser()

    parser = PydanticOutputParser(pydantic_object=ProductsLists)
    
    prompt = PromptTemplate(
        template="Search top 3 for match the description in the {product_scope} \n{format_instructions}\n\n",
        input_variables=["product_scope"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    _input = prompt.format_prompt(product_scope=json.dumps(info.dict()))
    print(_input)

    _output = agent.run(_input)


    return parser.parse(_output)

