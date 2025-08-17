import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Updated imports for the new LangChain structure
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Example 1: Basic HumanMessagePromptTemplate
def basic_human_message_example():
    """Simple example of HumanMessagePromptTemplate"""
    print("=== Example 1: Basic HumanMessagePromptTemplate ===")
    
    # Create a human message template
    human_template = HumanMessagePromptTemplate.from_template(
        "Tell me about {topic}"
    )
    
    # Format it with a value
    formatted_message = human_template.format(topic="artificial intelligence")
    print(f"Formatted message: {formatted_message}")
    print()

# Example 2: ChatPromptTemplate with single message
def chat_template_single_message():
    """ChatPromptTemplate with one human message"""
    print("=== Example 2: ChatPromptTemplate with Single Message ===")
    
    # Create a human message template
    human_message = HumanMessagePromptTemplate.from_template(
        "Explain {concept} in simple terms"
    )
    
    # Create a chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([human_message])
    
    # Format the prompt
    formatted_prompt = chat_prompt.format_prompt(concept="machine learning")
    print(f"Formatted prompt: {formatted_prompt}")
    print()

# Example 3: Multi-message conversation
def multi_message_conversation():
    """ChatPromptTemplate with multiple message types"""
    print("=== Example 3: Multi-Message Conversation ===")
    
    # System message (sets the context/role)
    system_template = SystemMessagePromptTemplate.from_template(
        "You are a helpful coding assistant. Always provide code examples."
    )
    
    # Human message
    human_template = HumanMessagePromptTemplate.from_template(
        "Write a Python function to {task}"
    )
    
    # AI message (previous response)
    ai_template = AIMessagePromptTemplate.from_template(
        "Here's a solution: {code_snippet}"
    )
    
    # Human follow-up
    follow_up_template = HumanMessagePromptTemplate.from_template(
        "Can you explain how {function_name} works?"
    )
    
    # Create chat prompt with multiple messages
    chat_prompt = ChatPromptTemplate.from_messages([
        system_template,
        human_template,
        ai_template,
        follow_up_template
    ])
    
    # Format with values
    formatted_prompt = chat_prompt.format_prompt(
        task="calculate fibonacci numbers",
        code_snippet="def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)",
        function_name="fib"
    )
    print(f"Multi-message prompt: {formatted_prompt}")
    print()

# Example 4: Using with Pydantic models (like your original code)
def pydantic_integration_example():
    """Integration with Pydantic models for structured output"""
    print("=== Example 4: Pydantic Integration ===")
    
    # Define your data structure
    class ProgrammingTip(BaseModel):
        tip: str = Field(description="A useful programming tip")
        language: str = Field(description="Programming language this tip applies to")
        difficulty: str = Field(description="Beginner, Intermediate, or Advanced")
    
    # Create parser
    parser = PydanticOutputParser(pydantic_object=ProgrammingTip)
    
    # Create prompt template
    human_message = HumanMessagePromptTemplate.from_template(
        "Give me a programming tip about {topic}. {format_instructions}"
    )
    
    chat_prompt = ChatPromptTemplate.from_messages([human_message])
    
    # Format with parser instructions
    formatted_prompt = chat_prompt.format_prompt(
        topic="Python decorators",
        format_instructions=parser.get_format_instructions()
    )
    
    print(f"Pydantic prompt: {formatted_prompt}")
    print()

# Example 5: Dynamic conversation building
def dynamic_conversation():
    """Building conversations dynamically"""
    print("=== Example 5: Dynamic Conversation Building ===")
    
    # Base system message
    system_message = SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant. {personality}"
    )
    
    # Human message template
    human_message = HumanMessagePromptTemplate.from_template(
        "{user_input}"
    )
    
    # Create base chat prompt
    base_prompt = ChatPromptTemplate.from_messages([
        system_message,
        human_message
    ])
    
    # Different personalities
    personalities = [
        "Be very formal and professional",
        "Be casual and friendly",
        "Be humorous and witty"
    ]
    
    user_inputs = [
        "What's the weather like?",
        "Tell me a joke",
        "Explain quantum physics"
    ]
    
    for i, (personality, user_input) in enumerate(zip(personalities, user_inputs)):
        print(f"Conversation {i+1} ({personality}):")
        formatted = base_prompt.format_prompt(
            personality=personality,
            user_input=user_input
        )
        print(f"  User: {user_input}")
        print(f"  System: {personality}")
        print()

# Example 6: Template with conditional logic
def conditional_template_example():
    """Template with conditional formatting"""
    print("=== Example 6: Conditional Template ===")
    
    # Human message with conditional content
    human_template = HumanMessagePromptTemplate.from_template(
        """Please help me with {topic}.
        
        {extra_context if extra_context else "Provide a general overview."}
        
        If this is about {topic}, focus on practical examples."""
    )
    
    chat_prompt = ChatPromptTemplate.from_messages([human_template])
    
    # Format with and without extra context
    print("With extra context:")
    formatted1 = chat_prompt.format_prompt(
        topic="data structures",
        extra_context="I'm a beginner programmer."
    )
    print(f"  {formatted1}")
    
    print("\nWithout extra context:")
    formatted2 = chat_prompt.format_prompt(
        topic="algorithms",
        extra_context=""
    )
    print(f"  {formatted2}")
    print()

if __name__ == "__main__":
    print("LangChain Prompt Template Examples\n")
    
    # Run all examples
    basic_human_message_example()
    chat_template_single_message()
    multi_message_conversation()
    pydantic_integration_example()
    dynamic_conversation()
    #conditional_template_example()
    
    print("All examples completed!") 