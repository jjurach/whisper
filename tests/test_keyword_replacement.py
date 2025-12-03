import unittest
import re


def process_text_with_llm(text):
    """
    Processes the transcribed text by replacing spoken punctuation commands
    with actual punctuation marks, aligned with Apple's dictation commands.
    """
    if not text:
        return text

    print(f"Processing text '{text}' with keyword punctuation replacement...", flush=True)

    # Order: longer phrases first to prevent partial matches
    replacements = {
        # Multi-word commands first
        "question mark": "?",
        "exclamation point": "!",
        "new paragraph": "\n\n",
        "new line": "\n",
        "open quote": "\"",
        "close quote": "\"",
        "dollar sign": "$",
        "open parenthesis": "(",
        "close parenthesis": ")",
        # Single-word commands
        "period": ".",
        "comma": ",",
        "colon": ":",
        "semicolon": ";",
        "hashtag": "#",
    }

    # Case-insensitive word boundary replacement
    for keyword, punctuation in replacements.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        text = re.sub(pattern, punctuation, text, flags=re.IGNORECASE)

    return text


class TestKeywordReplacement(unittest.TestCase):
    """Test suite for Apple-standard keyword-based punctuation replacement."""

    def test_basic_punctuation(self):
        self.assertEqual(process_text_with_llm("This is a test period"), "This is a test.")
        self.assertEqual(process_text_with_llm("Apples COMMA oranges"), "Apples,oranges")
        self.assertEqual(process_text_with_llm("How much dollar sign"), "How much$")

    def test_multi_word_commands(self):
        self.assertEqual(process_text_with_llm("What time is it question mark"), "What time is it?")
        self.assertEqual(process_text_with_llm("Wow exclamation point"), "Wow!")

    def test_phrase_ordering(self):
        # Ensure "question mark" works even with "question" in text
        input_text = "She asked a question mark"
        expected = "She asked a question?"
        self.assertEqual(process_text_with_llm(input_text), expected)

    def test_no_false_matches(self):
        # Should not replace partial words
        self.assertEqual(process_text_with_llm("Periodic table"), "Periodic table")
        self.assertEqual(process_text_with_llm("Hashtag rocks"), "Hashtag rocks")

    def test_whitespace_preservation(self):
        input_text = "Word1  comma  Word2"
        expected = "Word1  ,  Word2"
        self.assertEqual(process_text_with_llm(input_text), expected)

    def test_multiple_replacements(self):
        input_text = "Hello world period How are you question mark"
        expected = "Hello world. How are you?"
        self.assertEqual(process_text_with_llm(input_text), expected)

    def test_new_paragraph_formatting(self):
        input_text = "First sentence period new paragraph Second sentence"
        expected = "First sentence.\n\nSecond sentence"
        self.assertEqual(process_text_with_llm(input_text), expected)

    def test_case_insensitive_variations(self):
        self.assertEqual(process_text_with_llm("PERIOD"), ".")
        self.assertEqual(process_text_with_llm("Period"), ".")
        self.assertEqual(process_text_with_llm("period"), ".")

    def test_empty_and_none_inputs(self):
        self.assertEqual(process_text_with_llm(""), "")
        self.assertIsNone(process_text_with_llm(None))

    def test_symbols_and_special_chars(self):
        self.assertEqual(process_text_with_llm("Cost is fifty dollar sign"), "Cost is fifty $")
        self.assertEqual(process_text_with_llm("Use hashtag"), "Use #")

    def test_quotes_and_parentheses(self):
        self.assertEqual(process_text_with_llm("He said open quote hello close quote"), "He said \"hello\"")
        self.assertEqual(process_text_with_llm("Use open parenthesis custom close parenthesis keyword"), "Use (custom) keyword")

    def test_colon_and_semicolon(self):
        self.assertEqual(process_text_with_llm("Time colon five"), "Time: five")
        self.assertEqual(process_text_with_llm("Item one semicolon item two"), "Item one; item two")

    def test_new_line_command(self):
        input_text = "Line one new line Line two"
        expected = "Line one\nLine two"
        self.assertEqual(process_text_with_llm(input_text), expected)


if __name__ == "__main__":
    unittest.main()