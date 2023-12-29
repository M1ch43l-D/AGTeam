import os
import dotenv
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen import GroupChat, GroupChatManager

dotenv.load_dotenv()
assert os.environ.get("OPENAI_API_KEY")

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
    },
)
llm_config = {
    "cache_seed": 44,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

USER_PROXY_PROMPT = "A human admin. Interact with the Product Manager to discuss the plan. Plan execution needs to be approved by this admin."\

ENGINEER_PROMPT = "You are an expert at writing python code. You do not execute your code (that is the responsibility of the FunctionCallingAgent), you only write code for other agents to use or execute. Your code should always be complete and compileable and contained in a python labeled code block. Other agents can't modify your code. So do not suggest incomplete code which requires agents to modify. Don't use a code block if it's not intended to be executed by the agent. If you want the agent to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask agents to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the agent. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. If the error states that a dependency is missing, please install the dependency and try again. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible."

EXECUTOR_PROMPT = "Executor. Execute the code written by the engineer and report the result."

PLANNER_PROMPT = "Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval. The plan may involve an engineer who can write code and a scientist who doesn't write code. Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist."

CRITIC_PROMPT = "Critic. Double check the plan, claims, and code from other agents and provide feedback."

SCIENTIST_PROMPT = "Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code."


user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message=USER_PROXY_PROMPT,
   code_execution_config=False,
)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message=ENGINEER_PROMPT,
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message=EXECUTOR_PROMPT,
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": True,
        },
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=llm_config,
    system_message=SCIENTIST_PROMPT,
)
planner = autogen.AssistantAgent(
    name="Planner",
    llm_config=llm_config,
    system_message=PLANNER_PROMPT,
)
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message=CRITIC_PROMPT,
)
groupchat = autogen.GroupChat(agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="""
find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.
""",
)