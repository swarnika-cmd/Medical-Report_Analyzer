from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from medicalreportanalyzer.tools.image_reader import MedicalReportImageReader

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Medicalreportanalyzer():
    """Medicalreportanalyzer crew - Analyzes medical report images and provides
    patient-friendly health summaries with actionable recommendations."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    @agent
    def report_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['report_parser'],  # type: ignore[index]
            tools=[MedicalReportImageReader()],
            verbose=True
        )

    @agent
    def health_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['health_analyst'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def health_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['health_advisor'],  # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def parse_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['parse_report_task'],  # type: ignore[index]
        )

    @task
    def analyze_health_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_health_task'],  # type: ignore[index]
        )

    @task
    def generate_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_summary_task'],  # type: ignore[index]
            output_file='health_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Medicalreportanalyzer crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
