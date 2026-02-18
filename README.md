Enron Email Spam Detection App

A web application that classifies emails as spam or ham, built using the Enron email dataset. The app demonstrates a full pipeline: data preprocessing, model training, and live deployment with Docker.

🔹 Live Demo

  Try the frontend live here:
  https://enron-spam-frontend-1-0-0.onrender.com

  Enter the email subject, message, and date

  Click Classify Email to see if it’s spam or ham

🔹 Dataset

  Original dataset: https://github.com/MWiechmann/enron_spam_data

  License: GPL-3.0

  This project uses a processed JSON version built from the original dataset for easier handling and faster model training

  Both the original CSV and the converted JSON are included in the Docker image and container under the data folder

  Project license: GPL-3.0

🔹 Model Training

  Model trained in eda.ipynb using the original CSV dataset

  Includes feature engineering, exploratory data analysis (EDA), and training of the classification model

  Trained model is saved and used by the backend API for real-time predictions

  Roughly 88% of the project code is in this notebook

  ML Model Accuracy: 96%

🔹 Backend & Frontend
  Backend: FastAPI serving predictions at /predict

  Frontend: Streamlit UI for classifying emails easily

  Dockerized for consistent deployment

  Deployed on Render for public access

🔹 Key Features

  Preprocessed JSON dataset from Enron emails

  Trained ML model integrated into backend API

  Live demo via Streamlit frontend

  Easy local testing using Docker Compose
