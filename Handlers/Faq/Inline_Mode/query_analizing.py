from Handlers.Faq.Inline_Mode.keywords import get_all_words, get_all_answers


class QueryAnalizer:

    def __init__(self):
        self.words = list(get_all_words())
        self.answers = list(get_all_answers())

    def process_query(self, text):
        val = text.strip()
        # result = []
        # for word in self.words:
        #     if val in word:
        #         result.append(word)
        # return result

        return [word for word in self.words if val in word]

    def get_answers(self, words):
        result = []
        for z in words:
            for i, word in enumerate(self.words):
                if z in word:
                    result.append(self.answers[i])

        return result
