from matplotlib import pyplot as plt
import numpy as np
import pandas as pd  
import os
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download('punkt')

# Load the dataset with proper handling of quoted strings
file_path = 'dataset.csv'
data = pd.read_csv(file_path, on_bad_lines='skip', quotechar='"', delimiter=',')

# Display the first few rows of the dataframe
print(data.head())

# Clean the data if necessary (e.g., remove duplicates, handle missing values)
data.drop_duplicates(inplace=True)
data.dropna(inplace=True)

# Tokenize the text data (assuming the second column contains the text data)
data['tokenized_text'] = data.iloc[:, 1].apply(word_tokenize)

# Vectorize the text data (using the second column for vectorization)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data.iloc[:, 1])

# Prepare the target variable (assuming the third column contains the labels)
y = data.iloc[:, 2]

# Split the dataset into training and testing sets (e.g., 80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the 'data' directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save the training and testing sets to separate CSV files
train_data = pd.DataFrame(X_train.toarray(), columns=vectorizer.get_feature_names_out())
train_data['label'] = y_train.values
train_data.to_csv('data/training_dataset.csv', index=False)

test_data = pd.DataFrame(X_test.toarray(), columns=vectorizer.get_feature_names_out())
test_data['label'] = y_test.values
test_data.to_csv('data/testing_dataset.csv', index=False)

print("Training and testing datasets created successfully.")

# Train the Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=3, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10), random_state=42
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.figure()
plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training score')
plt.plot(train_sizes, test_mean, 'o-', color='g', label='Cross-validation score')

plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='g')

plt.title('Learning Curve')
plt.xlabel('Training Examples')
plt.ylabel('Score')
plt.legend(loc='best')
plt.grid()
plt.show()

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)










##### if lang == 'fr':
            answer = translator_fr.translate(answer)
            st.write("Vous parlez francais")
        elif lang == 'ar':
            answer = translator_ar.translate(answer)
            st.write("This is arabic")
        elif: lang == 'en':
            answer = translator_en.translate(answer)
            st.write("You're speaking English")
            else:
                st.write("Sorry, i only speak  french , arabic , english")