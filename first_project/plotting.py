import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import numpy as np

class DataPlotter:
    def __init__(self, dataframe, img_dir='img'):
        """
        Initializes the DataPlotter with a DataFrame.

        Parameters:
        dataframe (pd.DataFrame): The DataFrame to plot data from.
        img_dir (str): Directory to save plots.
        """
        self.dataframe = dataframe
        self.img_dir = img_dir
        # Create the directory if it doesn't exist
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

    def plot_numerical_columns(self, numerical_columns, save_filename):
        """
        Creates and saves histograms for specified numerical columns in the DataFrame.

        Parameters:
        numerical_columns (list): A list of column names to be plotted.
        save_filename (str): Filename for the saved plot.
        """
        sns.set(style="whitegrid")
        plt.figure(figsize=(15, 10))

        for i, column in enumerate(numerical_columns, 1):
            plt.subplot(3, 3, i)
            sns.histplot(self.dataframe[column], kde=True)
            plt.title(column)

        plt.tight_layout()

        # Save the plot in the specified directory
        save_path = os.path.join(self.img_dir, save_filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to free up memory

    def plot_categorical_columns(self, categorical_columns, save_filename):
        """
        Creates and saves bar plots for specified categorical columns in the DataFrame.

        Parameters:
        categorical_columns (list): A list of column names to be plotted.
        save_filename (str): Filename for the saved plot.
        """
        plt.figure(figsize=(15, 10))

        for i, column in enumerate(categorical_columns, 1):
            plt.subplot(3, 2, i)
            sns.countplot(y=column, data=self.dataframe, order=self.dataframe[column].value_counts().index)
            plt.title(column)

        plt.tight_layout()

        # Save the plot in the specified directory
        save_path = os.path.join(self.img_dir, save_filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to free up memory

    def plot_num_features_against_target(self, numerical_columns, target_column, save_filename):
        """
        Creates and saves bar plots and KDE plots for specified numerical columns against a target column.
        """
        fig, axes = plt.subplots(nrows=len(numerical_columns), ncols=2, figsize=(15, 5 * len(numerical_columns)))
        axes = axes.flatten()

        for i, column in enumerate(numerical_columns):
            # Bar plot
            sns.barplot(x=target_column, y=column, data=self.dataframe, ax=axes[i*2], errorbar=None)
            axes[i*2].set_title(f'Mean {column} per {target_column}')

            # KDE plot
            for value in self.dataframe[target_column].unique():
                subset = self.dataframe[self.dataframe[target_column] == value][column]
                # Check for variance before plotting
                if np.var(subset) != 0:
                    sns.kdeplot(subset, ax=axes[i*2+1], label=f'{value} {target_column}')
                else:
                    # Optionally, display a message or handle the 0 variance case differently
                    print(f"No variance in data for {column} with {value} {target_column}")
            axes[i*2+1].set_title(f'Distribution of {column} by {target_column}')
            axes[i*2+1].legend()

        plt.tight_layout()

        # Save the plot in the specified directory
        save_path = os.path.join(self.img_dir, save_filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to free up memory

    def plot_categorical_vs_target(self, categorical_columns, target_column, save_filename):
        """
        Creates and saves 100% stacked bar plots for specified categorical columns against a target column.

        Parameters:
        categorical_columns (list): A list of categorical column names to be plotted against the target.
        target_column (str): The target column name for comparison.
        save_filename (str): Filename for the saved plot.
        """
        fig, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=(10, 20))
        axes = axes.flatten()

        for i, column in enumerate(categorical_columns):
            # Creating a crosstab for percentage calculation
            crosstab = pd.crosstab(self.dataframe[column], self.dataframe[target_column], normalize='index') * 100
            crosstab.plot(kind='bar', stacked=True, ax=axes[i])
            axes[i].set_title(f'{column} vs {target_column}')
            axes[i].legend(title=target_column, bbox_to_anchor=(1.05, 1), loc='upper left')
            axes[i].set_ylabel('% Distribution')

        plt.tight_layout()

        # Save the plot in the specified directory
        save_path = os.path.join(self.img_dir, save_filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to free up memory

    def plot_confusion_matrix_and_report(self, y_true, y_pred, classes, save_filename='train'):
        """
        Plots the confusion matrix and shows the classification report.

        Parameters:
        y_true (array): True labels.
        y_pred (array): Predicted labels.
        classes (list): List of class names.
        save_filename (str): Filename for the saved plot.
        """
        cm = confusion_matrix(y_true, y_pred, labels=np.arange(len(classes)))
        report = classification_report(y_true, y_pred, target_names=classes, output_dict=True)

        fig, ax = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={'width_ratios': [2, 3]})
        
        # Plot confusion matrix
        sns.heatmap(cm, annot=True, ax=ax[0], fmt='g')
        ax[0].set_title('Confusion Matrix')
        ax[0].set_xlabel('Predicted labels')
        ax[0].set_ylabel('True labels')
        ax[0].set_xticklabels(classes)
        ax[0].set_yticklabels(classes)

        # Create DataFrame from the classification report
        report_df = pd.DataFrame(report).transpose()

        # Adjust the number of x-tick labels to match the number of columns in report_df
        ax[1].set_xticklabels(report_df.columns, rotation=45)

        # Adjust the number of y-tick labels to match the number of rows, excluding summary rows
        num_rows = len(report_df.index) - 3  # Exclude 'accuracy', 'macro avg', 'weighted avg'
        ax[1].set_yticklabels(report_df.index[:num_rows])

        plt.tight_layout()

        # Save the plot in the specified directory
        save_path = os.path.join(self.img_dir, save_filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to free up memory