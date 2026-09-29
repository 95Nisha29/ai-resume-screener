"""TF-IDF and Cosine Similarity scoring engine."""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.nlp import clean_text, STOPWORDS


class SimilarityEngine:
    """Computes TF-IDF vectorization and Cosine Similarity between resumes and job descriptions."""

    def __init__(self, min_df: int = 1, ngram_range: Tuple[int, int] = (1, 2)):
        self.ngram_range = ngram_range
        self.min_df = min_df

    def compute_similarities(
        self,
        job_description: str,
        resumes: List[str]
    ) -> List[float]:
        """
        Compute cosine similarity of each resume against the job description.
        
        Returns:
            List[float]: similarity score in range [0.0, 1.0] for each resume.
        """
        if not resumes:
            return []

        cleaned_jd = clean_text(job_description)
        cleaned_resumes = [clean_text(r) for r in resumes]

        # Corpus is JD + all resumes
        corpus = [cleaned_jd] + cleaned_resumes

        # Check if all texts are empty
        if not any(doc.strip() for doc in corpus):
            return [0.0] * len(resumes)

        # Convert custom STOPWORDS to list for vectorizer
        stop_words_list = list(STOPWORDS)

        vectorizer = TfidfVectorizer(
            ngram_range=self.ngram_range,
            stop_words=stop_words_list,
            min_df=self.min_df,
            sublinear_tf=True,
            norm="l2"
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            # Fallback if vocabulary is completely empty after stop words
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1),
                sublinear_tf=True,
                norm="l2"
            )
            tfidf_matrix = vectorizer.fit_transform(corpus)

        # First row is Job Description
        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]

        # Compute cosine similarity between JD vector and each resume vector
        cosine_sims = cosine_similarity(resume_vectors, jd_vector).flatten()

        # Clip values to ensure clean bounds [0.0, 1.0]
        return [float(np.clip(score, 0.0, 1.0)) for score in cosine_sims]

    def get_top_keywords(
        self,
        text: str,
        top_n: int = 10
    ) -> List[Tuple[str, float]]:
        """Extract top TF-IDF keywords from a given text."""
        cleaned = clean_text(text)
        if not cleaned:
            return []

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words=list(STOPWORDS),
            sublinear_tf=True
        )

        try:
            tfidf_matrix = vectorizer.fit_transform([cleaned])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            sorted_indices = np.argsort(scores)[::-1][:top_n]
            return [(feature_names[i], float(scores[i])) for i in sorted_indices if scores[i] > 0]
        except Exception:
            return []
