import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.base import BaseEstimator, TransformerMixin

# Sample data (replace with your actual data)
# Assume 'X' is the feature matrix (FaceNet embeddings) and 'y_age', 'y_gender' are labels
X = np.random.rand(100000, 128)  # 128 is the size of FaceNet embeddings
y_age = np.random.choice(['18-25', '26-35', '36-50', '51-100'], size=(100000,))
y_gender = np.random.choice(['Male', 'Female'], size=(100000,))

# Define a custom transformer to extract age group from labels
class AgeGroupExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([int(label.split('-')[0]) for label in X]).reshape(-1, 1)

# Encode categorical labels
le_age = LabelEncoder()
le_gender = LabelEncoder()

y_age_encoded = le_age.fit_transform(y_age)
y_gender_encoded = le_gender.fit_transform(y_gender)

# Split the data into training and testing sets
X_train, X_test, y_age_train, y_age_test, y_gender_train, y_gender_test = train_test_split(
    X, y_age_encoded, y_gender_encoded, test_size=0.2, random_state=42
)

# Define a preprocessing pipeline for both age and gender
preprocessor = ColumnTransformer(
    transformers=[
        ('age', AgeGroupExtractor(), ['y_age']),
        ('passthrough', 'passthrough', list(range(128))),  # Assuming 128 features
    ],
    remainder='drop'
)

# Define a RandomForestClassifier pipeline for both age and gender
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=500, max_depth=20, random_state=42)),
])

# Train the pipeline
pipeline.fit(X_train, y_gender_train)

# Predictions
y_pred = pipeline.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_gender_test, y_pred)

# Print results
print(f"Gender Classification Accuracy: {accuracy * 100:.2f}%")

# Calculate similarity for each combination of gender and age groups
for gender in le_gender.classes_:
    for age_group in le_age.classes_:
        # Filter data for the specific gender and age group
        mask = (y_gender == le_gender.transform([gender])[0]) & (y_age == age_group)
        X_subset = X[mask]
        
        # Predict on the subset
        y_subset_pred = pipeline.predict(X_subset)
        
        # Calculate accuracy on the subset
        subset_accuracy = accuracy_score(y_gender_encoded[mask], y_subset_pred)
        
        print(f"Similarity for {gender} and Age Group {age_group}: {subset_accuracy * 100:.2f}%")

# this a demonstration Algorithm for similar use.
