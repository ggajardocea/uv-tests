import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# Define your desired data structure.
class Memory(BaseModel):
    result: str = Field(description="5 insights about the topic")
    topic: str = Field(description="Topic of the conversation")


load_dotenv()

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

PROMPT_MEMORY_INFO = """
    Provide 5 insights about {topic}.
    {format_instructions}
    """


def main():
    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Memory)

    # setup the chat model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)
    message = HumanMessagePromptTemplate.from_template(
        template=PROMPT_MEMORY_INFO,
    )
    chat_prompt = ChatPromptTemplate.from_messages([message])

    # get user input
    topic = input("Enter the topic for the facts: ")

    # generate the response
    print("Generating response...")
    chat_prompt_with_values = chat_prompt.format_prompt(
        topic=topic, format_instructions=parser.get_format_instructions()
    )
    #output = llm(chat_prompt_with_values.to_messages())
    output = llm.invoke(chat_prompt_with_values.to_messages())
    memory = parser.parse(output.content)

    # print the response
    print(f"The 5 insights about {topic} are: \n{memory.result}.")


if __name__ == "__main__":
    main()