QUESTION_BANK = {
    "python": [
        "What are the main features of Python?",
        "What is the difference between a list and a tuple?",
        "What are Python dictionaries, and how do they work?",
        "Explain the difference between == and is.",
        "What is exception handling in Python?",
    ],
    "sql": [
        "What is the difference between WHERE and HAVING?",
        "What is a primary key?",
        "Explain the different types of SQL joins.",
        "What is the difference between DELETE and TRUNCATE?",
        "What is database normalization?",
    ],
    "general": [
        "Tell me about yourself.",
        "Describe a technical project you have worked on.",
        "How do you approach solving a difficult problem?",
        "How do you debug an issue in your code?",
        "Why are you interested in this role?",
    ],
}


def get_questions(topic: str) -> list[str]:
    topic_key = topic.strip().lower()

    if topic_key in QUESTION_BANK:
        return QUESTION_BANK[topic_key]

    return QUESTION_BANK["general"]