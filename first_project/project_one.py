import pandas as pd
import logging
import os
import pipline
import plotting
import app
import numpy as np

def main():
    # Initialize the data processor with configuration file
    data_processor = pipline.DataProcessor('config.yaml')

    # Create a directory for images if it does not exist
    img_dir = 'img'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    # Load the CSV file based on configuration settings
    csv_file = data_processor.config['csv_config']['file_path']
    skip_col = data_processor.config['csv_config']['index_col']
    df = pd.read_csv(csv_file, index_col=skip_col)
    logging.info(f"Data is loaded successfully")

    # Filter the dataframe for a specific suburb and reset the index
    Glenroy = df[df['Suburb'] == 'Glenroy'].reset_index(drop=True)

    # Rename columns as specified in the configuration
    renaming = data_processor.config['csv_config']['rename_col']
    Glenroy = Glenroy.rename(columns=renaming)

    # Mapping property type abbreviations to full names
    type_mapping = {
        'h': 'House',
        'u': 'Unit',
        't': 'Townhouse'
    }
    Glenroy['property_type'] = Glenroy['property_type'].map(type_mapping)
    glenroy_nnull = Glenroy.dropna().reset_index(drop=True)
    logging.info('created data frame without null values')

    # Define columns to convert to integer and object data types
    to_int = ['number_of_bedrooms', 'number_of_bathrooms', 'number_of_car_spaces']
    to_object = ['total_rooms', 'number_of_bedrooms', 'number_of_bathrooms', 'number_of_car_spaces']

    # Convert data types of specified columns
    data_processor.convert_data_types(glenroy_nnull, to_int, to_object)
    logging.info(f'The type has been converted')

    # Identify numerical columns for plotting histograms
    numerical_columns = ['total_rooms', 'sale_price', 'distance_from_city_center', 'number_of_bedrooms', 'number_of_bathrooms', 'number_of_car_spaces', 
                         'land_size', 'building_area', 'year_built']
    plotter = plotting.DataPlotter(glenroy_nnull)
    plotter.plot_numerical_columns(numerical_columns, "numerical_columns_histograms.png")

    # Define and plot categorical features
    categorical_features = ['total_rooms', 'property_type', 'sale_method', 'number_of_bedrooms', 'number_of_bathrooms', 'number_of_car_spaces']
    df_categorical = glenroy_nnull[categorical_features]

    categorical_columns = ['property_type', 'sale_method', 'seller_agency', 'region_name', 'council_area']
    plotter = plotting.DataPlotter(glenroy_nnull)
    plotter.plot_categorical_columns(categorical_columns, "categorical_columns_bar_plots.png")

    # Plot numerical features against a target column
    numerical_columns = numerical_columns[1:]
    target_column = 'total_rooms'
    plotter = plotting.DataPlotter(glenroy_nnull)
    plotter.plot_num_features_against_target(numerical_columns, target_column, "numerical_features_vs_total_rooms.png")

    # Plot categorical features against the target variable 'total_rooms'
    categorical_columns = ['property_type', 'sale_method', 'seller_agency', 'region_name', 'council_area']
    target_column = 'total_rooms'
    plotter = plotting.DataPlotter(glenroy_nnull)
    plotter.plot_categorical_vs_target(categorical_columns, target_column, "categorical_features_vs_total_rooms.png")

    # Define relevant columns for model training
    relevant_columns = ['total_rooms', 'property_type', 'sale_price', 'sale_method', 'seller_agency', 'number_of_bedrooms']
    target_column = 'number_of_bedrooms'
    categorical_columns = ['property_type', 'sale_method', 'seller_agency']

    data = glenroy_nnull[relevant_columns]

    # Create and train a decision tree model
    model_trainer = app.ModelTrainer(dataframe=data, 
                                    target_column='number_of_bedrooms', 
                                    categorical_columns=categorical_columns)
    model_trainer.train_decision_tree()

    # Evaluate the model performance
    accuracy, report = model_trainer.evaluate_model()
    print("Accuracy:", accuracy)
    print("Classification Report:\n", report)

    # Optional: Plotting the confusion matrix and classification report
    # unique_labels = np.unique(model_trainer.y_test)
    # class_names = [str(label) for label in unique_labels]
    # plotter = plotting.DataPlotter(None)  # No need for DataFrame here
    # plotter.plot_confusion_matrix_and_report(model_trainer.y_test, model_trainer.dt_classifier.predict(model_trainer.X_test), class_names, "confusion_matrix_and_report.png")

if __name__ == "__main__":
    main()

