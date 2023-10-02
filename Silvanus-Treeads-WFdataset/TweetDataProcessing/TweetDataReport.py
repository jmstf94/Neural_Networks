import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

def print_tweet_report(df):
    """
    bla bla bla
    """
    column_names = list(df.columns)
    subseries =  [df.iloc[:,n] for n in range(0,len(column_names))]
    def get_shapelen(x):
        try:
            return x.shape
        except:
            return '---'
    shape_len = [get_shapelen(serie[0]) for serie in subseries]
    types = [type(serie[0]) for serie in subseries]
    subseries = [serie.astype(str) for serie in subseries]
    unique_values = [len(serie.unique()) for serie in subseries ]
    info = pd.DataFrame( { 'column_names':column_names, 'data_types':types, 'shape_len': shape_len, 'unique_values':unique_values} )
    return info

def check_relevance_balance(df):
    """
    bla bla bla
    """
    total = len(df)
    report = df['relevance'].value_counts().to_frame().reset_index()
    report.columns = ['relevance', 'count']
    report['balance'] = round(report['count']/total*100,2)
    report['balance'] = report['balance'].map(lambda x: str(x)+'%')
    return report

def datasplit(df,testsize,relovir=None):
    """
    Use the train test split function to get random splits each time from the whole dataframe.

    Return as a (examples,768) np array the representations and as a pandas series the y

    FUTURE: split datafram to relevan and irrelevant and then pick equal number of them to create the final dataset or with a
    parameter that defines the relation between 0 and 1 cases.
    # The relovir variable represents the relative ratio of irrelevant(we usually have more irrelevant so) over relevant number of training     examples in the set
    """
    if relovir is not None:
        grouping = df.groupby('relevance')
        group_dict = {}
        for name, group in grouping:
            group_dict['rel'+str(name)] = group
        irr = group_dict['rel0']
        rel = group_dict['rel1']
        the_smaller = min(len(irr),len(rel))
        irr = irr.sample(n=int(the_smaller*relovir)).reset_index(drop = True)
        rel = rel.sample(n=the_smaller).reset_index(drop = True)
        df = pd.concat([irr, rel]).sample(frac = 1).reset_index(drop = True)
    X_train, X_test, y_train, y_test = train_test_split(df['reps'], df['relevance'], test_size=testsize)
    training_set_X = np.vstack(X_train)
    test_set_X = np.vstack(X_test)
    y_train = y_train.to_frame().reset_index(drop = True)
    y_test = y_test.to_frame().reset_index(drop = True)
    return training_set_X, test_set_X, y_train, y_test
