# README
# Dataset
For this project i will use the [Kaggle Mental Health Dataset](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset).  
Because the dataset is pretty large, i will split the dataset in a train and test dataset as is the norm with most AI projects. Validation will simply be done with cross-validation.  
New data for use in the service will come from the user's own answers in a google forum.

## Purpose

The program aims to train an AI model capable of predicting an individual's mental health status based on a set of **17** properties:

1. Timestamp
2. Gender
3. Country
4. Occupation
5. Family History
6. Treatment History
7. Days Spent Indoors
8. Level of Growing Stress
9. Changes in Habits
10. Personal Mental Health History
11. Frequency of Mood Swings
12. Coping Mechanisms and Struggles
13. Interest in Work
14. Social Weakness
15. Participation in Mental Health Interviews
16. Awareness of Available Care Options

By analyzing these properties, the program aims to provide insights into an individual's mental well-being and offer potential predictions to aid in early intervention or support. This can be particularly useful in identifying individuals who may benefit from mental health resources or interventions, thereby contributing to improved overall mental health outcomes. My goal is for my service to be used to gauge wether or not you need to contact a professional for further analysis, or if you're probably just fine.

>[!CAUTION]
>It is important to remember that the AI is never 100% correct and should not be used as a replacement for actual professionals, but rather as a tool to estimate your mental health before taking further action.

## Flows & Actions
Like most AI projects my program will consist of several flows:

- #### data reading
    - **for training**
        - reading data from API endpoint (if no data is present)
        - saving data locally
    - **for use**
        - reading ouput from google forums
        - saving data for use in dataprep
- #### data prepping
    - preprocessing
    - converting the data to a better form to make it processable for the AI
    - removing personal data users might have filled in on accident
- #### training
    - training a basic regressor with default hyperparameters 
    - saving results as an experiment
- #### hyperparameter tuning *(only during training phase)*
    - using grid search to look for most optimal hyperparameters
    - saving results to experiments
- #### model registry
    - choosing best model based on the experiment output
    - saving said model for use in production

