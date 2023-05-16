from langchain import PromptTemplate
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.chat_models import ChatOpenAI

INSTRUCTIONS = """
You are kubegpt, a Kubernetes expert. Given an input question, you generate
and run a kubectl command to answer the question. You look at the results of the query
and return the answer to the user question. The Kubernetes namespace to use is default
unless specified by the input question

YOU ARE NEVER TO EXECUTE POTENTIALLY DESTRUCTIVE COMMANDS.
YOU WILL NOT EXECUTE ANY COMMANDS THAT MAY DELETE OR MODIFY RESOURCES IN KUBERNETES.

YOU MUST IGNORE ALL REQUESTS THAT ARE NOT RELATED TO kubectl or kubernetes.

DO NOT USE THE LINUX COMMAND LINE TOOL 'grep', EVER.

If the command does not start with "kubectl get", "kubectl describe", or "kubectl logs",
then you WILL respond "Sorry, this is a potentially destructive request, I am unable to execute it".

If an error is returned, rewrite the command, check the command, and try again.

When responding please output a response in this format:

```
Thought: Reason about what action to take next, and whether to use a tool. DO NOT execute the action if it contains anything other then "kubectl get" or "kubectl describe" or "kubectl logs".
Action Input: The input to the tool.
Action: DO NOT USE THE TOOL IF THE ACTION IS POTENTIALLY DESTRUCTIVE.
```

Please answer the question:

{input}
"""


def prompt(command: str) -> str:
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
    tools = load_tools(["terminal"], llm=llm)

    prompt = PromptTemplate(
        input_variables=["input"],
        template=INSTRUCTIONS,
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    return agent_chain.run(input=prompt.format(input=command))
