# ml-text-assistant

ML text assistant helps researchers extract and prepare texts from PDF's. It also provides coherence analysis utility for gesim topic extraction models.

---

## Install

This project uses pipenv as a dependencies maneger.

Assuming you already have pipenv intalled, you should intall the project with:

```make install```

This command will create a virtual env and install all dependencies.

---

## How to develop

Use Makefile functions to help you develop for this project.

```make build```

```make test```

```make coverage```

---

## How to use

Assistant provides some utilities to deal with text analysis.

```python
from ml_text_assistant import Assistant

assistant = Assistant()
```

Extract text from pdf files:

```python
# You could provide path to file or path to directory with pdf files as input
assistant.pdf_to_text('/path/to/pdf/', '/path/to/txt/')
```

Clean text and generate tokenized output:

```python
# You could provide path to file or path to directory with txt files as input
assistant.text_to_csv('/path/to/txt/', '/path/to/csv')
```

Generated files placed into provided output path:

```
/
└── path
    └── to
        ├── csv
        │   └── dataset.csv
        ├── pdf
        │   └── 3382494.3422167.pdf
        └── txt
            └── 3382494.3422167.txt

```

Or you could simply:

```python
# Read pdf files and generate cleaned tokenized dataset.csv
assistant.dataset('/path/to/pdf/', '/path/to/csv')
```

Explore some metrics about topic modeling strategies:

```python
tokens = #read content column from csv file

explorer = assistant.explorer(tokens)

def model_builder(num_topics, corpus, dictionary):
    return model # Any gensim compatible model

# Run model extracting 2 topics
explorer.coherence(2, model_builder)

# Run model extracting 5 topics
explorer.coherence(5, model_builder)

# Run model extracting 10 topics
explorer.coherence(10, model_builder)

# What extracted number of topics is the more coherent?
print(explorer.best())

# Suppose 5 topics are the best!
resume = explorer.resume(5, model_builder)
```

Resumed model. It shows the main topic for each document in the corpus:

```
| topic_id | topic_score | topic_keywords | document_original_id |
|----------|-------------|----------------|----------------------|
| 4        | 0.40971     | project,...    | 0                    |
| 4        | 0.5847      | project,...    | 1                    |
| 4        | 0.86529     | project,...    | 2                    |
```

## Examples

See `examples` folder for iteractive `jupyter` notebooks.

## Specification

See `spec` folder for details.