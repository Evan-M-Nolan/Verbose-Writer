# Agentic AI Planning System

A two-phase AI system that creates detailed implementation plans for your projects, allows you to manually review and edit them, then implements the code based on your approved plan.

## Features

- **Planning Agent**: Creates comprehensive technical specifications
- **Developer Agent**: Implements code based on your approved plans  
- **Human-in-the-Loop**: Manual review and editing between phases
- **Structured Output**: Well-organized plans and implementation files

## Setup

### 1. Clone/Create Project Directory
```bash
mkdir ai-planning-system
cd ai-planning-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# .env should contain:
# OPENAI_API_KEY=your_actual_api_key_here
```

### 5. Test Installation
```bash
python main.py
```

## Usage

### Full Workflow (Recommended)
```bash
python main.py
```
This will:
1. Ask for your project requirements
2. Generate a detailed implementation plan
3. Pause for you to review/edit the plan
4. Implement the code based on your approved plan

### Development Only Mode
If you already have an approved plan file:
```bash
python main.py develop plans/implementation_plan_20241225_143022.md
```

## Project Structure
```
ai-planning-system/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── .env                # Your API keys (create this)
├── .env.example        # Template for environment variables
├── plans/              # Generated plans (auto-created)
├── output/             # Implementation files (auto-created)
└── templates/          # Plan templates (auto-created)
```

## How It Works

### Phase 1: Planning
- The Planning Agent analyzes your requirements
- Creates a comprehensive technical specification including:
  - Architecture design
  - File structure
  - Implementation steps
  - API designs
  - Database schemas
  - Testing strategy

### Manual Review
- System pauses and shows you the plan file location
- You can edit the plan in Cursor or any text editor
- Make any changes you want before proceeding

### Phase 2: Development  
- The Developer Agent reads your approved plan
- Implements all the code according to your specifications
- Creates all files in the `output/` directory

## Example Usage

**Input**: "Build a todo app with React frontend and FastAPI backend"

**Planning Agent Output**: 
- Detailed 50+ line specification
- Database schema for todos
- API endpoint definitions
- React component structure
- Deployment instructions

**After Your Edits**: You modify the plan to use PostgreSQL instead of SQLite, add authentication, etc.

**Developer Agent Output**:
- Complete React frontend
- FastAPI backend with your specified database
- Docker configuration
- README with setup instructions

## Tips for Success

### Writing Good Requirements
- Be specific about your tech preferences
- Mention any constraints or requirements
- Include user stories if helpful
- Specify deployment preferences

### Editing Plans Effectively
- Review the technical stack choices
- Modify the file structure if needed
- Add or remove features
- Adjust implementation priorities
- Clarify any ambiguous sections

### Getting Better Results
- Start with smaller projects to test the system
- Iterate on your prompting style
- Keep plans detailed but not overly complex
- Use the development-only mode to test plan changes

## Troubleshooting

### "API Key not found"
Make sure your `.env` file exists and contains:
```
OPENAI_API_KEY=your_actual_key_here
```

### "Module not found" 
Make sure you've activated your virtual environment and installed requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Plans seem too generic
Try being more specific in your requirements and editing the agent prompts in `main.py`

### Development agent isn't following the plan
Check that your plan file has sufficient detail and clear instructions

## Customization

You can modify the agents' behavior by editing their `backstory` and `goal` parameters in `main.py`. You can also adjust the task descriptions to change what gets included in plans and implementations.

## Next Steps

- Add support for other LLM providers (Anthropic, Google)
- Create web interface with Streamlit
- Add plan templates for common project types
- Integration with version control
- Support for iterative development cycles