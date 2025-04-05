import pandas as pd

class SHLRecommendationEngine:
    def __init__(self):
        # Initialize with SHL product catalog data
        self.catalog = self._load_shl_catalog()
        
    def _load_shl_catalog(self):
        """
        Load and structure the SHL product catalog
        This would typically come from a database or API, but for demonstration
        we'll create a representative sample
        """
        # Sample catalog structure with key assessment information
        catalog_data = {
            'assessment_id': [
                'VERIFY-G+', 'VERIFY-N', 'VERIFY-V', 'OPQ32', 'MQ', 'MOTIVATION',
                'PREVUE', 'REMOTE_WORKER', 'SALESQ', 'CALL_CENTER', 'CODING_POTENTIAL',
                'EXEC_GLOBAL', 'SITUATIONAL_JUDGMENT'
            ],
            'name': [
                'Verify General Ability', 'Verify Numerical Reasoning', 'Verify Verbal Reasoning',
                'Occupational Personality Questionnaire', 'Motivation Questionnaire', 'Motivation Inventory',
                'Prevue Assessment', 'Remote Worker Assessment', 'SalesQ Assessment',
                'Call Center Assessment', 'Coding Potential Assessment', 'Executive Global Assessment',
                'Situational Judgment Test'
            ],
            'assessment_type': [
                'cognitive', 'cognitive', 'cognitive', 'personality', 'motivation', 'motivation',
                'mixed', 'behavioral', 'behavioral', 'mixed', 'skill', 'mixed', 'behavioral'
            ],
            'job_level': [
                'all', 'professional', 'professional', 'all', 'all', 'all',
                'all', 'all', 'sales', 'entry', 'technical', 'executive', 'all'
            ],
            'duration_minutes': [
                24, 18, 17, 25, 20, 15, 45, 20, 25, 30, 40, 60, 25
            ],
            'competencies': [
                ['problem solving', 'critical thinking', 'analysis'],
                ['numerical analysis', 'data interpretation', 'quantitative reasoning'],
                ['comprehension', 'verbal analysis', 'reasoning'],
                ['leadership', 'teamwork', 'resilience', 'communication', 'innovation'],
                ['drive', 'purpose', 'achievement', 'reward focus'],
                ['intrinsic drivers', 'extrinsic drivers', 'social drivers'],
                ['cognitive', 'interests', 'personality', 'abilities'],
                ['autonomy', 'self-management', 'communication', 'collaboration'],
                ['persuasion', 'resilience', 'drive', 'relationship building'],
                ['customer focus', 'attention to detail', 'problem solving'],
                ['logical thinking', 'algorithm design', 'analytical reasoning'],
                ['strategic thinking', 'influence', 'cross-cultural leadership'],
                ['judgment', 'decision making', 'situational awareness']
            ],
            'ideal_for': [
                'general screening', 'finance roles', 'knowledge workers', 'comprehensive personality assessment',
                'understanding motivational drivers', 'quick motivation assessment', 'holistic candidate evaluation',
                'remote work positions', 'sales positions', 'contact center roles', 'developer positions',
                'senior leadership', 'frontline managers'
            ],
            'language_availability': [
                'global', 'global', 'global', 'global', 'global', 'limited',
                'global', 'global', 'limited', 'global', 'global', 'limited', 'global'
            ]
        }
        
        return pd.DataFrame(catalog_data)
    
    def recommend(self, criteria):
        """
        Recommend SHL assessments based on given criteria
        
        Parameters:
        criteria (dict): Dictionary containing selection criteria
            Possible keys:
            - job_role (str): The target job role
            - job_level (str): The level of the position
            - assessment_focus (list): Competencies/skills to focus on
            - time_constraints (int): Maximum assessment time in minutes
            - required_languages (list): Required languages for the assessment
        
        Returns:
        DataFrame: Recommended assessments sorted by relevance score
        """
        # Start with full catalog
        recommendations = self.catalog.copy()
        recommendations['relevance_score'] = 0
        
        # Apply filters and scoring based on criteria
        if 'job_level' in criteria:
            # Filter for job level compatibility or 'all'
            level_mask = (recommendations['job_level'] == criteria['job_level']) | (recommendations['job_level'] == 'all')
            recommendations = recommendations[level_mask]
            
        if 'time_constraints' in criteria:
            # Filter by maximum duration
            recommendations = recommendations[recommendations['duration_minutes'] <= criteria['time_constraints']]
            
        if 'required_languages' in criteria and criteria['required_languages']:
            # Filter by language availability (simplified)
            # This would need to be more sophisticated in a real implementation
            recommendations = recommendations[recommendations['language_availability'] == 'global']
            
        if 'job_role' in criteria:
            # Score by relevance to job role
            job_keywords = self._extract_keywords(criteria['job_role'])
            
            # Check ideal_for field for matches
            for idx, row in recommendations.iterrows():
                ideal_keywords = self._extract_keywords(row['ideal_for'])
                match_score = len(set(job_keywords) & set(ideal_keywords)) * 2
                recommendations.at[idx, 'relevance_score'] += match_score
        
        if 'assessment_focus' in criteria:
            # Score by competency coverage
            for idx, row in recommendations.iterrows():
                competency_matches = sum(1 for comp in criteria['assessment_focus'] 
                                       if any(comp.lower() in c.lower() for c in row['competencies']))
                recommendations.at[idx, 'relevance_score'] += competency_matches * 3
                
        # Sort by relevance score
        recommendations = recommendations.sort_values(by='relevance_score', ascending=False)
        
        # Return the top recommendations
        return recommendations[['assessment_id', 'name', 'assessment_type', 'competencies', 
                               'duration_minutes', 'ideal_for', 'relevance_score']]
        
    def _extract_keywords(self, text):
        """Extract keywords from a text string"""
        # Simple keyword extraction (would be more sophisticated in a real implementation)
        if isinstance(text, str):
            return [word.lower() for word in text.replace(',', ' ').split()]
        return []

    def get_assessment_details(self, assessment_id):
        """Get detailed information about a specific assessment"""
        result = self.catalog[self.catalog['assessment_id'] == assessment_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
