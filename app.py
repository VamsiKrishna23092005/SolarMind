import streamlit as st
from solarmind.graph import get_compiled_graph
from solarmind.vision import get_vision_model
import os
import tempfile

st.title("SolarMind Dashboard")

st.sidebar.title("⚙️ Configuration")
ollama_url = st.sidebar.text_input(
    "Ollama Base URL", 
    value=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    help="If running on Streamlit Cloud, paste your Ngrok/tunnel URL to your local Ollama instance here."
)
os.environ["OLLAMA_BASE_URL"] = ollama_url

@st.cache_resource
def load_app():
    return get_compiled_graph()

app = load_app()

prompt = st.text_input("Research Query:", help="Enter solar-related query to begin.")

# Thread ID configuration using basic session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

if st.button("Run Pipeline") and prompt:
    with st.spinner("Running SolarMind parallel pipeline tasks..."):
        # Executes graph state up to Human-in-The-Loop interrupt
        try:
            for event in app.stream({"research_query": prompt}, config=config):
                st.write(event)
        except Exception as e:
            if "ConnectError" in str(type(e).__name__) or "Connection error" in str(e):
                st.error("🚨 **Connection Error: Could not connect to the Ollama LLM.**")
                st.info("You are running on a cloud environment without a local Ollama instance. Please use the sidebar to define a public URL to your Ollama server, or run this dashboard locally.")
                st.stop()
            else:
                st.error(f"Pipeline error: {e}")
                st.stop()
            
        state = app.get_state(config)
        
        if state.next and "human_review" in state.next:
            st.warning("Pipeline paused for human review.")
            st.write("### Current Report Draft:")
            st.write(state.values.get("research_report", ""))

def resume_pipeline():
    with st.spinner("Resuming pipeline compilation..."):
        # Proceed past interrupt point using natural human message
        try:
            for event in app.stream({"messages": [{"role": "human", "content": "Approved"}]}, config=config):
                st.write(event)
        except Exception as e:
            st.error(f"Connection/Pipeline Error: {e}")
            st.stop()
        
        state = app.get_state(config)
        st.success("Pipeline Completed!")
        st.subheader("Final Output Report:")
        # Show merged findings
        st.write(state.values.get("research_report", ""))

if st.button("Approve & Continue (Interrupt Handling)"):
    resume_pipeline()

# Multimodal Visual Capabilities - Phase 4
st.header("Multimodal Florence-2 Analysis")
uploaded_file = st.file_uploader("Upload solar irradiance graph", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Extracted Irradiance Chart")
    if st.button("Deep View Image Summary"):
        with st.spinner("Analyzing graph with Florence-2 (Local Setup)..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            vision_model = get_vision_model()
            analysis = vision_model.analyze_solar_graph(tmp_path)
            
            st.write("### Multimodal Analysis Findings:")
            st.info(analysis)
            os.remove(tmp_path)
