# UC_Davis_ML_Bikes

Project for ECS171 where we predict the average number of bikes that are being rented given the weather utilizing the Seoul Bike Dataset.

This GitHub Repository has 4 major areas:
1. EDA.ipynb: All of the data analysis performed on our data
2. Preparing_Data.ipynb: All of our outlier removal and standardization to created ProcessedData.csv
3. Final_Model_results.ipynb: All of our model training and evaluation
4. flask_ml_gui: Our frontend website using final Random Forest Model with Flask

To run the frontend website:
1. Make sure you are in the `flask_ml_gui` folder
2. Run `python3 -m venv .venv` to create a virtual environment
3. Run `source .venv/bin/activate` to activate the virtual environment
4. Run `pip install -r requirement.txt` to install all the packages needed
5. Run `python3 app.py` to launch the application