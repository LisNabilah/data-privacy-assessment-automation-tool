# comprehensive_summarizer.py - COMPLETE VERSION
import spacy
import pandas as pd
from collections import defaultdict
import re

class ComprehensiveObservationSummarizer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("Please install spaCy model: python -m spacy download en_core_web_sm")
        
        # Define comprehensive keyword patterns
        self.keyword_patterns = {
            # DATA PROTECTION OFFICER & GOVERNANCE
            'data protection officer': {
                'contact': ['contact', 'address', 'reach out', 'write to', 'responsible for'],
                'oversight': ['oversight', 'monitor', 'ensure compliance', 'advise on'],
                'rights_management': ['access', 'rectify', 'withdraw', 'limit', 'consent', 'erasure']
            },
            'roles and responsibilities': {
                'accountability': ['responsible for', 'accountable for', 'duties include', 'role involves'],
                'tasks': ['perform', 'conduct', 'implement', 'manage', 'maintain'],
                'reporting': ['report to', 'escalate to', 'inform management']
            },
            
            # LAWFUL PROCESSING & CONSENT
            'lawful bases': {
                'legal_grounds': ['lawful basis', 'legal ground', 'legitimate interest', 'consent', 'contract', 'legal obligation'],
                'documentation': ['document', 'record', 'maintain records'],
                'compliance': ['comply with', 'in accordance with', 'based on']
            },
            'consent': {
                'obtaining': ['obtain consent', 'get consent', 'request consent', 'seek approval'],
                'management': ['manage consent', 'track consent', 'record consent', 'consent log'],
                'withdrawal': ['withdraw consent', 'revoke consent', 'opt-out', 'remove consent']
            },
            'minors': {
                'age_verification': ['verify age', 'age check', 'parental consent', 'guardian approval'],
                'protection': ['special protection', 'additional safeguards', 'child privacy'],
                'consent_rules': ['parental consent', 'guardian approval', 'age-based rules']
            },
            
            # PRIVACY DOCUMENTATION
            'privacy policy': {
                'content': ['describe', 'explain', 'outline', 'detail'],
                'rights': ['rights of', 'entitled to', 'can access'],
                'procedures': ['procedure for', 'process for', 'steps to']
            },
            'privacy notice': {
                'communication': ['inform', 'notify', 'disclose to', 'tell users'],
                'transparency': ['clear', 'transparent', 'easily accessible'],
                'timing': ['at collection', 'before processing', 'upon request']
            },
            
            # DATA GOVERNANCE
            'data classification': {
                'categorization': ['classify', 'categorize', 'label', 'tag'],
                'levels': ['confidential', 'restricted', 'public', 'internal'],
                'handling': ['handle according to', 'based on classification', 'appropriate safeguards']
            },
            'data management lifecycle': {
                'stages': ['collection', 'storage', 'processing', 'retention', 'disposal'],
                'controls': ['control at each stage', 'throughout lifecycle', 'end-to-end'],
                'policies': ['policies for each stage', 'lifecycle management']
            },
            
            # SECURITY CONTROLS
            'access control': {
                'authentication': ['authenticate', 'verify identity', 'login credentials'],
                'authorization': ['authorize', 'permissions', 'role-based', 'privileges'],
                'restriction': ['restrict access', 'limit access', 'prevent unauthorized']
            },
            'encryption': {
                'protection': ['encrypt', 'cipher', 'encode', 'cryptographic'],
                'data_types': ['data at rest', 'data in transit', 'storage encryption'],
                'standards': ['encryption standard', 'algorithm', 'key management']
            },
            'multi-factor authentication': {
                'verification': ['multiple factors', 'two-factor', 'biometric', 'token'],
                'security': ['enhance security', 'additional layer', 'strong authentication']
            },
            
            # DEFAULT PATTERNS (fallback)
            'default': {
                'implementation': ['implement', 'deploy', 'set up', 'establish'],
                'maintenance': ['maintain', 'update', 'review regularly'],
                'monitoring': ['monitor', 'track', 'oversee', 'supervise']
            }
        }

    def preprocess_text(self, text):
        """Clean and preprocess the text - THIS WAS MISSING!"""
        if pd.isna(text):
            return ""
        text = re.sub(r'[•\-\*]\s*', '', str(text))
        text = ' '.join(text.split())
        return text

    def get_patterns_for_keyword(self, keyword):
        """Find the best matching patterns for a given keyword"""
        keyword_lower = keyword.lower().strip()
        
        # Try to find the best match in our patterns
        for pattern_key, patterns in self.keyword_patterns.items():
            if pattern_key in keyword_lower or keyword_lower in pattern_key:
                return patterns
        
        # Try partial matching for multi-word keywords
        for pattern_key in self.keyword_patterns.keys():
            if any(word in keyword_lower for word in pattern_key.split()) or \
               any(word in pattern_key for word in keyword_lower.split()):
                return self.keyword_patterns[pattern_key]
        
        return self.keyword_patterns['default']
    
    def extract_key_actions(self, text, keyword):
        """Extract key actions relevant to the specific keyword"""
        responsibilities = defaultdict(list)
        patterns = self.get_patterns_for_keyword(keyword)
        
        text_lower = text.lower()
        
        # Check for each responsibility pattern
        for category, terms in patterns.items():
            for term in terms:
                if term in text_lower:
                    responsibilities[category].append(term)
        
        return responsibilities
    
    def generate_concise_observation(self, raw_observations, keyword):
        """Generate a concise observation tailored to the specific keyword"""
        if not raw_observations:
            return ""
        
        # Preprocess and combine all observations
        if isinstance(raw_observations, list):
            combined_text = ' '.join([self.preprocess_text(obs) for obs in raw_observations])
        else:
            combined_text = self.preprocess_text(raw_observations)
        
        if not combined_text.strip():
            return ""
        
        # Extract responsibilities
        responsibilities = self.extract_key_actions(combined_text, keyword)
        
        # Generate observation based on keyword category and extracted responsibilities
        observation = self._build_observation_by_keyword(keyword, responsibilities, combined_text)
        
        return observation
    
    def _build_observation_by_keyword(self, keyword, responsibilities, full_text):
        """Build observation based on keyword category"""
        keyword_lower = keyword.lower()
        
        # DATA PROTECTION OFFICER
        if any(kw in keyword_lower for kw in ['data protection officer', 'dpo']):
            return self._build_dpo_observation(responsibilities)
        
        # ROLES & RESPONSIBILITIES
        elif 'role' in keyword_lower or 'responsibilit' in keyword_lower:
            return self._build_roles_observation(responsibilities)
        
        # CONSENT MANAGEMENT
        elif 'consent' in keyword_lower:
            return self._build_consent_observation(responsibilities, full_text)
        
        # SECURITY CONTROLS
        elif any(kw in keyword_lower for kw in ['access control', 'encryption', 'firewall', 'antivirus', 'mfa']):
            return self._build_security_observation(keyword, responsibilities)
        
        # AUDITS & ASSESSMENTS
        elif any(kw in keyword_lower for kw in ['audit', 'assessment', 'impact assessment']):
            return self._build_audit_observation(responsibilities)
        
        # INDIVIDUAL RIGHTS
        elif any(kw in keyword_lower for kw in ['right to', 'can access', 'allowed to']):
            return self._build_rights_observation(keyword, responsibilities)
        
        # INCIDENT MANAGEMENT
        elif any(kw in keyword_lower for kw in ['breach', 'incident', 'response']):
            return self._build_incident_observation(responsibilities)
        
        # DEFAULT OBSERVATION BUILDER
        else:
            return self._build_general_observation(keyword, responsibilities, full_text)
    
    def _build_dpo_observation(self, responsibilities):
        """Build observation for Data Protection Officer"""
        parts = []
        if responsibilities['contact']:
            parts.append("Designated as primary contact")
        if responsibilities['oversight']:
            parts.append("responsible for compliance oversight")
        if responsibilities['rights_management']:
            parts.append("manages data subject rights requests")
        
        if parts:
            return "Serves as " + " and ".join(parts) + "."
        return "Responsible for data protection compliance and individual rights management."
    
    def _build_consent_observation(self, responsibilities, full_text):
        """Build observation for consent-related keywords"""
        if responsibilities['obtaining']:
            return "Procedures for obtaining and recording valid user consent."
        elif responsibilities['withdrawal']:
            return "Process for allowing users to withdraw consent easily."
        elif 'minor' in full_text or 'child' in full_text:
            return "Special consent requirements and verification for minors."
        else:
            return "Consent management and tracking procedures."
    
    def _build_security_observation(self, keyword, responsibilities):
        """Build observation for security controls"""
        control_type = keyword.lower()
        
        if 'access' in control_type:
            return "Controls to restrict and manage system/data access based on roles."
        elif 'encryption' in control_type:
            return "Data encryption for protection at rest and in transit."
        elif 'firewall' in control_type:
            return "Network security controls to monitor and filter traffic."
        elif 'authentication' in control_type:
            return "Multi-factor authentication for enhanced access security."
        else:
            return f"Security controls and measures for {keyword}."
    
    def _build_audit_observation(self, responsibilities):
        """Build observation for audits and assessments"""
        if responsibilities['evaluation']:
            return "Regular evaluation and review of controls and compliance."
        elif responsibilities['risk_assessment']:
            return "Assessment of privacy risks and implementation of mitigation measures."
        else:
            return "Audit procedures to verify compliance and identify improvements."
    
    def _build_roles_observation(self, responsibilities):
        return "Defined responsibilities and accountability framework."
    
    def _build_rights_observation(self, keyword, responsibilities):
        right_type = keyword.lower()
        if 'access' in right_type:
            return "Procedures for handling data access requests from individuals."
        elif 'erasure' in right_type or 'delete' in right_type:
            return "Process for data deletion requests and compliance verification."
        elif 'correct' in right_type or 'update' in right_type:
            return "Procedures for handling data correction requests."
        else:
            return f"Process for handling {keyword} requests."
    
    def _build_incident_observation(self, responsibilities):
        if responsibilities['response']:
            return "Incident response procedures and escalation protocols."
        elif responsibilities['notification']:
            return "Breach notification procedures to authorities and affected individuals."
        else:
            return "Incident management and response framework."
    
    def _build_general_observation(self, keyword, responsibilities, full_text):
        """Default observation builder"""
        if responsibilities['implementation']:
            return f"Implementation and maintenance of {keyword}."
        elif responsibilities['monitoring']:
            return f"Ongoing monitoring and oversight of {keyword}."
        else:
            # Extract the most relevant sentence as fallback
            sentences = [sent.text for sent in self.nlp(full_text[:500]).sents]
            if sentences and len(sentences[0]) > 20:
                return sentences[0][:150] + ("..." if len(sentences[0]) > 150 else "")
            return f"Provisions and procedures related to {keyword}."

# Test function
def test_summarizer():
    """Test the summarizer with sample data"""
    summarizer = ComprehensiveObservationSummarizer()
    
    test_cases = [
        {
            'keyword': 'Data Protection Officer',
            'observation': '• If you wish to request access to or to rectify your Personal Data or withdraw/limit your consent, you may send your request in writing to the following. • How You Can Contact Us Any questions, comments and requests regarding this Privacy Notice are welcomed and should be addressed to: Data Protection'
        },
        {
            'keyword': 'Access Control',
            'observation': '• System access controls prevent unauthorized changes to personal data'
        }
    ]
    
    for test in test_cases:
        result = summarizer.generate_concise_observation(test['observation'], test['keyword'])
        print(f"Keyword: {test['keyword']}")
        print(f"Output: {result}\n")

if __name__ == "__main__":
    test_summarizer()