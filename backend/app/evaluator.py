
def evaluate_answer(answer: str, question: str = "") -> dict:
    word_count = len(answer.split())
    answer_lower = answer.lower()
    question_lower = question.lower()

    # Score based on answer length
    if word_count < 10:
        score = 20
        feedback = "Your answer is too short. Add more explanation and an example."
    elif word_count < 30:
        score = 40
        feedback = "You have a starting point. Explain your idea in more detail."
    elif word_count < 60:
        score = 65
        feedback = "Good attempt. Add specific details or a practical example."
    elif word_count < 100:
        score = 80
        feedback = "Good level of detail. Make sure your answer directly addresses the question."
    else:
        score = 90
        feedback = "Detailed answer. Keep it focused and organized."

    # Look for relevant concepts in the answer
    keyword_topics = {
        "normalization": [
            "redundancy", "duplicate", "database", "table",
            "dependency", "1nf", "2nf", "3nf"
        ],
        "primary key": ["unique", "identify", "row", "record"],
        "foreign key": ["reference", "relationship", "table"],
        "oops": ["class", "object", "inheritance", "polymorphism"],
        "python": ["interpreted", "readable", "language"],
    }

    matched_keywords = []
    relevant_keywords = []

    for topic, keywords in keyword_topics.items():
        if topic in question_lower:
            relevant_keywords = keywords
            matched_keywords = [
                keyword for keyword in keywords
                if keyword in answer_lower
            ]
            break

    if relevant_keywords:
        if matched_keywords:
            score = min(score + 10, 100)
            feedback += (
                " You mentioned relevant concepts: "
                + ", ".join(matched_keywords) + "."
            )
        else:
            score = max(score - 10, 0)
            feedback += " Include key concepts related to the question."

    return {
        "score": score,
        "feedback": feedback,
    }
