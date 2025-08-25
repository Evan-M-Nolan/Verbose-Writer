from crewai import Agent, Task, Crew

planner = Agent(
    role='Technical Planner',
    goal='Create detailed implementation plans',
    backstory='Expert at breaking down requirements into actionable plans'
)

developer = Agent(
    role='Developer',
    goal='Implement code based on technical plans',
    backstory='Skilled developer who follows specifications precisely'
)