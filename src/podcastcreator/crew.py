from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from podcastcreator.tools.audiomerger_tool import MergeAudioTool
from podcastcreator.tools.sarvamtts_tool import TextToSpeechTool
from podcastcreator.tools.cleanwaw_tool import CleanWavFilesTool

from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Podcastcreator():
    """Podcastcreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def podcast_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['podcast_creator'], # type: ignore[index]
            verbose=True
        )

    @agent
    def podcast_producer(self) -> Agent:
        return Agent(
            config=self.agents_config['podcast_producer'], # type: ignore[index]
            tools = [MergeAudioTool() , TextToSpeechTool() , CleanWavFilesTool() ] , 
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def create_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_report_task'], # type: ignore[index]
        )

    @task
    def create_podcast_script_segments_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_podcast_script_segments_task'], # type: ignore[index]
            output_file='report.md'
        )

    
    @task
    def merge_segments_to_audio_task(self) -> Task:
        return Task(
            config=self.tasks_config['merge_segments_to_audio_task'], # type: ignore[index]
            output_file='result.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Podcastcreator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
