from tabulate import tabulate


from .helpers import stripper,Language_Error
from .cleaning_functions import *


class Text_Cleaner():
    """
    This is a class that defines the cleaning mode for some text. To see all the possible functions that you can use create
    a text_cleaner instance and use the method show_rule_table.

    # todos: common matching problem: when two ore more cleaning rule function's matches overlap ( one solution that solves
    this is the "correct order" although it can be problematic too)
    """
    def __init__(self,language):
        """
        rules
        """

        self.rule_dict = get_me_the_rule_dict()
        self.cleaning_mode = []
        Language_Error(language)
        self.language = language

        # add two attributes for the maximum length of choices and rules

        # this creates  the rule table from the self.rule_dict

        rule_table = [["Extracts and Processes","Substitutions and Specifications"]]
        for i in self.rule_dict.keys():
            choices = []
            for j in self.rule_dict[i][1].keys():
                choices.append(self.rule_dict[i][1][j][0])
            rule_table.append([self.rule_dict[i][0],choices])
        self.rule_table = rule_table

    def add_cleaning_rules(self, *cleaning_rules):
        """
        With this method we add as many cleaning_rules(2-tuples) we want.
        """
        for i in cleaning_rules:
            if ((not isinstance(i,tuple)) or (len(i)!=2)):
                raise TypeError("Expected 2-tuples.")
            # add another if raise error for the maximum numbers in the tuples
            # add another to allow only one sub for each extra
            self.cleaning_mode.append(i)

    def get_cleaning_mode(self):
        return self.cleaning_mode

    def str_cleaning_mode(self):
        latable = [["Extracts","Substitutions"]]
        for i in range(len(self.cleaning_mode)):
            ext = self.cleaning_mode[i][0]
            sub = self.cleaning_mode[i][1]
            latable.append([self.rule_dict[ext][0],self.rule_dict[ext][1][sub][0]])

        return tabulate(latable, headers="firstrow", tablefmt="fancy_grid")

    def show_cleaning_mode(self):
        latable = [["Extracts","Substitutions"]]
        for i in range(len(self.cleaning_mode)):
            ext = self.cleaning_mode[i][0]
            sub = self.cleaning_mode[i][1]
            latable.append([self.rule_dict[ext][0],self.rule_dict[ext][1][sub][0]])

        print(tabulate(latable, headers="firstrow", tablefmt="fancy_grid"))

    def set_standard_cleaning(self):
        self.cleaning_mode = [(1,1),(2,1),(3,0),(4,1),(5,2),(6,0),(7,0)]

    def show_rule_table(self):
        """
        The cleaning rules tables is presented with the suggested order for better results.
        """
        print(tabulate(self.rule_table, headers="firstrow", tablefmt="fancy_grid"))

    def clean(self,text):
        ## here some extra feature would be to specify the order of the applied cleaning rules

        ### we could include a safety net to check that the function returns text

        ###There is an issue of the hashtag with the sub puncs function that substitutes the # symbol
        ###This needs to be addressed in some way
        ### for now we just call them as the 'user' puts them in the cleaning mode

        ### maybe we need a keep only letter function here and except my <>

        for mode in self.cleaning_mode:
            x,y = mode
            if x==8 or x==9:
                text = stripper(self.rule_dict[x][1][y][1](text,self.language))
            else:
                text = stripper(self.rule_dict[x][1][y][1](text))
        return text


def get_me_the_rule_dict():
    rule_dict = {
        1:  ('01-emoticons',
             {
              0: ('Remove', lambda text: sub_emoticons(text,' ')),
              1: ('Substitute with <EMOTICON>', lambda text: sub_emoticons(text,' <EMOTICON> '))
             }
            ),
        2 : ('02-urls',
             {
              0: ('Remove', lambda text: sub_url(text,' ')),
              1: ('Substitute with <URL>', lambda text: sub_url(text,' <URL> '))
             }
            ),
        3 : ('03-lowercase',
             {
              0: ('Every letter to a lower case letter', lambda text: lower_case(text))
             }
            ),
        4 : ('04-users',
             {
              0: ('Remove', lambda text: sub_users(text,' ')),
              1: ('Substitute with <USER>', lambda text: sub_users(text,' <USER> '))
             }
            ),
        5 : ('05-hashtags',
             {
              0: ('Remove', lambda text: sub_hashtags(text,' ')),
              1: ('Substitute with <HASHTAG>', lambda text: sub_hashtags(text,' <HASHTAG> ')),
              2: ('Substitute with the hashtag word', lambda text: sub_hashtags(text,'thirdmode'))
             }
            ),
        6 : ('06-punctuation',
             {
              0: ('Remove', lambda text: sub_puncs(text,' ')),
              1: ('Substitute with <PUNC>', lambda text: sub_puncs(text,' <PUNC> '))
             }
            ),
        7: ('07-numbers',
             {
              0: ('Remove', lambda text: sub_numbers(text,' ')),
              1: ('Substitute with <NUMBER>', lambda text: sub_numbers(text,' <NUMBER> '))
             }
            ),
        8: ('08-stopwords',
             {
              0: ('Remove', lambda text,lang: remove_stopwords(text,lang))
             }
            ),
        9: ('09-stemming',
             {
              0: ('Snowball Stemmer', lambda text,lang: stemming(text,lang))
             }
            )
    }
    return rule_dict
