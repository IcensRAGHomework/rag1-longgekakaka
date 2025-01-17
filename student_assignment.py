import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)


def init_llm():
    llm = AzureChatOpenAI(
        model=gpt_config['model_name'],
        deployment_name=gpt_config['deployment_name'],
        openai_api_key=gpt_config['api_key'],
        openai_api_version=gpt_config['api_version'],
        azure_endpoint=gpt_config['api_base'],
        temperature=gpt_config['temperature']
    )
    return llm


def generate_hw01(question):
    llm = init_llm()
    examples = [
        {
            "input": "2024年台湾10月有哪些纪念日?",
            "output": {
                    "Result": [
                        {"date": "2024-10-09", "name": "重阳节"},
                        {"date": "2024-10-10", "name": "中华民国国庆日"}
                    ]
            }
        }
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    # print few_shot_prompt
    # print(few_shot_prompt.invoke({}).to_messages())
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a Taiwan local assistant!"
                       "You should follow the examples to give me the result in json format."),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    chain = final_prompt | llm
    response = chain.invoke({"input": question})
    print(response.content)

def generate_hw02(question):
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
def demo(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    
    return response


if __name__ == '__main__':
    question = "2024年10月台湾有什么纪念日?"
    generate_hw01(question)