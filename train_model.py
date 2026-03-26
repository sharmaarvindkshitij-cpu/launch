import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Synthetic Dataset for Scam Detection
data = [
    # Scams
    ("Congratulations! You've won a $1000 Walmart gift card. Click here to claim your prize.", 1),
    ("URGENT: Your account has been suspended due to suspicious activity. Verify your identity immediately.", 1),
    ("You have been selected for a high-paying remote job. Please pay a small registration fee to start.", 1),
    ("Dear customer, your KYC is pending. Please click the link to update your PAN card details to avoid account blocking.", 1),
    ("Investment opportunity! Double your money in 24 hours with our guaranteed crypto scheme. Join our telegram group.", 1),
    ("Lottery Winner! Your phone number was selected to win $5,000,000. Send your bank details to transfer the fund.", 1),
    ("Your Netflix subscription has expired. Update your payment information here.", 1),
    ("A login attempt was prevented. If this wasn't you, reset your password at this link.", 1),
    ("This is the IRS. You owe back taxes. We will send the police to arrest you unless you pay immediately via Apple gift cards.", 1),
    ("Hot singles in your area want to chat. Click here now!", 1),
    ("Claim your free iPhone 15 Pro Max today. Only a few left in stock!", 1),
    ("Your Amazon package could not be delivered due to incomplete address. Click the link to pay the $2.00 redelivery fee.", 1),
    ("Bank alert: A transaction of $500 was made. If unauthorized, click here to cancel.", 1),
    ("Earn 10000 rupees a day by just watching videos. Join now!", 1),
    ("I am stranded in London and need $500 for a flight home. Please wire the money.", 1),
    
    # Safe
    ("Hey, are we still meeting for lunch at 1 PM?", 0),
    ("Can you send me the quarterly report by Friday?", 0),
    ("Happy birthday! Hope you have a wonderful day.", 0),
    ("Don't forget to pick up groceries on your way home. We need milk and eggs.", 0),
    ("The project meeting is scheduled for tomorrow at 10 AM in Conference Room B.", 0),
    ("I'll call you back in 10 minutes.", 0),
    ("Did you watch the game last night? What a finish!", 0),
    ("Please find attached the invoice for last month's services.", 0),
    ("Let's grab coffee sometime next week.", 0),
    ("Your appointment with Dr. Smith is confirmed for Thursday at 3 PM.", 0),
    ("Here are the notes from today's lecture.", 0),
    ("I'm running a bit late, be there in 15.", 0),
    ("Could you review this pull request when you have a chance?", 0),
    ("Just checking in to see how you're doing.", 0),
    ("Reminder: Team building event this Friday at 4 PM.", 0)
]

# Create DataFrame
df = pd.DataFrame(data, columns=['text', 'label'])

# Expand dataset slightly to allow reliable train/test split execution
df = pd.concat([df]*10, ignore_index=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Build Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('clf', LogisticRegression(random_state=42))
])

print("Training model...")
pipeline.fit(X_train, y_train)

# Evaluate Model
predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions))

# Save Model Pipeline
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, 'model/scam_model.pkl')
print("Model and vectorizer saved to model/scam_model.pkl.")
