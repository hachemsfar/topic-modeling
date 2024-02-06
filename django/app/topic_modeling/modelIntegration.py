import pickle
from sentence_transformers import SentenceTransformer
from umap import UMAP
from bertopic import BERTopic
import os 

# Load the pre-trained embedding model
embedding_model = SentenceTransformer("BAAI/bge-small-en")

file_path = os.path.join('topic_modeling','model_files', 'reduced_embeddings.pickle')

# Load the pre-reduced embeddings
with open(file_path, 'rb') as handle:
    reduced_embeddings = pickle.load(handle)

file_path = os.path.join('topic_modeling','model_files', 'final')
# Load the model
loaded_topic_model = BERTopic.load(file_path, embedding_model="BAAI/bge-small-en")

def predict_topic(new_abstracts):
    new_embeddings = embedding_model.encode([new_abstracts], show_progress_bar=True)

    reduced_embeddings_new = UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine', random_state=42).fit_transform(new_embeddings)

    new_topics, new_probs = loaded_topic_model.transform([new_abstracts], new_embeddings)

    topic_info = loaded_topic_model.get_topic_info()
    
    return new_topics, new_probs, topic_info