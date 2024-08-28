import re
import spacy
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:
    def __init__(self, data, noOfQues):
        self.summary = self.remove_bracketed_text(data)  
        self.noOfQues = noOfQues
        self.nlp = spacy.load("en_core_web_md")
        
       
        common_words = {"the", "a", "an", "this", "that", "these", "those", "in", "on", "at", "for", "with"}
        pronouns = {"I", "me", "you", "he", "him", "she", "her", "it", "we", "us", "they", "them", "my", "your", 
                    "his", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs"}
        
        
        self.common_words = common_words.union(word.capitalize() for word in common_words)
        self.pronouns = pronouns.union(word.capitalize() for word in pronouns)

    def remove_bracketed_text(self, text):
         return re.sub(r'\(.*?[-_=+*!%$@)]', '', text)

    def get_trivial_sentences(self):
        doc = self.nlp(self.summary)
        trivial_sentences = []
        for sent in doc.sents:
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                trivial_sentences.append({"original": sent.text, "trivial": trivial})
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        noun_phrases = [chunk.text for chunk in sentence.noun_chunks 
                        if not self.contains_pronouns(chunk.text) and not self.is_common_word(chunk.text)]
        
        if not noun_phrases or len(sentence) < 5:
            return None
        
        
        sentence_tokens = [token.text for token in sentence]
        
      
        middle_index = len(sentence_tokens) // 2
        for i, token in enumerate(sentence_tokens):
            if token in noun_phrases:
                replace_phrase = token
                break
        else:
            replace_phrase = noun_phrases[0]

        replace_index = sentence_tokens.index(replace_phrase)
        

        if replace_index <= middle_index:
            for i in range(middle_index + 1, len(sentence_tokens)):
                if sentence_tokens[i] in noun_phrases:
                    replace_phrase = sentence_tokens[i]
                    replace_index = sentence_tokens.index(replace_phrase)
                    break
        
        sentence_tokens[replace_index] = "__________"
        sentence_text = ' '.join(sentence_tokens)

        trivial = {
            "Question": sentence_text,
            "Answer": replace_phrase,
            "Similar": self.answer_options(replace_phrase.split()[0])
        }
        return trivial

    def contains_pronouns(self, phrase):
        return any(word in self.pronouns for word in phrase.split())

    def is_common_word(self, text):
        return text.lower() in self.common_words or text in self.common_words

    def answer_options(self, word):
        token = self.nlp(word)[0]
        similar_words = set()


        if token.has_vector:
            similar_words = {similar.lower_ for similar in token.vocab 
                             if token.similarity(similar) > 0.5 and similar.is_alpha and similar.lower_ != word.lower()}


        synsets = wn.synsets(word, pos="n")
        if synsets:
            hypernym = synsets[0].hypernyms()[0] if synsets[0].hypernyms() else None
            if hypernym:
                similar_words.update(hyponym.lemmas()[0].name().replace("_", " ") for hyponym in hypernym.hyponyms())

        similar_words -= self.common_words
        return list(similar_words)[:4] if similar_words else ["No similar options available"]

    def contains_number(self, sentence):
        return any(char.isdigit() for char in sentence)

    def increment_number(self, sentence):
        def increment_match(match):
            number = int(match.group())
            return str(number + 1)
        
        return re.sub(r'\d+', increment_match, sentence)

    def generate_false_statement(self, sentence):
        if self.contains_number(sentence):
            return self.increment_number(sentence)
        return sentence

    def generate_true_false(self, sentence):
        if np.random.choice([True, False]):
            return {"Question": sentence, "Answer": "True"}
        else:
            false_statement = self.generate_false_statement(sentence)
            return {"Question": false_statement, "Answer": "False"}

    def generate_test(self):
        trivial_pairs = self.get_trivial_sentences()
        question_types = ["fill-in-the-blank", "true-false"]
        questions, answers = [], []

        for i in range(min(self.noOfQues, len(trivial_pairs))):
            q_type = np.random.choice(question_types)
            qa = trivial_pairs[i]["trivial"] if q_type == "fill-in-the-blank" else self.generate_true_false(trivial_pairs[i]["original"])
            questions.append(qa["Question"])
            answers.append(qa["Answer"])

        return questions, answers
