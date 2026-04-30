import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score,confusion_matrix,ConfusionMatrixDisplay,accuracy_score,recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.inspection import permutation_importance



class DataSetHandel:
    def __init__(self,dataSet):
        self.dataset = dataSet
    
    # to remove column which has more than 90% unique value which indicates col like ID,name which not use full for dataset
    def removeUnique(self):
        drop_col = []
        for i in self.dataset.columns:
            count = self.dataset[i].nunique()
            print((count/150) > 0.9)
            if count/self.dataset.shape[0] >= 0.9 and self.dataset[i].dtype not in ['int64', 'float64']:
                self.dataset.drop(i,axis=1,inplace=True)
                drop_col.append(i)
        return drop_col

    def removeOutliears(self):
        for i in self.dataset.columns:
            if self.dataset[i].dtype in ['int64', 'float64']:
                q1 = self.dataset[i].quantile(0.25)
                q3 = self.dataset[i].quantile(0.75)
                IQR = q3-q1
                low = q1 - 1.5*IQR
                high = q3 + 1.5*IQR
                self.dataset = self.dataset[(self.dataset[i]>=low) & (self.dataset[i]<=high)]
        return self.dataset.shape

    def one_hotEncoding(self,*cols):
        for i in cols:
            self.dataset = pd.get_dummies(self.dataset,columns=i,dtype=int,)
        return self.dataset

    def handelMissingValues(self):
        for col in self.dataset.columns:

            if self.dataset[col].dtype in ['int64', 'float64']:
                mean = self.dataset[col].mean()
                self.dataset[col].fillna(mean, inplace=True)
            else:
                mode_val = self.dataset[col].mode()[0]
                self.dataset[col].fillna(mode_val, inplace=True)

    def finalData(self):
        return self.dataset
        


tab1,tab2 = st.tabs(["Dataset Operantion", "Model"])


st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 450px !important; # Set your desired width here
    }
    </style>
    """,
    unsafe_allow_html=True,
)

data_set = st.sidebar.file_uploader('Uplode DataSet (.csv)')


model_object = {
    # Regression Models
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(),
    'Lasso Regression': Lasso(),
    'KNN Regressor': KNeighborsRegressor(n_neighbors=5),

    # Classification Models
    'Logistic Regression': LogisticRegression(),
    'Decision Tree Classifier': DecisionTreeClassifier(),
    'Random Forest Classifier': RandomForestClassifier(),
    'Support Vector Classifier': SVC(),
    'KNN Classifier': KNeighborsClassifier(),
    'Naive Bayes': GaussianNB(),

}


if data_set:
    with tab1:
        st.subheader('Data Analysis:-')
        data = pd.read_csv(data_set)
        st.dataframe(data)

        null_values_before = data.isnull().sum()
        model = st.sidebar.selectbox(
            "Select Model",
            model_object.keys()
        )

        # dataset operation:----------------------------------
        
        data_opp = DataSetHandel(data)
        
        temp = data_opp.removeUnique()
        if temp:
            st.subheader(f"Remove Unwanted Cols:- {temp}")
            data = data_opp.finalData()
            st.subheader('new DataSet:')
            st.dataframe(data)

        st.subheader(f"DataSet Shape After Removing outliears:- {data_opp.removeOutliears()}")

        data_opp.handelMissingValues()
        data = data_opp.finalData()

        st.subheader('Null Values before/after:-')
        null_values_after = data.isnull().sum()
        # to show null values before and after operations:
        null_data = pd.DataFrame({'Null Values Before':null_values_before,'Null Values After':null_values_after})
        st.write(null_data)

        st.header('Features Correlation')
        corr = data.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            corr,
            annot=True,
            cmap='coolwarm',
            fmt='.5f',
            ax=ax
        )

        st.pyplot(fig)

    with tab2:
        # model operations:---------------------------------------------------------
        col_name = data.columns.to_list()
        

        # input fields for model related selections:-----------------------------------------------
        # to define column to predict
        toPredict = st.sidebar.selectbox(
            'Select Feature To Predict (select Y)', col_name
        )

        if toPredict:
            col_name.pop(col_name.index(toPredict))
        # to define numbers of features to consider

        # to list the only those features which has datatype = int or float 
        remaining_features = [i for i in col_name if data[i].dtype in ['int64', 'float64']]
        features = st.sidebar.multiselect(
            'Select Features to consider (select X)',remaining_features
        )

        train_size = st.sidebar.slider(label='select train dataset size',min_value=0.6,max_value=0.9,value=0.8)

        run_btn = st.sidebar.button('Run Model',use_container_width=True)

        # model working:-----------------------

        if run_btn:
            if toPredict:
                y = data[toPredict]   # cleaner

                if features:
                    x = data[features]   # user-selected features
                else:
                    x = data[remaining_features]


                x_train, x_test, y_train, y_test = train_test_split(
                    x, y, train_size=train_size, random_state=2
                )

                if model:
                    myModel = model_object[model]

                    # to check y data type id object and not classification then show error
                    if y_train.dtype == 'object' and model not in ['Logistic Regression','Decision Tree Classifier','Random Forest Classifier','Support Vector Classifier','KNN Classifier' ,'Naive Bayes']:
                        st.warning('Selected Y is Categorical Use Classification Model!!!')
                    
                    else:
                        try:
                            myModel.fit(x_train,y_train)
                            st.write('Model Prediction:- ')
                            y_pred = myModel.predict(x_test)
                            temp_data = pd.DataFrame({'Actual':y_test,'Predicted':y_pred})
                            st.dataframe(temp_data)
                        except Exception as e:
                            st.write('Error: ',e)

                        # to show error , or accuracy_score score according to model
                        if model in ['Logistic Regression','Decision Tree Classifier','Random Forest Classifier','Support Vector Classifier','KNN Classifier' ,'Naive Bayes']:
                            st.info(f'Accuracy Score: {accuracy_score(y_test,y_pred)}')
                            st.info(f'Recall Score: {recall_score(y_test,y_pred,average='weighted')}')
                            st.info(f'Confusion Matrix:')
                            fig,ax = plt.subplots()
                            ConfusionMatrixDisplay.from_predictions(y_test,y_pred,ax=ax)
                            st.pyplot(fig)
                        else:

                            st.info(f'MAE: {mean_absolute_error(y_test,y_pred)}')
                            st.info(f'MSE: {mean_squared_error(y_test,y_pred)}')
                            st.info(f'R^2 Score: {r2_score(y_test,y_pred)}')


                        # to plot  line chart between actual and predicted values
                        fig, ax = plt.subplots()

                        ax.plot(list(y_test), label='Actual')
                        ax.plot(list(y_pred), label='Predicted')

                        ax.set_title("Actual vs Predicted")
                        ax.legend()

                        st.pyplot(fig)
                

                        # to plot features importance on prediction--------
                        result = permutation_importance(
                            myModel,
                            x_test,
                            y_test,
                            n_repeats=10,
                            random_state=42
                        )
                        importance = result.importances_mean
                        fig, ax = plt.subplots()
                        ax.barh(x_test.columns, importance)
                        plt.title('Features Importance')
                        st.pyplot(fig)
