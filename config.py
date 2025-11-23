KEYWORD_CATEGORIES = {
    "data_retention": ["retain", "storage period", "delete after", "keep for", "dispose", "retention period"],
    "user_consent": ["consent", "opt-in", "opt-out", "unsubscribe", "agree", "permission", "authorization"],
    "breach_notification": ["breach", "security incident", "notify", "unauthorized access", "data loss", "security breach"],
    "user_rights": ["right to access", "right to erasure", "right to rectification", "data portability", "access your data"],
    "data_collection": ["collect", "gather", "obtain", "receive", "acquire", "personal information we collect"],
    "third_party_sharing": ["share with", "third party", "service provider", "partner", "affiliate", "transfer to"],
    "data_protection_officer": ["data protection officer", "dpo", "privacy officer"],
    "cross_border": ["cross border", "transfer outside", "international transfer"],
    "data_processing_agreement": ["data processing agreement", "dpa", "processor"],
    "privacy_notice": ["privacy notice", "privacy policy"],
    "data_inventory": ["data inventory", "record of processing"],
    "purpose_limitation": ["purpose limitation", "specific purpose"],
    "access_control": ["access control", "role-based access", "rbac"]
}

# Map our categories to Excel domains
CATEGORY_TO_DOMAIN = {
    "data_retention": "Information Lifecycle Management",
    "user_consent": "Legal and Regulatory", 
    "breach_notification": "Incident and Breach Management",
    "user_rights": "Data Subject Rights",
    "data_collection": "Information Lifecycle Management",
    "third_party_sharing": "Third Party Oversight",
    "data_protection_officer": "Governance and Operating Model",
    "cross_border": "Legal and Regulatory",
    "data_processing_agreement": "Third Party Oversight",
    "privacy_notice": "Policies, Processes and Guidelines",
    "data_inventory": "Records Management",
    "purpose_limitation": "Information Lifecycle Management",
    "access_control": "Data Security"
}

EXCEL_COLUMNS = {
    'domain': 'Domain',
    'keywords': 'Keywords', 
    'observation': 'Observation',
    'control_ref': 'Control Ref'
}