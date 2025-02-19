from swarm import Swarm, Agent
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI 

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")


class SingletonSwarm:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonSwarm, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = Swarm(client=OpenAI(
                api_key=api_key,
                base_url=base_url,
            ))
        return cls._instance

# 使用单例模式创建client
swarm_client = SingletonSwarm().client



def generate_agent_with_name_instruments(name, instructions,functions = []):
    return Agent(
        name=name,
        instructions=instructions,
        model="deepseek-chat",
        functions = functions
    )


def generate_response_with_agent_query(agent,query):
    news_response = swarm_client.run(
        agent=agent,
        messages=[{"role": "user", "content": f"{query}"}],
    )
    return news_response.messages[-1]["content"]


class AgentPool:
    def __init__(self, max_agents=20):
        self.max_agents = max_agents
        self.agents = []

    def add_agent(self, name, instructions, functions=[]):
        if len(self.agents) < self.max_agents:
            agent = generate_agent_with_name_instruments(name, instructions, functions)
            self.agents.append(agent)
            return agent
        else:
            raise Exception("Agent pool is full")

    #可能会get None
    def get_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def remove_agent(self, name):
        self.agents = [agent for agent in self.agents if agent.name != name]


    def execute_and_release(self, name, query):
        agent = self.get_agent(name)
        if agent:
            response = generate_response_with_agent_query(agent, query)
            self.remove_agent(name)
            return response
        else:
            # 这里的raise表示抛出一个异常。当找不到指定名称的agent时，程序会抛出一个异常，提示用户该agent不存在。
            raise Exception(f"Agent with name {name} not found")


if __name__ == "__main__":
    # 示例用法
    agent_pool = AgentPool()
    agent_pool.add_agent("标题助手", "帮助生成和优化标题")
    response = agent_pool.execute_and_release("标题助手", "如何生成一个好的标题,关于饮品推广的")
    print(response)
    
    









