from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

print("Loading BERT model...")
import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_bert_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

bert_model = load_bert_model()
print("BERT model loaded.")


def get_tfidf_vectors(text1: str, text2: str):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1
    )
    matrix  = vectorizer.fit_transform([text1, text2])
    return matrix[0], matrix[1]


def get_bert_embedding(text: str) -> np.ndarray:
    truncated = " ".join(text.split()[:512])
    return bert_model.encode(truncated, convert_to_numpy=True)


def get_tfidf_similarity(text1: str, text2: str) -> float:
    vec1, vec2 = get_tfidf_vectors(text1, text2)
    score      = cosine_similarity(vec1, vec2)[0][0]
    return round(float(score), 4)


def get_bert_similarity(text1: str, text2: str) -> float:
    emb1  = get_bert_embedding(text1).reshape(1, -1)
    emb2  = get_bert_embedding(text2).reshape(1, -1)
    score = cosine_similarity(emb1, emb2)[0][0]
    return round(float(score), 4)


def get_combined_score(text1: str, text2: str) -> dict:
    tfidf_score = get_tfidf_similarity(text1, text2)
    bert_score  = get_bert_similarity(text1, text2)
    combined    = round((0.4 * tfidf_score) + (0.6 * bert_score), 4)
    return {
        "tfidf_score"   : tfidf_score,
        "bert_score"    : bert_score,
        "combined_score": combined
    }


if __name__ == "__main__":
    r = """Experienced Python developer with machine learning and data science skills.
    Proficient in TensorFlow, scikit-learn, and SQL. Worked at Google."""

    j = """Looking for a Python developer with machine learning experience.
    Should know TensorFlow, deep learning, and data analysis."""

    result = get_combined_score(r, j)
    print(f"TF-IDF Score   : {result['tfidf_score']}")
    print(f"BERT Score     : {result['bert_score']}")
    print(f"Combined Score : {result['combined_score']}")