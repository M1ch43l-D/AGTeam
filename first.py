import os
import dotenv
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

dotenv.load_dotenv()
assert os.environ.get("OPENAI_API_KEY")

config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-4-32k-v0314"],
    },
)
gpt4_config = {
    "cache_seed": 45,
    "temperature": 0,
    "config_list": config_list_gpt4,
    "timeout": 600,
}

# Admin
user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message="A human admin.",
   code_execution_config=False,
)

# Market Researcher
market_researcher = autogen.AssistantAgent(
    name="MarketResearcher",
    llm_config=gpt4_config,
    system_message="Market Researcher. Analyze market trends, customer needs, and competitor strategies. Brainstorm complementary app concepts as needed. Provide insights to guide the development and positioning of the app.",
)

# Business Model Architect
business_model_architect = autogen.AssistantAgent(
    name="BusinessModelArchitect",
    llm_config=gpt4_config,
    system_message="Business Model Architect. Design viable business models, develop monetization strategies, and conduct financial forecasting. Align business strategies with market research findings.",
)

# Technical Lead
technical_lead = autogen.AssistantAgent(
    name="TechnicalLead",
    llm_config=gpt4_config,
    system_message="Technical Lead. Oversee technical development and advise on technology stack and feasibility. Ensure technical solutions align with business goals and market needs.",
)

# Brand Strategist
brand_strategist = autogen.AssistantAgent(
    name="BrandStrategist",
    llm_config=gpt4_config,
    system_message="Brand Strategist. Develop branding and positioning strategies. Create a unique brand identity and messaging that resonates with the target audience.",
)

# Creating the group chat with the new team configuration
groupchat = autogen.GroupChat(
    agents=[
        user_proxy, 
        market_researcher, 
        business_model_architect, 
        technical_lead, 
        brand_strategist
    ], 
    messages=[], 
    max_round=50
)

# Manager for the group chat
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

# Initiating the chat
user_proxy.initiate_chat(
    manager,
    message="""
    brainstorm ideas for a cybersecurity Saas app choose the top 3 ideas and progress the ideas 
    """,
)
