import re
import nltk
import spacy
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:
    def __init__(self, data, noOfQues):
        self.summary = data
        self.noOfQues = noOfQues
        self.nlp = spacy.load("en_core_web_md")
        self.common_words = set(["the", "a", "an", "this", "that", "these", "those", "in", "on", "at", "for", "with"])

    def get_trivial_sentences(self):
        doc = self.nlp(self.summary)
        trivial_sentences = []
        for sent in doc.sents:
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                trivial_sentences.append({"original": sent.text, "trivial": trivial})
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        noun_phrases = [chunk.text for chunk in sentence.noun_chunks]
        
        if len(noun_phrases) == 0 or len(sentence) < 5:
            return None
        
        replace_phrase = noun_phrases[0]
        
        if len(replace_phrase.split()) < 2 and replace_phrase.islower():
            return None
        
        blanks_phrase = "__________"
        sentence_text = sentence.text.replace(replace_phrase, blanks_phrase, 1)

        trivial = {
            "Question": sentence_text,
            "Answer": replace_phrase,
            "Similar": self.answer_options(replace_phrase.split()[0])
        }
        return trivial

    def answer_options(self, word):
        similar_words = set()
        token = self.nlp(word)[0]

        if token.has_vector:
            for similar in token.vocab:
                if token.similarity(similar) > 0.5 and similar.is_alpha and similar.lower_ != word.lower():
                    similar_words.add(similar.lower_)

        synsets = wn.synsets(word, pos="n")
        if synsets:
            hypernym = synsets[0].hypernyms()[0] if synsets[0].hypernyms() else None
            if hypernym:
                for hyponym in hypernym.hyponyms():
                    similar_word = hyponym.lemmas()[0].name().replace("_", " ")
                    if similar_word != word:
                        similar_words.add(similar_word)

        similar_words = similar_words - self.common_words
        return list(similar_words)[:4] if similar_words else ["No similar options available"]
    
    # def generate_false_statement(self, sentence):
    #         # This method will slightly alter a sentence to generate a false statement.
    #         altered_sentence = sentence
            
    #         # Randomly select a word to alter (like a name, year, or keyword).
    #         doc = self.nlp(sentence)
    #         for token in doc:
    #             if token.ent_type_ in ["PERSON", "ORG", "DATE"] or token.pos_ in ["NOUN", "PROPN", "NUM"]:
    #                 if token.ent_type_ == "DATE" and token.like_num:
    #                     # Change the year by a small amount
    #                     altered_sentence = sentence.replace(token.text, str(int(token.text) + np.random.choice([-1, 1, 5, -5])))
    #                 elif token.ent_type_ == "PERSON" or token.ent_type_ == "ORG":
    #                     # Replace the entity with a similar one from WordNet
    #                     similar = self.answer_options(token.text)
    #                     if similar:
    #                         altered_sentence = sentence.replace(token.text, similar[0])
    #                 break  



    def generate_true_false(self, sentence):
        # Return the original sentence as the true/false question with a "True" answer.
        return {"Question": sentence, "Answer": "True"}

    def generate_test(self):
        questions = []
        answers = []

        trivial_pairs = self.get_trivial_sentences()
        question_types = ["fill-in-the-blank", "true-false"]

        for i in range(min(int(self.noOfQues), len(trivial_pairs))):
            q_type = np.random.choice(question_types)
            if q_type == "fill-in-the-blank":
                qa = trivial_pairs[i]["trivial"]
                questions.append(qa["Question"])
                answers.append(qa["Answer"])
            elif q_type == "true-false":
                qa = self.generate_true_false(trivial_pairs[i]["original"])
                questions.append(qa["Question"])
                answers.append(qa["Answer"])

        return questions, answers
