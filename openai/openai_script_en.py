import nltk
import openai

"""This script is used to get the restults from ChatGPT when we want to analyse documents in portuguese 
"""

# place your OpenAI key here
openai.api_key = "secret"
# change the path of the document you want to analyse here
filename = "../test_en.txt"


def count_tokens(filename):
    """Counts the tokens in a document

    Args:
        filename (string): file path of the document

    Returns:
        int: returns the number of tokens in the document
    """
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = nltk.word_tokenize(text, language="english")
    return len(tokens), tokens


def break_up_file(tokens, chunk_size, overlap_size):
    """Breaks up the document

    Args:
        tokens (int): number of tokens
        chunk_size (int): size of each chunk
        overlap_size (int): number of overlap tokens in order to not lose information
    """
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(
            tokens[chunk_size - overlap_size :], chunk_size, overlap_size
        )


def break_up_file_to_chunks(filename, chunk_size=2000, overlap_size=100):
    """Breaks up the document into chunks of a certain size

    Args:
        filename (string): file path to the document
        chunk_size (int): size of each chunk. Defaults to 2000.
        overlap_size (int): number of overlap tokens. Defaults to 100.

    Returns:
        list: returns a list with all the chunks
    """
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = nltk.word_tokenize(text, language="english")
    return list(break_up_file(tokens, chunk_size, overlap_size))


def convert_to_prompt_text(tokenized_text):
    """Converts the prompt into prompt text since we have tokenized the document

    Args:
        tokenized_text (string): file path to the document

    Returns:
        string: returns a string with the text of a chunk
    """
    prompt_text = " ".join(tokenized_text)
    prompt_text = prompt_text.replace(" ,", ",")
    prompt_text = prompt_text.replace(" :", ":")
    prompt_text = prompt_text.replace(" .", ".")
    return prompt_text


"""The same prompt is sent to ChatGPT for every chunk we got and the responses are saved in an array
"""
prompt_response = []
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):
    print("Question for chunk " + str(i))
    prompt_request = """Summarize the following text and identify all people, companies, specifics and general topics referred to in this text. Please answer in the exact format.

                    Desired format:
                    Abstract: <abstract up to 50 words>
                    Person names: <comma_separated_list_of_company_names>
                    Company names: -||-
                    Specific topics: -||-
                    General topics: -||-

                    Text:""" + convert_to_prompt_text(
        chunks[i]
    )

    messages = [{"role": "system", "content": "This is text summarization."}]
    messages.append({"role": "user", "content": prompt_request})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.5,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    prompt_response.append(response["choices"][0]["message"]["content"].strip())
    print("Got reponse to chunk " + str(i))

"""We write to a file all the responses we got from ChatGPT
"""
print("Starting to write on file")

with open("chatgpt.txt", "w", encoding="utf-8") as f:
    f.flush()
    for res in prompt_response:
        f.write("%s\n" % res)
        f.write("---\n")
    f.close()

print("Done Writting")
