import re
import nltk
import spacy
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:
    def __init__(self, data, noOfQues):
        self.summary = data
        self.noOfQues = noOfQues
        self.nlp = spacy.load("en_core_web_md")  # Ensure the correct model with word vectors
        self.common_words = set(["the", "a", "an", "this", "that", "these", "those", "in", "on", "at", "for", "with"])

    def __init__(self, data, noOfQues):
        self.summary = data
        self.noOfQues = noOfQues
        self.nlp = spacy.load("en_core_web_md")  # Ensure the correct model with word vectors

    def get_trivial_sentences(self):
        doc = self.nlp(self.summary)
        trivial_sentences = []
        for sent in doc.sents:
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                trivial_sentences.append(trivial)
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        noun_phrases = [chunk.text for chunk in sentence.noun_chunks]
        
        # Only proceed if there's at least one noun phrase and the sentence has meaningful length
        if len(noun_phrases) == 0 or len(sentence) < 5:
            return None
        
        replace_phrase = noun_phrases[0]
        
        # Check if the replace phrase is a valid, meaningful noun
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

        # Handle missing vectors with a fallback
        if token.has_vector:
            for similar in token.vocab:
                if token.similarity(similar) > 0.5 and similar.is_alpha and similar.lower_ != word.lower():
                    similar_words.add(similar.lower_)

        # Add similar words from WordNet
        synsets = wn.synsets(word, pos="n")
        if synsets:
            hypernym = synsets[0].hypernyms()[0]
            for hyponym in hypernym.hyponyms():
                similar_word = hyponym.lemmas()[0].name().replace("_", " ")
                if similar_word != word:
                    similar_words.add(similar_word)

        return list(similar_words)[:4]

    def generate_true_false(self, sentence):
        # If sentence is a string, use it directly
        if isinstance(sentence, str):
            question = sentence + " (True/False)"
        else:
            question = sentence.text + " (True/False)"
    
        answer = "True" if np.random.rand() > 0.5 else "False"
        return {"Question": question, "Answer": answer}

    def generate_test(self):
        questions = []
        answers = []

        trivial_pairs = self.get_trivial_sentences()
        question_types = ["fill-in-the-blank", "true-false"]

        for i in range(min(int(self.noOfQues), len(trivial_pairs))):
            q_type = np.random.choice(question_types)
            if q_type == "fill-in-the-blank":
                qa = trivial_pairs[i]
                questions.append(qa["Question"])
                answers.append(qa["Answer"])
            elif q_type == "true-false":
                qa = self.generate_true_false(trivial_pairs[i]["Question"])
                questions.append(qa["Question"])
                answers.append(qa["Answer"])

        return questions, answers
