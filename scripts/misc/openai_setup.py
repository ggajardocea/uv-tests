import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print("✅ OpenAI API key loaded successfully!")
    print(f"Key starts with: {openai_api_key[:8]}...")
    
    # Set it as an environment variable for other libraries
    os.environ['OPENAI_API_KEY'] = openai_api_key
    
    # Now you can use it with LangChain
    try:
        from langchain_openai import ChatOpenAI
        
        # Initialize the chat model
        chat_model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=openai_api_key  # You can also pass it directly
        )
        
        print("✅ ChatOpenAI model initialized successfully!")
        print(f"Model: {chat_model.model_name}")
        
    except ImportError as e:
        print(f"❌ Error importing langchain_openai: {e}")
        print("Make sure you have installed the required packages:")
        print("uv add langchain-openai")
        
else:
    print("❌ OpenAI API key not found!")
    print("Please create a .env file in your project root with:")
    print("OPENAI_API_KEY=your_actual_api_key_here")
    print("\nOr set it as an environment variable:")
    print("export OPENAI_API_KEY=your_actual_api_key_here") 