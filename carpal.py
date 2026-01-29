import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. EDIT THIS SECTION ONLY (YOUR CONTENT)
# ==========================================

# A. The Main Scenario (Visible at the top)
# Content derived from Scenario 1: The Factory Worker [cite: 1]
SCENARIO = """
**Patient:** David Miller, 40-year-old male. [cite: 4]
**Setting:** General Practice Clinic. [cite: 4]
**Presenting Complaint:** Tingling and numbness in the right hand. [cite: 4]

**Situation:**
David is a factory worker on an assembly line involving repetitive wrist movements. [cite: 5, 15]
He reports that shaking the hand helps (the "flick sign"). [cite: 14, 21]
He is worried about his job security if he can't use his hand properly. [cite: 16]
"""

# B. The Tasks & Grading Logic
# Tasks mapped from source document [cite: 6]
TASK_LIST = [
    "1. **History:** Take a focused history. [cite: 7]",
    "2. **Physical Exam:** Perform a targeted physical examination of the hand (verbalize findings). [cite: 8]",
    "3. **Management:** Discuss the most likely diagnosis and initial management plan. [cite: 9]"
]

# Rubrics derived from AMC/Murtagh standards in source [cite: 22, 28]
RUBRIC_LIST = [
    # Rubric for Task 1 (History)
    """
    * **Identify Distribution:** Identify numbness/tingling in the median nerve distribution (thumb, index, and middle fingers). [cite: 13, 19, 29]
    * **Relief Factors:** Identify the "flick sign" (shaking hand). [cite: 14, 21]
    * **Red Flags:** Must ask about sudden weakness or history of trauma. [cite: 26]
    * **Critical Error:** Failure to ask about "red flags". [cite: 24, 26]
    """,
    
    # Rubric for Task 2 (Physical Exam)
    """
    * **Inspection:** Specifically check for thenar eminence wasting. [cite: 25, 102, 106]
    * **Special Tests:** Perform and verbalize Phalen's test and Tinel's sign. [cite: 30]
    * **Critical Error:** Failure to check for thenar eminence wasting. [cite: 24, 25, 112]
    """,
    
    # Rubric for Task 3 (Diagnosis & Management)
    """
    * **Diagnosis:** Identify Carpal Tunnel Syndrome. [cite: 1, 31]
    * **Conservative Management:** Recommend night-time neutral wrist splints (Gold Standard). [cite: 32, 89]
    * **Lifestyle/Medical:** Suggest activity modification and NSAIDs for pain. [cite: 32]
    * **Critical Error:** Inappropriate surgical referral before trying conservative measures for mild cases. [cite: 24, 27]
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

# Visual aid for the medical context
st.markdown("##### Reference Anatomy")
col_img1, col_img2 = st.columns(2)
with col_img1:
    st.write("Median Nerve Sensory Distribution")
    # Median nerve distribution affects the thumb, index, middle, and half of the ring finger [cite: 13, 29]
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Grant_1962_663.png/640px-Grant_1962_663.png", caption="Sensory Distribution", width=300)
    with col_img2:
    st.write("Phalen's Test Procedure")
    # Phalen's test is a key diagnostic physical exam for Carpal Tunnel [cite: 30]
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Phalens_test.jpg/640px-Phalens_test.jpg", caption="Special Tests", width=300)
    
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
