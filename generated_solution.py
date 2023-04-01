from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
import json

# Load dataset
data = load_breast_cancer(as_frame=True)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.25, random_state=42, shuffle=True)

# Create logistic regression model
model = LogisticRegression(max_iter=50000)
model.fit(X_train, y_train)

# Make predictions and calculate accuracy score
y_pred = model.predict(X_test)
accuracy = model.score(X_test, y_test)

# Generate classification report
report = classification_report(y_test, y_pred, target_names=data.target_names, output_dict=True, zero_division=1)

# Create JSON dict with metrics
metrics = {"Accuracy": accuracy, "Classification Report": report}

# Print JSON dict
print(json.dumps(metrics, indent=4))
