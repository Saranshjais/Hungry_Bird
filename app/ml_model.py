import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_recommendation_model(vendors):
    df = pd.DataFrame(vendors)

    df["features"] = df["cuisine_type"].fillna('') + " " + df["description"].fillna('')

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df["features"])

    similarity = cosine_similarity(tfidf_matrix)

    return df, similarity


def get_recommendations(vendor_name, df, similarity):
    if vendor_name not in df["name"].values:
        return []

    idx = df[df["name"] == vendor_name].index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []
    for i in scores[1:6]:
        results.append(df.iloc[i[0]].to_dict())

    return results