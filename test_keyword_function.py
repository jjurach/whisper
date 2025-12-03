#!/usr/bin/env python3
"""
Standalone test script for the keyword replacement functionality.
Tests the core logic without importing the full live_dictation module.
"""

import re


def process_text_with_llm(text):
    """
    Processes the transcribed text by replacing spoken punctuation commands
    with actual punctuation marks, aligned with Apple's dictation commands.
    """
    if not text:
        return text

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

    # Clean up extra spaces after punctuation (Apple dictation behavior)
    # Remove spaces after punctuation marks but not before
    text = re.sub(r'([.,!?;:\'\"])\s+', r'\1', text)

    return text


def run_tests():
    """Run comprehensive tests for the keyword replacement function."""
    tests_passed = 0
    tests_total = 0

    def assert_test(description, input_text, expected):
        nonlocal tests_passed, tests_total
        tests_total += 1
        result = process_text_with_llm(input_text)
        if result == expected:
            print(f"✅ {description}")
            tests_passed += 1
        else:
            print(f"❌ {description}")
            print(f"   Input: '{input_text}'")
            print(f"   Expected: '{expected}'")
            print(f"   Got: '{result}'")

    print("Testing Keyword-Based Punctuation Replacement")
    print("=" * 50)

    # Basic punctuation tests
    assert_test("Basic period replacement", "This is a test period", "This is a test.")
    assert_test("Basic comma replacement", "Apples comma oranges", "Apples, oranges")
    assert_test("Dollar sign replacement", "How much dollar sign", "How much$")

    # Multi-word commands
    assert_test("Question mark replacement", "What time is it question mark", "What time is it?")
    assert_test("Exclamation point replacement", "Wow exclamation point", "Wow!")

    # Quotes and formatting
    assert_test("Quote replacement", "She said open quote hello close quote", "She said \" hello \"")
    assert_test("Quote with proper spacing", "She said open quote hello close quote", "She said \" hello \"")

    # Parentheses
    assert_test("Parentheses replacement", "Use open parenthesis code close parenthesis", "Use ( code )")

    # Symbols
    assert_test("Colon replacement", "Time colon 3 PM", "Time: 3 PM")
    assert_test("Semicolon replacement", "First item semicolon second", "First item; second")
    assert_test("Hashtag replacement", "Check out hashtag python", "Check out # python")

    # Phrase ordering (longer phrases first)
    assert_test("Phrase ordering test", "She asked a question mark", "She asked a ?")

    # No false matches
    assert_test("No false match - periodic", "Periodic table", "Periodic table")
    assert_test("No false match - questionable", "Questionable actions", "Questionable actions")

    # Multiple replacements
    assert_test("Multiple replacements", "Hello world period How are you question mark",
               "Hello world. How are you?")

    # Formatting
    assert_test("New paragraph", "First sentence period new paragraph Second sentence",
               "First sentence . \n\n Second sentence")
    assert_test("New line", "Line one period new line Line two", "Line one . \n Line two")

    # Case insensitive
    assert_test("case insensitive - period", "PERIOD", ".")
    assert_test("case insensitive - question mark", "QUESTION MARK", "?")

    # Edge cases
    assert_test("Empty input", "", "")
    assert_test("None input", None, None)

    # Complex example
    complex_input = ("First paragraph period new paragraph "
                    "Second paragraph with comma a list colon item one semicolon item two period "
                    "Third paragraph with dollars dollar sign twenty five and hashtags hashtag python")
    complex_expected = ("First paragraph.\n\n"
                       "Second paragraph with , a list : item one ; item two. "
                       "Third paragraph with dollars $ twenty five and hashtags # python")
    assert_test("Complex formatting", complex_input, complex_expected)

    print("\n" + "=" * 50)
    print(f"Tests Passed: {tests_passed}/{tests_total}")

    if tests_passed == tests_total:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {tests_total - tests_passed} tests failed")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)