import streamlit as st
import pandas as pd
from shl_engine import SHLRecommendationEngine

def main():
    st.title("SHL Assessment Recommendation Tool")
    
    # Initialize the recommendation engine
    engine = SHLRecommendationEngine()
    
    # Create sidebar for inputs
    st.sidebar.header("Input Criteria")
    
    job_role = st.sidebar.text_input("Job Role", 
                                     placeholder="e.g., Software Developer, Sales Manager")
    
    job_level_options = ["entry", "professional", "manager", "executive", "all"]
    job_level = st.sidebar.selectbox("Job Level", job_level_options)
    
    # Multi-select for competencies
    all_competencies = [
        "leadership", "teamwork", "communication", "problem solving", 
        "critical thinking", "innovation", "resilience", "data analysis",
        "customer focus", "sales ability", "technical skill", "coding",
        "strategic thinking", "decision making", "people management"
    ]
    selected_competencies = st.sidebar.multiselect(
        "Key Competencies", all_competencies
    )
    
    # Time constraint slider
    max_time = st.sidebar.slider("Maximum Assessment Time (minutes)", 
                               min_value=10, max_value=60, value=30, step=5)
    
    # Language requirements (simplified)
    global_only = st.sidebar.checkbox("Must be available globally", value=True)
    
    # Button to get recommendations
    if st.sidebar.button("Get Recommendations"):
        # Build criteria dictionary
        criteria = {
            "job_role": job_role,
            "job_level": job_level,
            "assessment_focus": selected_competencies,
            "time_constraints": max_time
        }
        
        if global_only:
            criteria["required_languages"] = ["global"]
        
        # Get recommendations
        recommendations = engine.recommend(criteria)
        
        # Display recommendations
        st.header("Recommended SHL Assessments")
        
        if recommendations.empty:
            st.warning("No matching assessments found. Try adjusting your criteria.")
        else:
            # Display each recommendation as a card
            for idx, rec in recommendations.iterrows():
                with st.expander(f"{rec['name']} (Relevance: {rec['relevance_score']})"):
                    st.write(f"**Assessment ID:** {rec['assessment_id']}")
                    st.write(f"**Type:** {rec['assessment_type'].capitalize()}")
                    st.write(f"**Duration:** {rec['duration_minutes']} minutes")
                    st.write(f"**Ideal for:** {rec['ideal_for']}")
                    st.write("**Key competencies assessed:**")
                    for comp in rec['competencies']:
                        st.write(f"- {comp.capitalize()}")
                    
                    # Add a button to select this assessment
                    if st.button(f"Select {rec['assessment_id']}", key=f"select_{idx}"):
                        st.session_state.selected_assessment = rec['assessment_id']
                        
            if 'selected_assessment' in st.session_state:
                st.success(f"You've selected: {st.session_state.selected_assessment}")
                
    # Add some information about SHL assessments
    st.sidebar.markdown("---")
    st.sidebar.header("About SHL Assessments")
    st.sidebar.info(
        "SHL offers a comprehensive range of psychometric assessments "
        "for talent acquisition and development. These include cognitive ability tests, "
        "personality questionnaires, motivation assessments, and situation judgment tests."
    )

if __name__ == "__main__":
    main()