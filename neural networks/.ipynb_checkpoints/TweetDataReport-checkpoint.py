import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

class Relovir_Error(Exception):
    """
    This class checks if the given relovir number is acceptable based on the ratio of the dataset you gave.
    The dataset of course must be a pandas dataframe with two columns.The second column must be the 0
    (irrelevant) or 1(relevant) values of the corresponding tweets/representations. 
    
    """
    def __init__(self,dataset,relovir):
        self.relovir = relovir
        dataset = dataset.copy()
        checker = check_relevance_balance(dataset).copy()
        self.irr = checker.loc[checker['relevance']==0,'count'].reset_index(drop=True)[0]
        self.rel = checker.loc[checker['relevance']==1,'count'].reset_index(drop=True)[0]
        self.ratio = self.rel/self.irr
        if self.relovir>self.ratio or self.relovir>1:
            raise self
    def __str__(self):
        if self.relovir>self.ratio:
            return f"The relovir ratio of your dataset is {self.ratio} but you gave me {self.relovir}. The relovir ratio cannot be larger than 1."

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
    df = df.copy()
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

    FUTURE: split datafram to relevant and irrelevant and then pick equal number of them to create the final dataset or with a
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
    return training_set_X, test_set_X, y_train.to_numpy().reshape(-1), y_test.to_numpy().reshape(-1)

def datasplit_new(df,testsize,relovir=None):
    """
    Firstly we split the dataset into train and test parts.
    
    Then we create the training dataset by picking up the irrelevant tweets from the training 
    split part with only the number of relevant tweet
    
    The relovir variable represents the relative ratio of irrelevant(we usually have more irrelevant so) 
    over relevant number of training examples in the set.
    
    Returns as a (examples,768) np array the representations and the y as (examples,) shaped np array.
    
    Future: maybe it would be better to split the dataset by relevance and then pick up the "correct" 
    relovir ratio for the test dataset from the ratio of the total dataset. 
    Now we include some randomness which is not particularly wanted due to the fact that after the split
    the relovir ratios of the training and test parts won't match exactly. 
    I will have to make 20 30 iterations per model to make sure we get the average.
    In the other case we were going to be satisfied with 5. 
    """
    df = df.copy() # make a copied instance of the dataset
    
    X_train, X_test, y_train, y_test = train_test_split(df['reps'], df['relevance'], test_size = testsize)

    if relovir is not None:
        
        Relovir_Error(df,relovir) # check if you can accept the relovir variable instance maybe the ratio is not that big
        
        # now we reconstruct the training dataset in order to use the relovir 
        training_set = pd.DataFrame()
        training_set['reps'] = X_train
        training_set['relevance'] = y_train
        training_set.reset_index(drop = True)
        # we split the training data in irrelevant and relevant cases
        # we make sure the zeros and the ones correctly correspond to irr and rel respectively
        grouping = training_set.groupby('relevance')
        group_dict = {}
        for name, group in grouping:
            group_dict[str(name)] = group
        # we find the absolute numbers 
        irr = group_dict['0']
        rel = group_dict['1']
        #print(len(irr)+len(rel))
        #pickup all the irrelevants and the correct random part of the relevants
        dfirr = irr.sample(frac = 1).reset_index(drop = True)
        #print(len(dfirr))
        dfrel = rel.sample(n = int(len(irr)*relovir)).reset_index(drop = True)
        #print(len(dfrel))
        #print(len(dfirr)+len(dfrel)
        training_set = None
        training_set = pd.concat([dfirr, dfrel]).sample(frac = 1).reset_index(drop = True)
    
    training_set_X = np.vstack(training_set['reps'])
    test_set_X = np.vstack(X_test)
    y_train = training_set['relevance'].to_frame().reset_index(drop = True)
    y_test = y_test.to_frame().reset_index(drop = True)
    return training_set_X, test_set_X, y_train.to_numpy().reshape(-1), y_test.to_numpy().reshape(-1)


def preparer(df):
    """
    returns the prepared dataframe
    """
    df = df.copy()

    #keep only text and relevance
    column_names = df.columns.to_list()

    accepted_text_names = ['text','full_text','reps']
    accepted_relevancy_names = ['relevance','relevant']

    for name in accepted_text_names:
        if name in column_names:
            new_df = df[name].copy()

    for name in accepted_relevancy_names:
        if name in column_names:
            new_df = pd.concat([new_df, df[name]], axis=1)

    #drop duplicates, shuffle randomly , reset index, rename columns
    new_df = new_df.drop_duplicates()
    new_df.columns = ['text','relevance']
    new_df = new_df.sample(frac=1).reset_index(drop=True)

    #make relevance an int instead of boolean
    new_df['relevance'] = new_df['relevance'].apply(lambda x: np.int64(x))
    return new_df
