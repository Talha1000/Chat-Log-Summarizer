from nltk.corpus import stopwords
import re
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# Download stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))


def parse_chat_log(lines):
    """Extract user and AI messages from chat log lines."""
    user_msgs, ai_msgs = [], []
    for line in lines:
        if line.startswith("User:"):
            user_msgs.append(line[len("User:"):].strip())
        elif line.startswith("AI:"):
            ai_msgs.append(line[len("AI:"):].strip())
    return user_msgs, ai_msgs


def get_message_stats(user_msgs, ai_msgs):
    """Count total messages and separate counts for user and AI."""
    return {
        "total": len(user_msgs) + len(ai_msgs),
        "user": len(user_msgs),
        "ai": len(ai_msgs)
    }


def get_keywords(messages, top_n=5, use_tfidf=True):
    """
    Extract top N keywords using TF-IDF by default.
    If use_tfidf=False, fallback to frequency-based extraction.
    """
    if use_tfidf:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
        X = vectorizer.fit_transform(messages)
        return vectorizer.get_feature_names_out().tolist()
    else:
        all_text = " ".join(messages).lower()
        words = re.findall(r"\b[a-z]{2,}\b", all_text)
        filtered_words = [w for w in words if w not in STOPWORDS]
        counter = Counter(filtered_words)
        return [kw for kw, _ in counter.most_common(top_n)]


def generate_one_line_summary(keywords):
    """Generate a clean one-line summary from keywords with natural formatting."""
    if not keywords:
        return "The conversation covered general topics."

    formatted = [kw.capitalize() for kw in keywords]

    if len(formatted) == 1:
        return f"The conversation focused on {formatted[0]}."
    elif len(formatted) == 2:
        return f"The conversation focused on {formatted[0]} and {formatted[1]}."
    else:
        return f"The conversation focused on {', '.join(formatted[:-1])}, and {formatted[-1]}."


def summarize_chat(stats, keywords, one_line_summary):
    """Generate the full summary text."""
    return f"""Summary:
- The conversation had {stats['total']} exchanges.
- The user sent {stats['user']} messages; the AI sent {stats['ai']} messages.
- {one_line_summary}
- Most common keywords: {', '.join(keywords)}
"""
