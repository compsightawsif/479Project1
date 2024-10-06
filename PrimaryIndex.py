import os

from collections import defaultdict

from PreprocessingPipeline import PreprocessingPipeline


class SPIMIIndexer:
    def __init__(self, token_stream, doc_ids):
        self.token_stream = token_stream
        self.doc_ids = doc_ids
        self.dictionary = defaultdict(list)  # Dictionary to store the inverted index

    def spimi_invert(self):
        """Perform SPIMI-inspired inversion to build an inverted index."""
        for doc_id, token in zip(self.doc_ids, self.token_stream):
            # If the token is not in the dictionary, add it
            if token not in self.dictionary:
                self.dictionary[token] = []

            # Add the docID to the token's postings list if it's not already there
            if doc_id not in self.dictionary[token]:
                self.dictionary[token].append(doc_id)

    def write_to_primary_index(self, filename="PrimaryIndex.txt"):
        """Write the inverted index to a file."""
        sorted_terms = sorted(self.dictionary.keys())  # Sort the terms alphabetically

        with open(filename, 'w') as f:
            for term in sorted_terms:
                postings_list = ', '.join(map(str, self.dictionary[term]))
                f.write(f"{term}: {postings_list}\n")

        print(f"Inverted index written to {filename}")

    def get_inverted_index(self):
        """Return the inverted index (dictionary)."""
        return self.dictionary


# Example usage
if __name__ == "__main__":
    # Assuming you already have the token_stream and doc_ids from PreprocessingPipeline
    pipeline = PreprocessingPipeline('reuters21578/')
    pipeline.extract_articles()

    token_stream = pipeline.get_token_stream()
    doc_ids = pipeline.get_doc_ids()

    # Initialize and run the SPIMI indexer
    indexer = SPIMIIndexer(token_stream, doc_ids)
    indexer.spimi_invert()

    # Write the inverted index to PrimaryIndex.txt
    indexer.write_to_primary_index()
