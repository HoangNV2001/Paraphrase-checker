'''
contain the methods for similarity measures between two sentences (details in the
report),
and vectorize_pair method, which takes in two sentences and returns a 1x9 vector,
corresponding to 9 similarity measures calculated for the pair.
'''


from math import sqrt
from re import compile
from collections import Counter
from numpy import zeros
from nltk import trigrams, bigrams
from numpy import array


def cosine(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Cosine Similarity of the 2 word vectors.
    '''
    vec1 = Counter(text_list1)
    vec2 = Counter(text_list2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = sqrt(sum1) * sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def levenshtein_scaled(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Scaled Levenshtein distance of the 2 word vectors.
    '''
    size_x = len(text_list1) + 1
    size_y = len(text_list2) + 1
    matrix = zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if text_list1[x-1] == text_list2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )

    denominator = max(size_x-1, size_y-1)
    if denominator ==0:
        return 0.0
    else:
        return (matrix[size_x - 1, size_y - 1])/denominator


def jaro_distance(s1, s2) :
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Jaro distance of the 2 word vectors.
    '''
    # If the strings are equal
    if (s1 == s2) :
        return 1.0;

    # Length of two strings
    len1 = len(s1);
    len2 = len(s2);

    if (len1 == 0 or len2 == 0) :
        return 0.0;

    # Maximum distance upto which matching
    # is allowed
    max_dist = (max(len(s1), len(s2)) // 2 ) - 1;

    # Count of matches
    match = 0;

    # Hash for matches
    hash_s1 = [0] * len(s1) ;
    hash_s2 = [0] * len(s2) ;

    # Traverse through the first string
    for i in range(len1) :

        # Check if there is any matches
        for j in range( max(0, i - max_dist),
                    min(len2, i + max_dist + 1)) :

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0) :
                hash_s1[i] = 1;
                hash_s2[j] = 1;
                match += 1;
                break;

    # If there is no match
    if (match == 0) :
        return 0.0;

    # Number of transpositions
    t = 0;

    point = 0;

    # Count number of occurrences
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1) :
        if (hash_s1[i]) :

            # Find the next matched character
            # in second string
            while (hash_s2[point] == 0) :
                point += 1;

            if (s1[i] != s2[point]) :
                point += 1;
                t += 1;
            else :
                point += 1;

        t /= 2;

    # Return the Jaro Similarity
    return ((match / len1 + match / len2 +
            (match - t) / match ) / 3.0);

# Jaro Winkler Similarity
def jaro_Winkler(s1, s2) :
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Jaro Winkler distance of the 2 word vectors.
    '''
    jaro_dist = jaro_distance(s1, s2);

    # If the jaro Similarity is above a threshold
    if (jaro_dist > 0.7) :

        # Find the length of common prefix
        prefix = 0;

        for i in range(min(len(s1), len(s2))) :

            # If the characters match
            if (s1[i] == s2[i]) :
                prefix += 1;

            # Else break
            else :
                break;

        # Maximum of 4 characters are allowed in prefix
        prefix = min(4, prefix);

        # Calculate jaro winkler Similarity
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)

    return jaro_dist;


def manhattan_scaled(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Scaled Manhattan distance of the 2 word vectors.
    '''
    vec1 = Counter(text_list1)
    vec2 = Counter(text_list2)

    union = set(vec1.keys()).union(vec2.keys())

    distance = 0
    for item in union:
        distance += abs(vec1[item] - vec2[item])

    denominator = sum(vec1.values()) + sum(vec2.values())

    if denominator == 0:
        return 0
    else:
        return float(distance)/denominator


def euclidean_scaled(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Scaled Euclidean distance of the 2 word vectors.
    '''
    vec1 = Counter(text_list1)
    vec2 = Counter(text_list2)

    union = set(vec1.keys()).union(vec2.keys())

    distance = 0
    for item in union:
        distance += (vec1[item] - vec2[item])**2

    denominator = sqrt(sum([i**2 for i in vec1.values()]) + sum([i**2 for i in vec2.values()]))

    if denominator == 0:
        return 0
    else:
        return sqrt(distance)/denominator

def bigram_scaled(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Scaled Bi-gram distance of the 2 word vectors.
    '''
    set1 = set(bigrams(text_list1))
    set2 = set(bigrams(text_list2))

    union = set1.union(set2)
    intersection = set1.intersection(set2)


    if len(union) == 0:
        return 0
    else:
        return float(len(intersection))/len(union)

def trigram_scaled(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Scaled Tri-gram distance of the 2 word vectors.
    '''
    set1 = set(trigrams(text_list1))
    set2 = set(trigrams(text_list2))

    union = set1.union(set2)
    intersection = set1.intersection(set2)


    if len(union) == 0:
        return 0
    else:
        return float(len(intersection))/len(union)

def dice(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Dice coefficient of the 2 word vectors.
    '''
    vec1 = Counter(text_list1)
    vec2 = Counter(text_list2)

    intersection = len(set(vec1.keys()) & set(vec2.keys()))
    denominator = len(vec1.keys()) + len(vec2.keys())

    if not denominator :
        return 0.0
    else:
        return 2*intersection/denominator

def jaccard(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: float: Jaccard coefficient of the 2 word vectors.
    '''
    vec1 = Counter(text_list1)
    vec2 = Counter(text_list2)

    intersection = len(set(vec1.keys()) & set(vec2.keys()))
    denominator = len(set(vec1.keys()).union(set(vec2.keys())))

    if not denominator :
        return 0.0
    else:
        return intersection/denominator

def vectorize_pair(text_list1, text_list2):
    '''
    :param: text_list1: list of strings, each string is a word.
    :param: text_list2: list of strings, each string is a word.
    :returns: List of float: The 9 similarity measure values of the 2 word vectors.
    '''
    return [cosine(text_list1,text_list2), levenshtein_scaled(text_list1,text_list2), jaro_Winkler(text_list1,text_list2), manhattan_scaled(text_list1,text_list2), euclidean_scaled(text_list1,text_list2), bigram_scaled(text_list1,text_list2), trigram_scaled(text_list1,text_list2), dice(text_list1,text_list2), jaccard(text_list1,text_list2)]



if __name__ == '__main__':
    text_list1 = ['This', 'is', 'a','foo', 'bar', 'sentence']
    text_list2 = ['fdsvbsa','v','asdfa','asdgadh','asgasgfasdg','afdsbgsa','dgvsdfgvjf','asdfgasdf','asdfasghhh','asdfasasdfadfghe','h','jer','ea','aha','hrtjrj']
    text_list2 = ['This', 'is', 'a','foo', 'bar', 'sentence','but','a','bit','different','o','k','?','gs','gheht','eha','aehaethae','aehaerh','aa','bb','cc','dd','ee']
    text_list3 = ['This', 'is', 'a','foo', 'bar', 'sentence']

    print("Cosine similarity:", cosine(text_list1, text_list2))
    print("Levenshtein scaled:",levenshtein_scaled(text_list1, text_list2))
    print("Jaro-Winkler similarity:", jaro_Winkler(text_list1, text_list2))
    print("Manhattan scaled distance:", manhattan_scaled(text_list1, text_list2))
    print("Euclidean scaled distance:", euclidean_scaled(text_list1, text_list2))
    print("Bigram scaled distance:", bigram_scaled(text_list1, text_list2))
    print("Trigram scaled distance:", trigram_scaled(text_list1, text_list2))
    print("Dice coefficient:", dice(text_list1, text_list2))
    print("Jaccard coefficient:", jaccard(text_list1, text_list2))

    print(vectorize_pair(text_list1,text_list2))
