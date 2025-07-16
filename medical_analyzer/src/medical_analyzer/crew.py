from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class MedicalSummarizerCrew():
    """MedicalAnalyzer crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def reader_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["reader_agent"],
            verbose=True
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarizer_agent"],
            verbose=True
        )

    @agent
    def validator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["validator_agent"],
            verbose=True
        )

    @task
    def read_task(self) -> Task:
        return Task(
            config=self.tasks_config["read_task"]
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_task"],
            output_file="output/summary.txt"
        )

    @task
    def validate_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["validate_summary_task"],
            output_file="output/validation_report.txt"
        )
    
    @task
    def revise_summary_task(self) -> Task:
        return Task(
        config=self.tasks_config["revise_summary_task"],
        output_file="output/summary.txt"
    )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    

    
    def revision_crew(self) -> Crew:
        return Crew(
            agents=[
                self.summarizer_agent(),
                self.validator_agent()
            ],
            tasks=[
                self.revise_summary_task(),
                self.validate_summary_task()
            ],
            process=Process.sequential,
            verbose=True
        )

