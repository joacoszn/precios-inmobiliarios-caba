
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def crear_features_nlp(df: pd.DataFrame, text_column: str = 'description', vectorizer=None):
    """
    Procesa una columna de texto para crear características TF-IDF.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        text_column (str): Nombre de la columna con el texto.
        vectorizer (TfidfVectorizer, optional): Vectorizer pre-entrenado. 
            Si es None, se creará y entrenará uno nuevo.

    Returns:
        pd.DataFrame: DataFrame con las características TF-IDF.
        TfidfVectorizer: El vectorizer utilizado (nuevo o el proporcionado).
    """
    text_series = df[text_column].str.lower().fillna('')

    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(text_series)
    else:
        tfidf_matrix = vectorizer.transform(text_series)

    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                              columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])], 
                              index=df.index)
    
    return tfidf_df, vectorizer

def guardar_vectorizer(vectorizer, path):
    """Guarda el vectorizer en un archivo pickle."""
    with open(path, 'wb') as f:
        pickle.dump(vectorizer, f)
