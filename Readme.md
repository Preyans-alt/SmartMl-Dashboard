# AutoML Dataset Analyzer & Model Trainer

A Streamlit-based machine learning web app that allows users to:

* Upload any CSV dataset
* Perform automatic dataset preprocessing
* Select ML models
* Train and evaluate models
* Visualize feature importance, correlations, predictions, and metrics

---

## Features

### Dataset Operations

The app automatically performs:

* **Remove unwanted columns**

  * Drops columns with more than **90% unique values**
  * Useful for removing:

    * IDs
    * Names
    * Unique identifiers

* **Outlier Removal**

  * Uses **IQR (Interquartile Range)** method

* **Missing Value Handling**

  * Numerical columns → filled with **mean**
  * Categorical columns → filled with **mode**

* **One Hot Encoding Support**

  * Converts categorical columns into numeric format

* **Null Value Comparison**

  * Shows null values before and after preprocessing

* **Correlation Heatmap**

  * Displays feature correlation matrix using heatmap

---

## Supported Models

### Regression Models

* Linear Regression
* Ridge Regression
* Lasso Regression
* KNN Regressor

### Classification Models

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier
* Support Vector Classifier (SVC)
* KNN Classifier
* Naive Bayes

---

## Model Evaluation

### Regression Metrics

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* R² Score

### Classification Metrics

* Accuracy Score
* Recall Score
* Confusion Matrix

---

## Visualizations

The app provides:

* Correlation Heatmap
* Actual vs Predicted Graph
* Confusion Matrix
* Feature Importance Graph

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Project Structure

```bash
project/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## How to Use

1. Upload a CSV dataset
2. Select a machine learning model
3. Choose:

   * Target column (Y)
   * Features (X)
4. Select train size
5. Click **Run Model**

The app will automatically:

* Clean dataset
* Train model
* Show predictions
* Display metrics and graphs
