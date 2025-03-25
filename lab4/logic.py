from const import WORDS


def process_search(term: str) -> str:
    processed_words = []
    for word in WORDS:
        if word == term:
            processed_words.append(highlight_word(word))
        else:
            processed_words.append(word)
    return ' '.join(processed_words)


def highlight_word(word: str) -> str:
    return f'<span style="background-color: red; color: white;">{word}</span>'
