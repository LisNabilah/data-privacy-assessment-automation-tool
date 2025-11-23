import re
from config import KEYWORD_CATEGORIES, CATEGORY_TO_DOMAIN

def split_into_sentences(text):
    """
    Simple sentence splitter (no NLTK required)
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        sentence = re.sub(r'\s+', ' ', sentence)
        if len(sentence) > 10:
            clean_sentences.append(sentence)
    
    return clean_sentences

def extract_obligations(full_text, keyword_categories, category_to_domain):
    """
    Extract sentences and map them to domains
    """
    obligations = []
    sentences = split_into_sentences(full_text)
    
    print(f"Checking {len(sentences)} sentences for keywords...")
    
    for sentence in sentences:
        for category, keywords in keyword_categories.items():
            for keyword in keywords:
                if keyword.lower() in sentence.lower():
                    domain = category_to_domain.get(category, 'Unknown')
                    obligations.append({
                        'text': sentence,
                        'category': category,
                        'matched_keyword': keyword,
                        'domain': domain
                    })
                    break
    
    return obligations