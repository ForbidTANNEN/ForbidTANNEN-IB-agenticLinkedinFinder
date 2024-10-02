import os

from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str, company: str, emailDomain: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    template = """given the full name {name_of_person} and the following information about them: company-{company} and email domain-{emailDomain}, I want you to get it me a link to their Linkedin profile page.
                          If you cannot find then answer, "I dont know". Your answer should contain only a URL."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person", "company", "emailDomain"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, handle_parsing_errors=True, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name, company=company, emailDomain=emailDomain)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


# Anthony	Nemitz	Close	close.com	Co-Founder & Chief Operating Officer
if __name__ == "__main__":
    # # linkedin_url = lookup("Jason Brook", "hospitalgiftshop.com", emailDomain="Hospital Giftshop.com")
    # linkedin_url = lookup("Anthony Nemitz", "Close", "close.com")
    # print(linkedin_url)
    print(get_profile_url_tavily("LinkedIn Scott Kalan Nectar"))