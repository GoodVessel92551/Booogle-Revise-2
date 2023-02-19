import numpy as np
import pickle,csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

with open("ai/generation/generation.pkl", "rb") as f:
    clf = pickle.load(f)
    vectorizer = pickle.load(f)


def prompt(prompt):
    X = vectorizer.transform([prompt])
    label = clf.predict(X)[0]
    return label
