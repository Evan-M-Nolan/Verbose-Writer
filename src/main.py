import os
import sys
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from crewai.tools import FileReadTool, FileWriterTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgenticPlanningSystem:
    def __init__(self):
        self.setup_directories()
        self.setup_tools()
        self.setup_agents()
        
    def setup_directories(self):
        """Create necessary directories"""
        directories = ['plans', 'output', 'templates']
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)
    
    def setup_tools(self):
        """Initialize tools for file operations"""
        self.file_read_tool = FileReadTool()
        self.file_writer_tool = FileWriterTool()
    
    def setup_agents(self):
        """Initialize the planning and developer agents"""
        
        self.planner_agent = Agent(
            role='Senior Technical Planner',
            goal='Create comprehensive, detailed technical implementation plans that can be easily understood and modified by humans before development',
            backstory="""You are a senior software architect with 15+ years of experience in planning and designing software systems. 
            You excel at breaking down complex requirements into clear, actionable implementation plans. You understand that your plans 
            will be reviewed and potentially modified by humans before implementation, so you make them detailed yet flexible.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.file_writer_tool]
        )
        
        self.developer_agent = Agent(
            role='Senior Full-Stack Developer',
            goal='Implement high-quality code exactly according to the approved technical plan',
            backstory="""You are an expert full-stack developer who excels at following detailed specifications. 
            You read technical plans carefully and implement them precisely, asking for clarification only when the plan 
            is ambiguous. You write clean, well-documented, production-ready code.""",
            verbose=True,
            allow_delegation=True,
            tools=[self.file_read_tool, self.file_writer_tool]
        )
    
    def create_planning_task(self, requirements):
        """Create the planning task"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"plans/implementation_plan_{timestamp}.md"
        
        return Task(
            description=f"""
            Create a comprehensive technical implementation plan for the following requirements:
            
            {requirements}
            
            Your plan should include:
            1. **Project Overview**: Clear summary of what will be built
            2. **Technical Stack**: Recommended technologies, frameworks, and libraries
            3. **Architecture**: High-level system design and component interactions
            4. **File Structure**: Complete directory and file organization
            5. **Database Design**: Schema, relationships, and data models (if applicable)
            6. **API Design**: Endpoints, request/response formats (if applicable)
            7. **Implementation Steps**: Ordered list of development phases
            8. **Key Components**: Detailed breakdown of each major component
            9. **Dependencies**: External libraries and their purposes
            10. **Configuration**: Environment variables, settings, and deployment notes
            11. **Testing Strategy**: Unit tests, integration tests, and testing approach
            12. **Potential Challenges**: Known issues and proposed solutions
            
            Save the plan to: {plan_filename}
            
            Make the plan detailed enough that a developer can implement it without guessing, 
            but structured so a human can easily review and modify it.
            """,
            agent=self.planner_agent,
            expected_output=f"A comprehensive technical plan saved to {plan_filename}"
        )
    
    def create_development_task(self, plan_file):
        """Create the development task"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return Task(
            description=f"""
            Read the approved implementation plan from {plan_file} and implement the complete solution.
            
            Instructions:
            1. Read and understand the entire plan thoroughly
            2. Follow the plan exactly as specified
            3. Create all files and directories as outlined
            4. Implement all features and functionality described
            5. Include proper error handling and logging
            6. Add comprehensive comments and documentation
            7. Follow the coding standards mentioned in the plan
            8. Save all implementation files in the output/ directory
            
            If any part of the plan is unclear or missing details, ask for clarification 
            rather than making assumptions.
            
            Create a summary file explaining what was implemented and how to run/use it.
            """,
            agent=self.developer_agent,
            expected_output="Complete implementation with all files created in output/ directory and a summary of what was built"
        )
    
    def run_planning_phase(self, requirements):
        """Run only the planning phase"""
        print("🚀 Starting Planning Phase...")
        
        planning_task = self.create_planning_task(requirements)
        planning_crew = Crew(
            agents=[self.planner_agent],
            tasks=[planning_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = planning_crew.kickoff()
        print("\n✅ Planning phase completed!")
        
        # Find the created plan file
        plans_dir = Path("plans")
        plan_files = list(plans_dir.glob("implementation_plan_*.md"))
        if plan_files:
            latest_plan = max(plan_files, key=lambda x: x.stat().st_mtime)
            print(f"📋 Plan saved to: {latest_plan}")
            return str(latest_plan)
        
        return None
    
    def run_development_phase(self, plan_file):
        """Run the development phase with an approved plan"""
        if not os.path.exists(plan_file):
            print(f"❌ Plan file not found: {plan_file}")
            return
        
        print(f"🔨 Starting Development Phase with plan: {plan_file}")
        
        development_task = self.create_development_task(plan_file)
        development_crew = Crew(
            agents=[self.developer_agent],
            tasks=[development_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = development_crew.kickoff()
        print("\n✅ Development phase completed!")
        print("📁 Check the output/ directory for your implementation")
    
    def run_full_workflow(self, requirements):
        """Run the complete workflow with manual approval step"""
        # Phase 1: Planning
        plan_file = self.run_planning_phase(requirements)
        
        if not plan_file:
            print("❌ Failed to create plan file")
            return
        
        # Manual review step
        print(f"\n📝 Please review and edit the plan file: {plan_file}")
        print("Make any necessary changes, then return here.")
        
        while True:
            user_input = input("\nType 'approve' to proceed with development, or 'quit' to exit: ").strip().lower()
            if user_input == 'approve':
                break
            elif user_input == 'quit':
                print("👋 Workflow cancelled. You can resume later by running development phase with your plan file.")
                return
            else:
                print("Please type 'approve' or 'quit'")
        
        # Phase 2: Development
        self.run_development_phase(plan_file)


def main():
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    system = AgenticPlanningSystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "develop" and len(sys.argv) > 2:
            # Run development phase only
            plan_file = sys.argv[2]
            system.run_development_phase(plan_file)
        else:
            print("Usage:")
            print("  python main.py                    # Run full workflow")
            print("  python main.py develop <plan.md>  # Run development phase only")
    else:
        # Interactive mode
        print("🤖 Welcome to the Agentic Planning System!")
        print("This system will create a detailed implementation plan that you can review and edit.")
        
        requirements = input("\nDescribe what you want to build: ").strip()
        
        if not requirements:
            print("❌ Please provide some requirements")
            return
        
        system.run_full_workflow(requirements)


if __name__ == "__main__":
    main()