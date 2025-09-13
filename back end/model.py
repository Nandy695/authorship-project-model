import hashlib
import time
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Blockchain Implementation
# -------------------------------
class Block:
    def __init__(self, index, timestamp, manuscript_hash, ai_score, authorship, plagiarism, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.manuscript_hash = manuscript_hash
        self.ai_score = ai_score
        self.authorship = authorship
        self.plagiarism = plagiarism
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.manuscript_hash}{self.ai_score}{self.authorship}{self.plagiarism}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis", 0, "N/A", "N/A", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, manuscript_hash, ai_score, authorship, plagiarism):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), manuscript_hash, ai_score, authorship, plagiarism, latest_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# -------------------------------
# AI Content Detection (Simulated)
# -------------------------------
def detect_ai_content(text):
    """
    Simulate AI content detection.
    Later you can integrate a real NLP model or API.
    """
    ai_percentage = random.randint(0, 100)

    if ai_percentage < 20:
        authorship = "Human-written"
    elif 20 <= ai_percentage <= 50:
        authorship = "Half written by AI"
    else:
        authorship = "AI-generated"

    return ai_percentage, authorship

# -------------------------------
# Plagiarism Detection
# -------------------------------
def check_plagiarism(text, folder="manuscripts"):
    """
    Compare input text against stored manuscripts in a folder.
    Uses TF-IDF + Cosine Similarity.
    """
    if not os.path.exists(folder):
        return "No Manuscripts Found"

    documents = []
    file_names = []

    # Load all manuscript files
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                documents.append(f.read())
                file_names.append(file)

    if not documents:
        return "No Manuscripts Found"

    # Add user text to the comparison set
    documents.append(text)

    # Vectorize
    vectorizer = TfidfVectorizer().fit_transform(documents)
    similarity_matrix = cosine_similarity(vectorizer[-1], vectorizer[:-1])

    max_similarity = similarity_matrix.max()

    if max_similarity > 0.7:  # threshold
        return f"Plagiarism Detected (similarity: {max_similarity:.2f})"
    else:
        return "No Plagiarism"

# -------------------------------
# Main Program
# -------------------------------
if __name__ == "__main__":
    blockchain = Blockchain()

    # Get manuscript input (later connect to frontend)
    manuscript = input("Enter your manuscript content:\n")

    # Timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Manuscript Hash
    manuscript_hash = hashlib.sha256(manuscript.encode()).hexdigest()

    # AI Detection
    ai_score, authorship = detect_ai_content(manuscript)

    # Plagiarism Detection
    plagiarism_result = check_plagiarism(manuscript)

    # Add to Blockchain
    blockchain.add_block(manuscript_hash, ai_score, authorship, plagiarism_result)

    # Show Results
    print("\n--- Analysis Results ---")
    print(f"Timestamp: {timestamp}")
    print(f"AI Content Score: {ai_score}%")
    print(f"Authorship: {authorship}")
    print(f"Plagiarism: {plagiarism_result}")
    print("\n--- Blockchain Ledger ---")
    for block in blockchain.chain:
        print(vars(block))
