import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. EDIT THIS SECTION ONLY (YOUR CONTENT)
# ==========================================

# A. The Main Scenario (Visible at the top)
# [cite_start]Content derived from Scenario 1: The Factory Worker [cite: 1]
SCENARIO = """
[cite_start]**Patient:** David Miller, 40-year-old male. [cite: 4]
[cite_start]**Setting:** General Practice Clinic. [cite: 4]
[cite_start]**Presenting Complaint:** Tingling and numbness in the right hand. [cite: 4]

**Situation:**
[cite_start]David is a factory worker on an assembly line involving repetitive wrist movements. [cite: 5, 15]
[cite_start]He reports that shaking the hand helps (the "flick sign"). [cite: 14]
[cite_start]He is worried about his job security if he can't use his hand properly. [cite: 16]
"""

# B. The Tasks & Grading Logic
# [cite_start]Tasks mapped from source document [cite: 6]
TASK_LIST = [
    [cite_start]"1. **History:** Take a focused history.", [cite: 7]
    [cite_start]"2. **Physical Exam:** Perform a targeted physical examination of the hand (verbalize findings).", [cite: 8]
    [cite_start]"3. **Management:** Discuss the most likely diagnosis and initial management plan." [cite: 9]
]

# [cite_start]Rubrics derived from AMC/Murtagh standards in source [cite: 22]
RUBRIC_LIST = [
    # Rubric for Task 1 (History)
    """
    * [cite_start]**Identify Distribution:** Identify numbness/tingling in the median nerve distribution (thumb, index, and middle fingers). [cite: 29]
    * [cite_start]**Relief Factors:** Identify the "flick sign" (shaking hand). [cite: 14]
    * [cite_start]**Red Flags:** Must ask about sudden weakness or history of trauma. [cite: 26]
    * [cite_start]**Critical Error:** Failure to ask about "red flags". [cite: 26]
    """,
    
    # Rubric for Task 2 (Physical Exam)
    """
    * [cite_start]**Inspection:** Specifically check for thenar eminence wasting. [cite: 25]
    * [cite_start]**Special Tests:** Perform and verbalize Phalen's test and Tinel's sign. [cite: 30]
    * [cite_start]**Critical Error:** Failure to check for thenar eminence wasting. [cite: 25]
    """,
    
    # Rubric for Task 3 (Diagnosis & Management)
    """
    * [cite_start]**Diagnosis:** Identify Carpal Tunnel Syndrome. [cite: 31]
    * [cite_start]**Conservative Management:** Recommend night-time neutral wrist splints (Gold Standard). [cite: 32]
    * [cite_start]**Lifestyle/Medical:** Suggest activity modification and NSAIDs for pain. [cite: 32]
    * [cite_start]**Critical Error:** Inappropriate surgical referral before trying conservative measures for mild cases. [cite: 27]
    """
]

# ==========================================
# 2. DO NOT TOUCH THE CODE BELOW
# ==========================================

# A. Setup Google Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Gemini setup error: {e}")

# B. Page Setup
st.set_page_config(page_title="AMC Clinical Exam", layout="wide")
st.title("AMC Clinical Exam Simulation")
st.markdown("---")

# C. Display Scenario
st.header("1. Scenario")
st.info(SCENARIO)

st.markdown("---")
st.header("2. Task-by-Task Performance")

# D. The Loop (Creates a section for each task)
for index, (task_text, rubric_text) in enumerate(zip(TASK_LIST, RUBRIC_LIST)):
    with st.container():
        st.subheader(task_text)
        
        col_task_left, col_task_right = st.columns([1, 2])
        
        with col_task_left:
            st.write("🎙️ **Record your response:**")
            audio_val = st.audio_input(label=f"Rec Task {index+1}", key=f"audio_{index}")
            
        with col_task_right:
            if audio_val:
                if st.button(f"Grade Task {index+1}", key=f"btn_{index}"):
                    with st.spinner("Analyzing..."):
                        try:
                            audio_data = audio_val.read()
                            
                            prompt = f"""
                            You are an AMC Examiner evaluating ONE SPECIFIC TASK.
                            
                            SCENARIO: {SCENARIO}
                            CURRENT TASK: {task_text}
                            RUBRIC FOR THIS TASK: {rubric_text}
                            
                            INSTRUCTIONS:
                            1. Transcribe the student's audio.
                            2. Compare it strictly to the RUBRIC provided above.
                            3. Did they meet the requirements?
                            
                            OUTPUT:
                            **Transcription:** "..."
                            **Feedback:** ...
                            **Verdict:** PASS / FAIL (for this task)
                            """
                            
                            response = model.generate_content([
                                prompt,
                                {"mime_type": "audio/wav", "data": audio_data}
                            ])
                            
                            st.markdown(response.text)
                            
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.info("Waiting for audio...")
        
        st.divider()

# E. Hidden Master Rubric
st.write("### Review Full Case")
with st.expander("👁️ Click to Reveal Full Answer Key (All Tasks)"):
    st.markdown("### Official Examiner Guide")
    st.info(SCENARIO)
    
    for i, (t, r) in enumerate(zip(TASK_LIST, RUBRIC_LIST)):
        st.markdown(f"**{t}**")
        st.markdown(r)
        st.markdown("---")
