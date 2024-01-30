import nltk
import pandas as pd

"""This script is used to count how many times a word appears in a document and to count how many times
a category result is mentioned in the same document 
"""

# change the path of the document you want to analyse here
FILENAME = "./results/test_en.txt"
# change the file with the category results
CATEGORYFILE = "./results/nysrpa_vs_bruen/gpt-3.5-turbo-0613/people.txt"

exp_matches = []
df_matches = pd.DataFrame()
df_countwords = pd.DataFrame()


def get_files_and_tokenization(filename, categoryfile):
    """Tokenizes both document and category results

    Args:
        filename (string): file path to the document
        categoryfile (string): file path of the file with the category results

    Returns:
        token_list (list []): returns a list with the tokens of the document
        splitted_dictionary (list []): returns a list with the tokens of a category results
    """
    words = open(categoryfile, "r", encoding="utf-8").read().splitlines()
    dictionary = [x.lower() for x in words if x == " " or len(x) > 2]
    splitted_dictionary = []
    for exp in dictionary:
        splitted_dictionary.append(nltk.word_tokenize(exp, language="english"))

    for split_exp in splitted_dictionary:
        exp_matches.append(tuple([split_exp, 0]))

    file_content = open(filename, encoding="utf-8").read()
    raw_token_list = nltk.word_tokenize(file_content, language="english")
    stopwords = ["eos", "EOS"]
    token_list = [x.lower() for x in raw_token_list]

    """Uncomment if you want to refine the tokens of the document
    """
    # tokens = refine_token_list(token_list)
    with open("tokens.txt", "w", encoding="utf-8") as f:
        f.flush()
        for item in token_list:
            f.write("%s\n" % item)
    f.close()
    print("Done Tokens")

    return token_list, splitted_dictionary


def refine_token_list(token_list):
    """Refines the original token list

    Args:
        token_list (string []): list of tokens from the document

    Returns:
        string []: returns a refined list of the tokens
    """
    refined_token_list = []
    for token in token_list:
        token = token.lower()
        if token.isalpha():
            new_token = token
        else:
            new_token = ""
        if new_token != "" and len(new_token) >= 2:
            vowels = len([v for v in new_token if v in "aeiou"])
            if vowels != 0:
                refined_token_list.append(new_token)

    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.extend(["eos"])
    tokens = [x for x in refined_token_list if x not in stopwords]
    return tokens


def count_words(token_list):
    """Counts the number of times the tokens from the document appear in document

    Args:
        token_list (string []): list of tokens from the document

    Returns:
        DataFrame: returns a list with the tokens from the document and the amount times they are mentioned
    """
    tokens = refine_token_list(token_list)
    freqs = nltk.FreqDist(tokens).items()
    freqs = sorted(freqs, key=lambda tup: tup[1], reverse=True)

    df_countwords = pd.DataFrame(freqs, columns=["Word", "Count"])

    with open("count_words.txt", "w", encoding="utf-8") as f:
        f.flush()
        f.write(df_countwords.to_string())
    f.close()
    print("Done Count Words")
    df_countwords.index += 1
    return df_countwords


def count_matches(token_list, splitted_dictionary):
    """Algorithm to count the amount of times category results appear in a document

    Args:
        token_list (string []): list with the tokens of the document
        splitted_dictionary (string []): list with the tokens of a category results
    """
    for i in range(len(token_list)):
        for j in range(len(splitted_dictionary)):
            exp_size = len(splitted_dictionary[j])
            if token_list[i] == splitted_dictionary[j][0]:
                for k in range(exp_size):
                    if (
                        k == exp_size - 1
                        and token_list[i + k] == splitted_dictionary[j][k]
                    ):
                        new_value = exp_matches[j][1] + 1
                        exp_matches[j] = (exp_matches[j][0], new_value)
                    else:
                        if token_list[i + k] == splitted_dictionary[j][k]:
                            continue
                        else:
                            break
            else:
                continue


def matching_exp(token_list, splitted_dictionary):
    """Counts the number of times the category results are mentioned in the document

    Args:
        token_list (string []): list with the tokens of the document
        splitted_dictionary (string []): list with the tokens of a category results

    Returns:
        DataFrame: returns a list with the category results and the amount times they are mentioned in the document
    """
    count_matches(token_list, splitted_dictionary)
    exp_matches.sort(key=lambda x: x[1], reverse=True)

    df_matches = pd.DataFrame(exp_matches, columns=["Expression", "Count"])

    with open("matching.txt", "w", encoding="utf-8") as f:
        f.flush()
        f.write(df_matches.to_string())
    f.close()
    print("Done Matching")
    df_matches.index += 1
    return df_matches


token_list, splitted_dictionary = get_files_and_tokenization(FILENAME, CATEGORYFILE)
df_matches = matching_exp(token_list, splitted_dictionary)
count_words(token_list)
