import json
import random
import re

import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD TRAINING DATA
# ============================================================

with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)


patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])


# ============================================================
# NLP PREPROCESSING
# ============================================================

stemmer = PorterStemmer()


def preprocess_text(text):
    tokens = nltk.wordpunct_tokenize(text.lower())

    processed_tokens = []

    for token in tokens:
        if re.match(r"^[a-zA-Z]+$", token):
            processed_tokens.append(stemmer.stem(token))

    return processed_tokens


# ============================================================
# FEATURE EXTRACTION
# ============================================================

# Word-level TF-IDF
word_vectorizer = TfidfVectorizer(
    tokenizer=preprocess_text,
    token_pattern=None,
    lowercase=False,
    ngram_range=(1, 2),
    sublinear_tf=True
)


# Character-level TF-IDF
# Helps the chatbot recognize variations in wording.
char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    sublinear_tf=True
)


# Combine word and character features
vectorizer = FeatureUnion([
    ("word_features", word_vectorizer),
    ("character_features", char_vectorizer)
])


# Convert training sentences into numerical vectors
X = vectorizer.fit_transform(patterns)


# ============================================================
# TRAIN MACHINE LEARNING MODEL
# ============================================================

model = LogisticRegression(
    C=2.0,
    max_iter=2000,
    random_state=42
)

model.fit(X, tags)


# ============================================================
# FIND RESPONSE FOR INTENT
# ============================================================

def find_response(predicted_tag):

    for intent in data["intents"]:

        if intent["tag"] == predicted_tag:

            return random.choice(intent["responses"])

    return "Sorry, I could not understand your request."


# ============================================================
# CHATBOT RESPONSE FUNCTION
# ============================================================

def get_response(user_message):

    user_message = user_message.strip()

    # Handle empty messages
    if not user_message:

        return {
            "intent": "unknown",
            "confidence": 0.0,
            "response": "Please enter a message so I can help you."
        }


    # Convert user message into features
    user_vector = vectorizer.transform([user_message])


    # --------------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # --------------------------------------------------------

    probabilities = model.predict_proba(user_vector)[0]

    best_model_index = probabilities.argmax()

    model_confidence = float(
        probabilities[best_model_index]
    )

    model_tag = model.classes_[best_model_index]


    # --------------------------------------------------------
    # SIMILARITY MATCHING
    # --------------------------------------------------------

    similarities = cosine_similarity(
        user_vector,
        X
    )[0]

    best_match_index = similarities.argmax()

    similarity_score = float(
        similarities[best_match_index]
    )

    similarity_tag = tags[best_match_index]


    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    # Very strong similarity means the user's message
    # closely matches a known training example.
    if similarity_score >= 0.72:

        predicted_tag = similarity_tag
        confidence = similarity_score


    # Moderate similarity can rescue cases where the
    # machine-learning probability is too low.
    elif similarity_score >= 0.45 and model_confidence < 0.50:

        predicted_tag = similarity_tag
        confidence = similarity_score


    # Strong machine-learning prediction
    elif model_confidence >= 0.50:

        predicted_tag = model_tag
        confidence = model_confidence


    # Otherwise classify as unknown
    else:

        return {
            "intent": "unknown",
            "confidence": round(
                max(model_confidence, similarity_score),
                2
            ),
           
"response": (
    "I'm sorry, I don't fully understand that. "
    "You can ask me about email assistance, "
    "study help, or task planning."
)

        }


    # --------------------------------------------------------
    # GENERATE RESPONSE
    # --------------------------------------------------------

    response = find_response(predicted_tag)


    return {
        "intent": predicted_tag,
        "confidence": round(float(confidence), 2),
        "response": response
    }


# ============================================================
# TERMINAL CHATBOT
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("        AI CHATBOT - NLP INTENT CLASSIFIER")
    print("=" * 55)

    print("NLP Model: TF-IDF + Logistic Regression")
    print("Matching: Word + Character Similarity")
    print("Type 'exit' to stop the chatbot.")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower().strip() == "exit":

            print("Bot: Goodbye!")
            break


        result = get_response(user_input)


        print("Bot:", result["response"])

        print(
            f"Intent: {result['intent']} | "
            f"Confidence: {result['confidence']}"
        )

        print()
