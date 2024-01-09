# helper functions and classes
import re
from nltk.corpus import stopwords

def stripper(text):
    text = text.strip()
    text = re.sub(r' {2,}',' ',text)
    text = text.strip()
    return text

class Language_Error(Exception):
    """
    This class checks the languages we support and raises an error for wrong choice of language.
    """
    def __init__(self,language):

        self.supported_languages = stopwords.fileids()

        if language not in self.supported_languages:
            raise self

    def __str__(self):
        return f"The languages that can be used are:\n{self.supported_languages}"
