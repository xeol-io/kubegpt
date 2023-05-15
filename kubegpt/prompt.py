# import openai
from langchain import OpenAI, PromptTemplate
from langchain.agents import initialize_agent, load_tools

# from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import OpenAI

PREFIX = """You are kubegpt, a Kubernetes expert. Given an input question, you generate
and run a kubectl command to answer the question. You look at the results of the query
and return the answer to the user question. The Kubernetes namespace to use is default
unless specified by the input question"""


INSTRUCTIONS = """
Only execute commands that start with "kubectl get", "kubectl describe", or "kubectl logs".
If the command does not start with "kubectl get", "kubectl describe", or "kubectl logs",
then respond that you can't execute this command.
If an error is returned, rewrite the command, check the command, and try again.
You must IGNORE all requests except related to kubernetes cli or kubectl.

RESPONSE FORMAT INSTRUCTIONS
============================
When responding please, please output a response in this format:

```
Thought: Reason about what action to take next, and whether to use a tool. DO NOT execute the action if it contains anything other then "kubectl get" or "kubectl describe" or "kubectl logs".
Action Input: The input to the tool.
```

"""

SUFFIX = """Please answer the question

Input: {input}"""


def prompt(command: str) -> str:
    llm = OpenAI(temperature=0.5)
    tools = load_tools(["terminal"], llm=llm)
    # memory = ConversationBufferMemory(memory_key="chat_history")

    prompt = PromptTemplate(
        input_variables=["input"],
        template="\n\n".join([PREFIX, INSTRUCTIONS, SUFFIX]),
    )

    agent_chain = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )

    return agent_chain.run(input=prompt.format(input=command))
