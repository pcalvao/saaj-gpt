# SAAJ-GPT

## Overview
System for analyzing legal documents using ChatGPT and Natural Language Processing (NLP) with Natural Language Toolkit (NLTK). The system is capable of analyzing documents both in English and Portuguese, although was developed with the analysis of documents in Portuguese in mind. The system funcionalities are the following:
* Get a summary of the document being analyze
* Get the results identified by ChatGPT for a category (People, Companies, Specific Topics and General Topics)
* Get the local summaries of every result identified by ChatGPT
* Create a personalized law dictionary
* Take notes as you analyze your document and download it at the end

## Installation
Start by downloading the code and extracting the zip to your code.

Open the code and install all Python libraries required with the command:
```
pip install -r requirements.txt
```

After all the libraries are installed you can run the system locally with the command:
```
python ./api/app.py
```

If you wanna access the system online, click [here](http://pedrocalvao.pythonanywhere.com/). Some of the drawbacks of using the system online are the fact that the version available is the first version of the system developed which has a not so friendly interface and the functionality of getting the local summaries of the results identified by ChatGPT is not working. Other drawback of the online version is the fact that it only has available one document to be analyzed. 

## Interface

This is the interface of the system when analyzing a document:

<img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface.png?raw=true" width="600" height="400">

On the left column of the system, is where the user can select the expressions to add to his personalized law dictionary and also select which category he wants to get results from. Also on this column the user can find his notepad.

<p float="left">
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-selector.png?raw=true" width="30%" />
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-notepad.png?raw=true" width="30%" />
</p>

On the middle column of the interface, the user can find the results to the category he selected, the local summaries of result he selects and the personalized law dictionary.

<p float="left">
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-category-results.png?raw=true" width="30%" />
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-local-summaries.png?raw=true" width="30%" />
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-personalized-law-dictionary.png?raw=true" width="30%" />
</p>

On the right column, we can find the document being analyzed or when the user wants to check the different contexts of a result, the document generated with those contexts.

<p float="left">
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-document.png?raw=true" width="30%" />
  <img src="https://github.com/pcalvao/saaj-gpt/blob/main/images/interface-context-document.png?raw=true" width="30%" />
</p>
