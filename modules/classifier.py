import re


# Keyword database for each legal category
LEGAL_CATEGORIES = {
    "Criminal Law": {
        "strong": [
            "fir", "arrest", "accused", "charge sheet", "murder", "theft", "robbery", "kidnapping",
            "assault", "fraud", "criminal", "police", "investigation", "offence", "crime", "complaint", 
            "victim", "witness","ipc", "evidence", "bail"
        ],
        "medium": [
            "station", "suspect", "court case", "prosecution", "conviction", "sentence", "custody"
        ]
    },
    "Contract Law": {
        "strong": [
            "agreement", "contract", "party", "terms and conditions", "obligation", "breach", 
            "consideration", "termination", "nda", "service agreement", "contractor", "liability"
        ],
        "medium": [
            "clause", "payment terms", "mutual consent", "binding", "legal obligation"
        ]
    },
    "Corporate Law": {
        "strong": [
            "company", "board of directors", "shareholder", "shares", "corporation", "annual meeting",
            "memorandum of association", "articles of association", "director", "compliance", "merger",
            "acquisition"
        ],
        "medium": [
            "business entity", "corporate governance", "stakeholder", "registered office"
        ]
    },
    "Property Law": {
        "strong": [
            "property", "land", "sale deed", "lease", "tenant", "ownership", "real estate", "mortgage",
            "rent agreement", "possession", "registry", "transfer deed"
        ],
        "medium": [
            "plot", "house", "building", "landlord", "boundary", "encumbrance"
        ]
    },
    "Intellectual Property Law": {
        "strong": [
            "patent", "copyright", "trademark", "intellectual property", "licensing", "infringement",
            "brand name", "logo", "trade secret"
        ],
        "medium": [
            "creative work", "ownership rights", "exclusive rights", "registered mark"
        ]
    },
    "Employment Law": {
        "strong": [
            "employee", "employer", "salary", "wages", "employment agreement", "termination letter",
            "resignation", "workplace", "labour", "labor", "hr policy", "payroll"
        ],
        "medium": [
            "leave policy", "working hours", "compensation", "benefits", "attendance"
        ]
    },
    "Other": {
        "strong": [],
        "medium": []
    }
}


def clean_text(text):
    """Convert to lowercase and remove punctuation for keyword matching"""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def classify_document(text):
    """
    Classify document into legal category using weighted keyword scoring.
    Returns primary category, confidence percentage, and scores for all categories.
    """
    text = clean_text(text)
    scores = {}

    # Calculate weighted score for each category
    for category, keywords in LEGAL_CATEGORIES.items():
        score = 0
        for keyword in keywords["strong"]:
            score += text.count(keyword) * 3
        for keyword in keywords["medium"]:
            score += text.count(keyword)
        scores[category] = score

    # Find best matching category
    best_category = max(scores, key=scores.get)
    highest_score = scores[best_category]
    total_score = sum(scores.values())

    # No keywords matched
    if highest_score == 0:
        all_scores = [
            {"category": cat, "score": 0, "percentage": 0}
            for cat in LEGAL_CATEGORIES.keys()
        ]
        return {
            "category": "Other",
            "confidence": 0,
            "all_scores": all_scores
        }

    # Calculate percentage distribution
    all_scores = []
    for category, score in scores.items():
        if score == 0:
            all_scores.append({"category": category, "score": 0, "percentage": 0})
        else:
            percentage = round((score / total_score) * 100, 2)
            all_scores.append({
                "category": category,
                "score": score,
                "percentage": percentage
            })

    # Sort by confidence (highest first)
    all_scores.sort(key=lambda x: x["percentage"], reverse=True)

    return {
        "category": best_category,
        "confidence": round((highest_score / total_score) * 100, 2),
        "all_scores": all_scores
    }