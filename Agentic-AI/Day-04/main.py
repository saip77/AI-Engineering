from crewai import Crew, Process
from agents import senior_researcher, script_writer, reviewer, manager
from tasks import research_task, script_task, review_task, rewrite_task

crew = Crew(
    agents=[senior_researcher, script_writer, reviewer],
    tasks=[research_task, script_task, review_task, rewrite_task],
    process=Process.hierarchical,
    manager_agent=manager,  
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff(
        inputs={"topic": "latest AI regulations 2026"}
    )
    print(result)