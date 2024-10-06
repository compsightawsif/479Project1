import os
from bs4 import BeautifulSoup
import re
# import nltk
from nltk.tokenize import word_tokenize

# nltk.download('punkt')

class PreprocessingPipeline:
    def __init__(self, corpus_directory):
        self.corpus_directory = corpus_directory
        self.total_articles = 0
        self.headlines = []
        self.bodies = []
        self.token_stream = []
        self.doc_ids = []

    def extract_articles(self):
        for filename in os.listdir(self.corpus_directory):
            if filename.endswith('.sgm'):
                filepath = os.path.join(self.corpus_directory, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    sgm_data = f.read()

                soup = BeautifulSoup(sgm_data, 'html.parser')

                articles = soup.find_all('reuters')
                self.total_articles += len(articles)

                for article in articles:
                    self._extract_doc_id(article)
                    self._extract_text(article)

    def _extract_doc_id(self, article):
        new_id = article.get('newid')
        if new_id:
            self.doc_ids.append(new_id)

    def _normalize_text(self, text):
        # Convert text to lowercase and remove non-alphanumeric characters
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        return text

    def _extract_text(self, article):
        headline = article.find('title')
        body = article.find('body') or article.find('text') or article.find('content')

        if headline:
            headline_text = self._normalize_text(headline.get_text())
            self.headlines.append(headline_text)
            self.token_stream.extend(word_tokenize(headline_text))

        if body:
            body_text = self._normalize_text(body.get_text())
            self.bodies.append(body_text)
            self.token_stream.extend(word_tokenize(body_text))


    def get_token_stream(self):
        return self.token_stream

    def get_doc_ids(self):
        return self.doc_ids

# Example usage:
if __name__ == "__main__":
    # Initialize the pipeline with the corpus directory path
    corpus_directory = 'reuters21578/'  # Update this to your path
    pipeline = PreprocessingPipeline(corpus_directory)

    # Extract articles and tokenize
    pipeline.extract_articles()

    # Token streams are now available for further processing
    token_stream = pipeline.get_token_stream()
