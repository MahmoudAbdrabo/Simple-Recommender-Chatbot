import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:
    def __init__(self, csv_path, import_features):
        self.df = pd.read_csv(csv_path)
        self.import_features = import_features
        self.titles = self.df['title'].tolist()
        self.df.fillna('', inplace=True)

        # Merge selected columns into one text for each book.
        self.df['combined_features'] = self.df[import_features].astype(str).agg(' '.join, axis=1)

        # Converting Text to Numeric Representation Using TF-IDF
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.feature_matrix = self.vectorizer.fit_transform(self.df['combined_features'])

        # Calculating the similarity between each book and another
        self.similarity = cosine_similarity(self.feature_matrix)

    def recommend(self, fav_book, top_n=5):
        matches = difflib.get_close_matches(fav_book, self.titles)
        if not matches:
            return [" i did not find a similar book with this name 😑😑"]

        best_match = matches[0]
        index = self.df[self.df.title == best_match].index[0]

        similarity_scores = list(enumerate(self.similarity[index]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        recommended = []
        for book_index, _ in sorted_scores:
            if book_index == index:
                continue
            title = self.df.iloc[book_index]['title']
            recommended.append(title)
            if len(recommended) >= top_n:
                break

        return recommended
    def get_author(self, book_title):
        matches = difflib.get_close_matches(book_title, self.titles)
        if matches:
            match = matches[0]
            author = self.df[self.df.title == match]['authors'].values[0]
            return f"✍️ The author of the book is: {author}"
        return "Sorry, I couldn't find this book to find the author"

    def get_bestsellers(self, top_n=10):
        self.df['average_rating'] = pd.to_numeric(self.df['average_rating'], errors='coerce')
        self.df = self.df.dropna(subset=['average_rating'])

        # Sort by Rating
        top_books = self.df.sort_values(by='average_rating', ascending=False).head(top_n)

        # Create a text list in the format  Book Title —  4.7
        book_list = [
            f"📘 {row['title']} — ⭐ {row['average_rating']:.1f}"
            for _, row in top_books.iterrows()
        ]

        return book_list





    def get_publish_year(self, book_title):
        matches = difflib.get_close_matches(book_title, self.titles)
        if matches:
            match = matches[0]
            year = self.df[self.df.title == match]['published_year'].values[0]
            return f"📅 The book was published in the year {year}"
        return "Sorry, I could not find this book to find the year of publication."