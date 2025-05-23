from sentence_transformers import SentenceTransformer, util

class CategoryMatcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def find_best_category(self, candidate: str, categories):
        candidate_embedding = self.model.encode(candidate, convert_to_tensor=True)
        names = [cat['name'] for cat in categories]
        embeddings = self.model.encode(names, convert_to_tensor=True)
        similarities = util.cos_sim(candidate_embedding, embeddings)[0]
        best_idx = similarities.argmax().item()
        best_score = similarities[best_idx].item()
        if best_score >= 0.7:
            return categories[best_idx]['id'], categories[best_idx]['name']
        return None, None
