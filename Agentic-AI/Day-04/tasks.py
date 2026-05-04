from crewai import Task
from agents import senior_researcher, script_writer, reviewer


# 🔹 Research Task
research_task = Task(
    description="""
    Gather accurate and up-to-date information about {topic} using available tools.

    Provide:
    - What it is
    - Why it matters
    - One real-world example

    Keep the explanation simple, clear, and factual.
    Do NOT include unnecessary details or assumptions.
    """,
    expected_output="""
    A clear and factual explanation with:
    - Simple language
    - One real-world example
    - No fabricated or assumed facts
    """,
    agent=senior_researcher,
)


# 🔹 Script Writing Task
script_task = Task(
    description="""
    Create an engaging YouTube script about {topic}.

    Use ONLY the information provided in context.
    Do NOT invent facts or statistics.

    Structure:
    - Hook
    - Introduction
    - Main explanation
    - Ending

    Keep it conversational and engaging.
    """,
    expected_output="""
    A structured YouTube script that:
    - Has clear sections (Hook, Intro, Body, Ending)
    - Uses only factual information
    - Is engaging and easy to understand
    """,
    agent=script_writer,
)


# 🔹 Review Task (LOOP SAFE)
review_task = Task(
    description="""
    Review the YouTube script ONCE.

    Check for:
    - major factual inaccuracies
    - weak engagement
    - unclear explanations

    IMPORTANT:
    - If the script is already good, say: "No major improvements needed."
    - Do NOT over-criticize minor issues.
    - Do NOT suggest infinite improvements.
    """,
    expected_output="""
    EITHER:
    - A list of major improvements

    OR:
    - "No major improvements needed."
    """,
    agent=reviewer,
)


# 🔹 Rewrite Task (FINAL STEP)
rewrite_task = Task(
    description="""
    Improve the YouTube script using the review feedback.

    Rules:
    - Fix only major issues
    - Do NOT completely rewrite unless necessary
    - Keep the script concise and engaging

    IMPORTANT:
    - If review says "No major improvements needed", return the original script.

    This is the FINAL step. Do not iterate further.
    """,
    expected_output="""
    Final improved YouTube script.

    End your response with:
    "FINAL VERSION COMPLETE"
    """,
    agent=script_writer,
)