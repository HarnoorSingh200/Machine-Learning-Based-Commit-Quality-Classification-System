from .text import Analyzer
from .scorers import FleschKincaid
import nltk

class Readability:
    def __init__(self, text):
        self._analyzer = Analyzer()
        self._statistics = self._analyzer.analyze(text)

    def flesch_kincaid(self):
        """Calculate Flesch-Kincaid Grade Level."""
        return FleschKincaid(self._statistics).score()

    def statistics(self):
        return {
            'num_letters': self._statistics.num_letters,
            'num_words': self._statistics.num_words,
            'num_sentences': self._statistics.num_sentences,
            'num_polysyllabic_words': self._statistics.num_poly_syllable_words,
            'avg_words_per_sentence': self._statistics.avg_words_per_sentence,
            'avg_syllables_per_word': self._statistics.avg_syllables_per_word,
        }
