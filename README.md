# 🩺 Medical Report Analyzer AI Crew

<div align="center">
  <br/>
  <strong>🚀 Explore the AI-Powered Medical Report Analyzer 🚀</strong>
  <br/>
  <br/>

  [![Live Application Demo](https://img.shields.io/badge/🔴_Live_Demo-Streamlit_App-FF4B4B?style=for-the-badge&logo=streamlit)](https://swarnika-cmd-medical-report-ana-medicalreportanalyzerapp-nppfwi.streamlit.app/)
  
  *Click the badge above to try the live application!*
</div>

---

Welcome to the **Medical Report Analyzer Crew** project, powered by [crewAI](https://crewai.com) 🤖. 

This project leverages a multi-agent AI system to collaboratively analyze complex medical reports, interpret health data against standard reference ranges, and provide patient-friendly health summaries. By maximizing the collective intelligence of specialized agents, we make medical data accessible and easy to understand!

## ✨ Features

- **Multi-Agent Collaboration:** Specialized AI agents work together seamlessly.
- **Vision AI Integration:** Extracts information directly from medical report images.
- **Personalized Health Advisories:** Generates easy-to-read, actionable health summaries.

## 🛠️ Installation

Ensure you have Python **`>=3.10 <3.14`** installed on your system. This project uses [UV](https://docs.astral.sh/uv/) ⚡ for blazing-fast dependency management.

1️⃣ **Install UV (if you haven't already):**
```bash
pip install uv
```

2️⃣ **Install the project dependencies:**
*(Optional) Lock the dependencies and install them by using the CLI command:*
```bash
crewai install
```

## ⚙️ Customizing Your Crew

Before running the agents, you need to configure your environment.

🔑 **Add your API Keys:**
Create a `.env` file in the root directory and add your keys (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`).

You can customize the AI crew behavior by modifying the following files:
- 🕵️‍♂️ **Agents:** Modify `src/medicalreportanalyzer/config/agents.yaml` to define or tweak your agents.
- 📋 **Tasks:** Modify `src/medicalreportanalyzer/config/tasks.yaml` to define your tasks.
- 🧠 **Logic:** Modify `src/medicalreportanalyzer/crew.py` to add your own logic, tools, and specific arguments.
- 🚀 **Execution:** Modify `src/medicalreportanalyzer/main.py` to add custom inputs for your agents and tasks.

## 🚀 Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the **Medical Report Analyzer Crew**, assembling the agents and assigning them tasks as defined in your configuration. By default, it will generate a comprehensive markdown report (`health_report.md`) based on the analyzed data.

## 🧩 Understanding Your Crew

The Medical Report Analyzer Crew is composed of multiple AI agents, each with unique roles, goals, and tools:
- **Agents Configuration:** `config/agents.yaml` outlines the capabilities and roles.
- **Tasks Configuration:** `config/tasks.yaml` defines the step-by-step objectives they must achieve collaboratively.

## 💬 Support & Community

For support, questions, or feedback regarding the CrewAI framework:
- 📖 Visit the [documentation](https://docs.crewai.com)
- 💻 Reach out through the [GitHub repository](https://github.com/joaomdmoura/crewai)
- 👾 [Join the Discord Community](https://discord.com/invite/X4JWnZnxPb)
- 💬 [Chat with their docs](https://chatg.pt/DWjSBZn)

---
<div align="center">
  <i>Let's create wonders together with the power and simplicity of AI.</i>
</div>
