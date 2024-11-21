import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Project

def recommend_projects(project_id):
    # Fetch all projects from the database
    projects = Project.objects.all()

    # Prepare the data for recommendation
    data = [{
        'id': project.id,
        'title': project.title,
        'description': project.description or '',
        'category': project.category or '',
        'location': project.location or ''
    } for project in projects]

    # Create a DataFrame
    df = pd.DataFrame(data)
    df['combined_features'] = (
        df['title'] + " " +
        df['description'] + " " +
        df['category'] + " " +
        df['location']
    )

    # Create a TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get recommendations
    project_idx = df[df['id'] == project_id].index[0]
    similarity_scores = list(enumerate(cosine_sim[project_idx]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:4]
    recommended_ids = [df.iloc[i[0]]['id'] for i in sorted_scores]

    # Fetch recommended projects from the database
    return Project.objects.filter(id__in=recommended_ids)
