import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from tasks import tasks
task=tasks()

# load the vectorizer and classifier from disk
vectorizer = joblib.load('vectorizer.joblib')
clf = joblib.load('clf.joblib')

def process_query(query):
    # vectorize the query using the loaded vectorizer
    X_query = vectorizer.transform([query])

    # predict the intent using the loaded classifier
    intent = clf.predict(X_query)[0]

    # call the appropriate function based on the predicted intent
    if intent == 'open_website':
        task.openWebsite(query)
    elif intent == 'open_youtube':
        task.youtubeSearch(query)
    elif intent == 'play_music':
        task.play_song(query)
    elif intent == 'get_date':
        task.speakDateTime()
