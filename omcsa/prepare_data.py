import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the IMDB dataset
data = pd.read_csv('omcsa/IMDB Dataset.csv')

# Preprocess the data
X = data['review'].values
y = data['sentiment'].values

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the preprocessed data
with open('train_data.pkl', 'wb') as f:
    pickle.dump((X_train, y_train), f)
with open('test_data.pkl', 'wb') as f:
    pickle.dump((X_test, y_test), f)