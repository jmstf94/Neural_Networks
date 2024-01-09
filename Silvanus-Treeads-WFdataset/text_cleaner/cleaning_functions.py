import re # maybe just import sub in the future
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from snowballstemmer import stemmer

from .helpers import stripper, Language_Error

# all of the called functions must return text!

def sub_url(text,sub):
    """
    Substitutes http://.... and https://.... link types in a text string.
    """
    return stripper(re.sub(r"http\S+", sub, text))

def sub_users(text,sub):
    """
    Substitutes @.... users from social media text.
    """
    ##There is an issue with the sub puncs function that substitutes the # symbol
    ###This needs to be addressed in some way
    ### for now we just call them as the 'user' puts them in the cleaning mod
    return stripper(re.sub(r"@\S+", sub, text))

def sub_puncs(text,sub):
    """
    string.punctuation is: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    we exclude the symbols <>
    Substitutes !"#$%&\'()*+,-./:;=?@[\\]^_`{|}~ in a text string.
    """
    punc_symbols = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'
    # for now is just symbols basically without the <> but this should be actual punctuation at some point
    # return stripper(text.translate(str.maketrans("!","p", string.punctuation)))
    new_text = ''
    for char in text:
        if char in punc_symbols:
            new_text+=sub
        else:
            new_text+=char
    return stripper(new_text)

def sub_hashtags(text,sub):
    """
    Substitutes #.... users from social media text.

    """
    ###There is an issue with the sub puncs function that substitutes the # symbol
    ###This needs to be addressed in some way
    ### for now we just call them as the 'user' puts them in the cleaning mode

    if sub == 'thirdmode':
        return stripper(re.sub(r'#(\w+)(?=[^\w]|$)', r'\1', text))
    return stripper(re.sub(r"#\S+",sub,text))

def sub_numbers(text,sub):
    """
    Substitutes strings of numbers in a test string.
    """
    return stripper(re.sub(r'\d+', sub , text))

def sub_emoticons(text,sub):
    #### obviously this is not a good way to do this but still the more accurate
    from emoji import EMOJI_DATA
    emoticons = list(EMOJI_DATA.keys())
    em_list = []
    for string in emoticons:
        em_list.append(string.encode('unicode_escape').decode().replace('*','\*'))
    for i in range(len(em_list)):
        x = em_list[i]
        text = re.sub( x , sub ,text)
    return stripper(text)

def remove_stopwords(text,language):
    Language_Error(language)
    stop_words = set(stopwords.words(language))
    words = word_tokenize(stripper(text))
    tokens = [w for w in words if not w in stop_words]
    return stripper(' '.join(tokens))

def stemming(text,language):
    Language_Error(language)
    stem = stemmer(language)
    words = word_tokenize(stripper(text),language = language)
    stemmed_tokens = [stem.stemWord(i) for i in words]
    return stripper(' '.join(stemmed_tokens))

def lower_case(text):
    return stripper(text.lower())
