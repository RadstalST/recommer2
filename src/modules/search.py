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
from langchain.memory import ConversationBufferMemory

from langchain.utilities import SerpAPIWrapper





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
    # parser = CommaSeparatedListOutputParser() 

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

