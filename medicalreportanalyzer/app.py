import streamlit as st
import os
import tempfile

# Import your working CrewAI setup
# (Make sure this matches the exact class name inside your src/medicalreportanalyzer/crew.py file)
from medicalreportanalyzer.crew import Medicalreportanalyzer

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Health Analyzer", page_icon="🩺", layout="centered")

st.title("🩺 AI Medical Report Analyzer")
st.write("Upload your blood test or medical report to generate a patient-friendly health summary.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload Medical Report", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Show a preview of what the user uploaded
    st.image(uploaded_file, caption="Report Preview", use_container_width=True)
    
    # Run the AI only when the user clicks the button
    if st.button("Generate Health Summary"):
        
        with st.spinner("Agents are analyzing your report... This may take a minute or two."):
            try:
                # 1. Save the uploaded file to a temporary location on your disk
                # (Because your CrewAI tool requires a physical file path!)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_image_path = tmp_file.name

                # 2. Pass that temporary path into your CrewAI inputs
                inputs = {
                    'image_path': temp_image_path
                }
                
                # 3. Kickoff the Crew
                crew = Medicalreportanalyzer().crew()
                result = crew.kickoff(inputs=inputs)
                
                # 4. Display the beautifully formatted markdown report!
                st.success("Analysis Complete!")
                
                # If CrewAI returns a complex object, we just want the raw string output
                final_text = result.raw if hasattr(result, 'raw') else str(result)
                st.markdown(final_text)

            except Exception as e:
                st.error(f"Pipeline crashed: {str(e)}")
                
            finally:
                # Clean up: Delete the temporary file so we don't clutter your hard drive
                if 'temp_image_path' in locals() and os.path.exists(temp_image_path):
                    os.remove(temp_image_path)