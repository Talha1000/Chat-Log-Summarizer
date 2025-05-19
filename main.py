import os
import sys
from utils import parse_chat_log, get_message_stats, get_keywords, summarize_chat, generate_one_line_summary


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat_lines = f.readlines()

    user_msgs, ai_msgs = parse_chat_log(chat_lines)
    stats = get_message_stats(user_msgs, ai_msgs)
    keywords = get_keywords(user_msgs + ai_msgs, use_tfidf=True)

    # Pass only keywords to generate_one_line_summary
    one_line_summary = generate_one_line_summary(keywords)

    summary = summarize_chat(stats, keywords, one_line_summary)

    print(f"\nSummary for {file_path}:")
    print(summary)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py chat.txt")
        return

    path = sys.argv[1]

    if os.path.isdir(path):
        for file_name in os.listdir(path):
            if file_name.endswith(".txt"):
                process_file(os.path.join(path, file_name))
    else:
        process_file(path)


if __name__ == '__main__':
    main()
