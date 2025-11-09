# chatbot.py
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key in .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Restrict to stock-related queries only
template = """
You are a stock market assistant. Only respond to questions related to stocks, stock prices, trading strategies, companies, market news, or financial terms.

If the user asks anything unrelated to the stock market, say:
"I'm trained only to answer stock-related questions. Please ask something about stocks or finance."

Conversation history:
{history}
User: {input}
AI:"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template,
)

llm = ChatOpenAI(temperature=0.5, openai_api_key=openai_api_key)
memory = ConversationBufferMemory()

chatbot = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
)

def get_chat_response(user_input):
    return chatbot.run(user_input)
