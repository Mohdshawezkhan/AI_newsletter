from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from newsletter_gen.tools.research import SearchAndContents, FindSimilar, GetContents 
from datetime import datetime
import streamlit as st
from typing import Union, List, Tuple, Dict
from langchain_core.agents import AgentFinish
import json
# from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_community.llms import Ollama
ollama_mixtral = Ollama(model="mixtral", base_url="https://11434-01jawwb3nm1m9k6nnvnmd453kq.cloudspaces.litng.ai")

@CrewBase

class NewsletterGenCrew():
    agents_config='config/agents.yaml'
    tasks_config='config/tasks.yaml'

    def llm(self):
          llm = ollama_mixtral
          return llm
    
    @agent
    def researcher(self)-> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SearchAndContent(), FindSimilar(), GetContents()],
            verbose=True,
            llm=self.llm()
        )
    @agent
    def editor(self)-> Agent:
        return Agent(
            config=self.agents_config['editor'],
            tools=[SearchAndContent(), FindSimilar(), GetContents()],
            verbose=True,
            llm=self.llm()
        )

    @agent
    def designer(self)-> Agent:
        return Agent(
            config=self.agents_config['designer'],
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self.llm()
        )
    
    @task
    def research_task(self)-> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher()
        )
    
    @task
    def edit_task(self)-> Task:
        return Task(
            config=self.tasks_config['edit_task'],
            agent=self.editor(),
        )
    
    @task
    def newsletter_task(self)-> Task:
        return Task(
            config=self.tasks_config['newsletter_task'],
            agent=self.designer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
