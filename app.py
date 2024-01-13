from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class ModelTrainer:
    def __init__(self, dataframe, target_column, categorical_columns, random_state=42):
        """
        Initializes the ModelTrainer with a DataFrame.

        Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        target_column (str): The name of the target column.
        categorical_columns (list): A list of names of categorical columns.
        random_state (int): Random state for train_test_split.
        """
        self.dataframe = dataframe
        self.target_column = target_column
        self.categorical_columns = categorical_columns
        self.random_state = random_state
        self.label_encoders = {}
        self.X_train, self.X_test, self.y_train, self.y_test = [None] * 4
        self._prepare_data()

    def _encode_categorical_columns(self):
        """Encodes categorical variables in the dataframe."""
        for column in self.categorical_columns:
            le = LabelEncoder()
            self.dataframe[column] = le.fit_transform(self.dataframe[column])
            self.label_encoders[column] = le

    def _prepare_data(self):
        """Prepares the data for modeling."""
        # Encoding categorical variables
        self._encode_categorical_columns()

        # Converting 'number_of_bedrooms' to integer type
        self.dataframe[self.target_column] = self.dataframe[self.target_column].astype(int)

        # Splitting the dataset into features and target variable
        X = self.dataframe.drop(self.target_column, axis=1)
        y = self.dataframe[self.target_column]

        # Splitting the dataset into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=self.random_state)

    def train_decision_tree(self):
        """Trains a Decision Tree classifier."""
        self.dt_classifier = DecisionTreeClassifier(random_state=42)
        self.dt_classifier.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        """Evaluates the trained Decision Tree model."""
        y_pred = self.dt_classifier.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred)
        return accuracy, report


