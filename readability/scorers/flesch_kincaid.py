from readability.exceptions import ReadabilityException


class Result:
    def __init__(self, score):
        self.score = score

    def __str__(self):
        return "{}".format(self.score)


class FleschKincaid:
    def __init__(self, stats):
        self._stats = stats
        if stats.num_words < 0:  # ORIGINALLY HUNDRED
            raise ReadabilityException('0 words required.')

    def score(self):
        score = self._score()
        return Result(
            score=score
        )

    def _score(self):
        stats = self._stats
        return (0.38 * stats.avg_words_per_sentence +
                11.8 * stats.avg_syllables_per_word) - 15.59
