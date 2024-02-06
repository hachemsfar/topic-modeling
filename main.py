import streamlit as st
import pickle
from sentence_transformers import SentenceTransformer
from umap import UMAP
from bertopic import BERTopic

# Load the pre-trained embedding model
embedding_model = SentenceTransformer("BAAI/bge-small-en")

# Load the pre-reduced embeddings
with open('reduced_embeddings.pickle', 'rb') as handle:
    reduced_embeddings = pickle.load(handle)

# Load the model
loaded_topic_model = BERTopic.load("final", embedding_model="BAAI/bge-small-en")

def main():
    st.title("Topic Modeling Dashboard")

    # User input for a single block of text
    new_abstracts = st.text_area("Enter a single block of text:", "")

    if new_abstracts:
        # Encode the single block of text
        new_embeddings = embedding_model.encode([new_abstracts], show_progress_bar=True)

        # Visualize using UMAP
        reduced_embeddings_new = UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine', random_state=42).fit_transform(new_embeddings)

        # Transform the single block of text using the loaded topic model
        new_topics, new_probs = loaded_topic_model.transform([new_abstracts], new_embeddings)

        st.write("New Topics:", new_topics)
        st.write("Topic Probabilities:", new_probs)

if __name__ == "__main__":
    main()
