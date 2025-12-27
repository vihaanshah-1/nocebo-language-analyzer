"""
Nocebo Language Analyzer
========================

This module provides a simple interface for analysing medical consent or
instruction text for potential nocebo-triggering language. It uses a
pre-trained logistic regression classifier (trained on a small dataset of
patient‑facing medical documents) to assign an anxiety risk score to each
sentence and highlights phrases that may induce negative expectations.

Functions
---------
``predict_nocebo_risk(text: str) -> List[dict]``
    Given a block of text, split it into sentences, score each sentence and
    return a list of dictionaries containing the sentence, predicted risk
    label (0 = neutral, 1 = mild, 2 = moderate, 3 = high) and the set of
    trigger categories detected.

``suggest_rewrite(sentence: str) -> str``
    Provide a neutral rewrite for a given sentence by replacing words that
    contribute to anxiety according to a simple replacement dictionary.

Usage example
-------------
>>> from nocebo_analyzer import predict_nocebo_risk, suggest_rewrite
>>> text = "You must not drive after sedation. Rare complications include stroke."
>>> results = predict_nocebo_risk(text)
>>> for res in results:
...     print(res['sentence'], res['label'], res['categories'])
>>> safe = suggest_rewrite(text)
>>> print(safe)

Note
----
This tool is intended for educational purposes only. It does not provide
medical advice and should not be used to make clinical decisions.
"""

import os
import re
from typing import List, Dict
import joblib

# Load the trained vectorizer and model from the pickle file on import
_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'nocebo_model.pkl')
_VECTORIZER, _MODEL = joblib.load(_MODEL_PATH)

# Define the same triggers used during training for category highlighting
_TRIGGERS = {
    'threat_intensity': [
        'dangerous', 'severe', 'fatal', 'high risk', 'life‑threatening',
        'death', 'stroke', 'brain death', 'paralysis', 'heart attack',
        'anaphylaxis', 'cardiac arrest', 'respiratory arrest',
        'rare complications', 'serious complications'
    ],
    'uncertainty': [
        'unknown', 'cannot guarantee', 'may not work', 'unpredictable',
        'possible', 'it is still possible', 'rare but possible', 'rarely',
        'if it does happen'
    ],
    'vivid_side_effects': [
        'nausea', 'vomiting', 'diarrhoea', 'diarrhea', 'constipation',
        'abdominal pain', 'pain', 'sting', 'burn', 'headache', 'itching',
        'itchy', 'rash', 'dizziness', 'swelling', 'bleeding', 'infection',
        'extravasation', 'allergic reaction', 'grogginess', 'dry mouth',
        'urinary retention', 'confusion', 'shortness of breath'
    ],
    'directive_harshness': [
        'must not', 'do not', 'stop taking', 'forbidden', 'you must',
        'you should', 'please', 'you will be asked', 'not to leave',
        'must', 'should', 'you should not', 'you will need'
    ],
}

# Replacement dictionary for rewriting sentences
_REPLACEMENTS = {
    'pain': 'discomfort',
    'severe': 'significant',
    'risk': 'chance',
    'complications': 'issues',
    'complication': 'issue',
    'death': 'very serious complications',
    'stroke': 'serious medical condition',
    'heart attack': 'serious cardiac condition',
    'vomiting': 'feeling sick',
    'nausea': 'feeling sick',
    'diarrhoea': 'loose stools',
    'diarrhea': 'loose stools',
    'constipation': 'difficulty with bowel movements',
    'allergic reaction': 'allergy',
    'anaphylaxis': 'severe allergy',
    'cardiac arrest': 'heart stopping',
    'respiratory arrest': 'breathing stopping',
    'brain death': 'loss of brain function',
    'paralysis': 'loss of movement',
    'itchy': 'irritated',
    'rash': 'skin irritation',
    'bleeding': 'bleeding (rare)',
    'swelling': 'swelling (temporary)',
    'shortness of breath': 'difficulty breathing',
    'must not': 'should not',
    'do not': 'please avoid',
    'stop taking': 'please stop taking',
    'you must': 'you should',
    'you will be asked': 'we will ask you',
    'you will need': 'you may need',
}


def _split_sentences(text: str) -> List[str]:
    """Split input text into a list of sentences using a simple regex."""
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]


def _detect_categories(sentence: str) -> List[str]:
    """Return a list of trigger categories present in a sentence."""
    categories = []
    lower = sentence.lower()
    for cat, words in _TRIGGERS.items():
        for w in words:
            if w in lower:
                categories.append(cat)
                break
    return categories


def predict_nocebo_risk(text: str) -> List[Dict[str, object]]:
    """Analyse a block of text for nocebo risk.

    Parameters
    ----------
    text: str
        The input text to analyse.

    Returns
    -------
    List[dict]
        A list of dictionaries for each sentence containing:
        * 'sentence': the original sentence
        * 'label': the predicted risk score (0–3)
        * 'categories': list of trigger categories detected
    """
    sentences = _split_sentences(text)
    results: List[Dict[str, object]] = []
    if not sentences:
        return results
    X_vec = _VECTORIZER.transform(sentences)
    labels = _MODEL.predict(X_vec)
    for sent, lbl in zip(sentences, labels):
        categories = _detect_categories(sent)
        results.append({'sentence': sent, 'label': int(lbl), 'categories': categories})
    return results


def suggest_rewrite(sentence: str) -> str:
    """Return a neutral rewrite of a sentence by replacing anxiety-inducing words."""
    rewritten = sentence
    for word, repl in _REPLACEMENTS.items():
        rewritten = re.sub(r'\b' + re.escape(word) + r'\b', repl, rewritten, flags=re.IGNORECASE)
    return rewritten


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = input('Enter text to analyse:\n')
    for res in predict_nocebo_risk(text):
        print(f"Sentence: {res['sentence']}\n  Risk label: {res['label']}\n  Categories: {', '.join(res['categories'])}\n  Suggestion: {suggest_rewrite(res['sentence'])}\n")
