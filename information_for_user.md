# Welcome to SolarMind: Autonomous Energy Market Analyst ☀️🧠

Thank you for deploying SolarMind! This document serves as your primary guide to understanding what this project is, what it is capable of, and exactly how you can interact with it on the deployed Streamlit Dashboard.

## 🎯 What is this project?

**SolarMind** is an advanced, fully open-source AI pipeline built using **LangGraph**. It acts as an autonomous research team dedicated to solar energy, technical forecasting (like PatchTST), hardware metrics, and energy policy.

Instead of just asking a single AI a question, SolarMind uses a Multi-Agent architecture:
- 🕵️ **Parallel Researchers:** When you ask a question, the system spawns multiple "Researcher" agents simultaneously. One looks at *Market Trends*, another at *Technical Metrics*, and another at *Policy Subsidies*.
- 📊 **Technical Analyst (RAG):** An agent specifically designed to look at hard technical data and metrics (which can be supercharged if you upload PDFs to its local ChromaDB database).
- 🧑‍⚖️ **The Critic:** A quality-control agent that reviews the compiled research. If the report is poor or hallucinated, it forces the researchers to go back and try again!
- ✍️ **The Final Editor:** Merges all the parallel findings into one cohesive, professional report.

Best of all? It's designed to run entirely on **free, local, open-source models** like Llama3 and Florence-2!

---

## 🎮 How to use the Dashboard

When you open your Streamlit Dashboard, you will see a clean interface. Here is exactly how to play around with it:

### 1. Generating a Research Report
1. **Find the "Research Query" Box:** At the top of the dashboard, you will see a text input box.
2. **Ask a complex question:** Type something related to the solar industry. Examples to try:
   - *"What are the current hardware costs and efficiency rates of perovskite solar cells?"*
   - *"Explain how the PatchTST algorithm is being used to forecast solar irradiance."*
   - *"Identify the latest government subsidies for residential solar in Europe."*
3. **Click "Run Pipeline":** The LangGraph engine will begin executing. You will see raw "events" streaming onto the screen—this is you watching the agents "think" and pass data to each other in real-time!

### 2. The Human-in-the-Loop Interrupt
SolarMind doesn't just blindly publish its findings; it waits for your approval.
1. After the agents finish compiling the draft, the pipeline will **pause**.
2. You will see a yellow warning: `Pipeline paused for human review` along with the drafted report.
3. If you are satisfied with what the AI found, click the **"Approve & Continue"** button. The system will finalize the run and output the polished `Final Comprehensive Report`.

### 3. Deep Multimodal Visual Analysis
At the bottom of the dashboard is the **Multimodal Florence-2 Analysis** section.
1. **Take a screenshot or save an image** of a complex solar data graph (e.g., an irradiance chart, a loss-curve graph from a research paper, or a patch-time-series visualization).
2. **Drag and drop** that image into the file uploader.
3. **Click "Deep View Image Summary".**
4. The system will boot up `Florence-2` (Microsoft's open-source vision model) to physically "look" at the graph and extract the visual trends into text for you.

*(Note: If running locally, this step downloads the Vision Model weights the very first time you click it, so it may take a minute!)*

---

## 🚀 Pro Tips for Next Steps

Now that you have the basic dashboard running, here is how you can take SolarMind to the next level:

- **Upload your own data (RAG):** Right now, the Technical Analyst relies on web searches. To make it a true expert, put PDF research papers (like the original PatchTST papers) inside the project folder, and run the `ingest_papers()` function in `solarmind/rag.py` to fill the local vector database.
- **Tweak the Prompts:** Open `solarmind/graph.py` and modify the instructions given to the `researcher_node` or the `critic_node`. You can change the agent's personality or focus entirely!
