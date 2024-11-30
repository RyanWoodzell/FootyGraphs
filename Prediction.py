import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

class Prediction:
    def __init__(self, data):
        self.data = data
        
    def predict(self):
        # Feature engineering
        self.data['GF/MP'] = self.data['GF'] / self.data['MP']
        self.data['GA/MP'] = self.data['GA'] / self.data['MP']
        self.data['GD/MP'] = self.data['GD'] / self.data['MP']
        self.data['xGD/MP'] = self.data['xGD'] / self.data['MP']
        self.data['Recent_Points'] = self.data['Last 5'].apply(lambda x: x.count('W') * 3 + x.count('D'))

            # Define features and target
        features = ['Pts', 'Pts/MP', 'GD/MP', 'GF/MP', 'GA/MP', 'xGD/MP', 'Recent_Points']
        X = self.data[features]
        y = self.data['Rk']

            
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Train logistic regression model
        log_reg = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42)
        log_reg.fit(X_train, y_train)

        # Make predictions and probabilities
        y_pred = log_reg.predict(X_test)
        y_prob = log_reg.predict_proba(X_test)

        # Evaluate model
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Extract and display the probability of coming in first place for each team
        # We are interested in the probability for rank 1 (first place), which corresponds to the first column (index 0) of the probabilities array
        prob_rank_1 = y_prob[:, 0]  # Probability of coming in 1st place

        # Create a DataFrame to display the team names and their probabilities of finishing in first place
        teams = self.data['Squad'].iloc[X_test.index]  # Get the team names from the test set
        team_probabilities = pd.DataFrame({
            'Team': teams,
            'Probability of Finishing 1st': prob_rank_1
        })

        # Sort by probability in descending order
        team_probabilities = team_probabilities.sort_values(by='Probability of Finishing 1st', ascending=False)

        # Display the results
        print("\nProbability of Finishing in 1st Place for Each Team:")
        print(team_probabilities)