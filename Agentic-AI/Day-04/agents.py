from crewai import Agent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
load_dotenv()

search_tool = SerperDevTool()
senior_researcher = Agent(
    role="researcher",
    goal="""Break down complex AI topics into simple, beginner-friendly explanations.
    Focus on clarity, real-world examples, and avoid technical jargon.""",
    backstory="""You have 10+ years of experience explaining AI to non-technical audiences.
    You are known for making difficult concepts easy to understand.""",
    verbose=True,
    memory=False,
    tools=[search_tool],
    llm="gpt-4o-mini",
    allow_delegation=False,
)

script_writer = Agent(
    role="writer",
    goal="""Write highly engaging YouTube scripts that capture attention in the first 5 seconds,
    use storytelling, and maintain viewer interest throughout.""",
    backstory="""You specialize in viral educational content and understand audience psychology,
    retention techniques, and storytelling frameworks.""",
    verbose=True,
    memory=False,
    tools=[],
    llm="gpt-4o-mini",
    allow_delegation=False,
)

reviewer = Agent(
    role="reviewer",
    goal="""Critically evaluate YouTube scripts for clarity, engagement, and accuracy.
    Suggest specific improvements.""",
    backstory="""You are an expert in content quality, audience retention,
    and storytelling. You identify weak hooks, boring sections, and unclear explanations.""",
    verbose=True,
    memory=False,
    tools=[],
    llm="gpt-4o-mini",
    allow_delegation=False,
)

manager = Agent(
    role="AI Project Manager",
    goal="""
    You are ONLY a coordinator.

    You MUST:
    - NEVER use tools
    - NEVER answer directly
    - ALWAYS delegate tasks first

    Workflow:
    1. Delegate research to researcher
    2. Then writing to writer
    3. Then review to reviewer
    4. Then improvement

    You do NOT perform any work yourself.
    """,
    backstory="Strict coordinator who never does execution work.",
    verbose=True,
    memory=True,
    llm="gpt-4o-mini",
    allow_delegation=True,
)