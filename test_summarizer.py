# test_summarizer.py
from comprehensive_summarizer import ComprehensiveObservationSummarizer

def test_specific_keywords():
    summarizer = ComprehensiveObservationSummarizer()
    
    # Test with your exact data
    test_cases = [
        {
            'keyword': 'Data Protection Officer',
            'observation': '''• If you wish to request access to or to rectify your Personal Data or withdraw/limit your consent, you may send your request in writing to the following. • How You Can Contact Us Any questions, comments and requests regarding this Privacy Notice are welcomed and should be addressed to: Data Protection'''
        },
        {
            'keyword': 'Access Control', 
            'observation': '• System access controls prevent unauthorized changes to personal data'
        },
        {
            'keyword': 'Right to Erasure',
            'observation': '• Users can request deletion of their personal data by submitting a written request'
        }
    ]
    
    for test in test_cases:
        result = summarizer.generate_concise_observation(test['observation'], test['keyword'])
        print(f"Keyword: {test['keyword']}")
        print(f"Input: {test['observation'][:100]}...")
        print(f"Output: {result}")
        print("---")

if __name__ == "__main__":
    test_specific_keywords()