Experiments on hypothesis detection in scientific literature.

* [notes on existing work](docs/hypothesis-detection-notes.md)

* [experimenting with existing relevant datasets](dataset/Readme.md)


## Assemble resources 

Survive in the python dependency marshlands:

```
virtualenv --system-site-packages -p python3.8 env
source env/bin/activate
```

Install dependencies:

```sh
pip3 install -r requirements.txt 
```

Assemble resources in the same JSON format: 

```sh
python3 hypothesis_detection/assemble_dataset.py
```

This will create our hypothesis Frankenstein dataset under `dataset/combined` one JSON file per orginal corpus in the same JSON format, ready for training a classifier. 

Below some statics on the individual and combined datasets, see [here](dataset/Readme.md) for more information: 

| corpus               | Level   | Hypothesis sentences | Non-hypothesis sentences | total        | 
|---                   |---      |---                   |---                       |---           |
| ART/CoreSC           |full-text| 656 (1.9%)           | 34024 (98.1%)            | 34680 (100%) |
| Multi-CoreSC CRA     |full-text| 152 (1.8%)           | 8349 (98.2%)             | 8501 (100%)  |
| SciARG               | abstract| 48 (1.2%)            | 3938 (98.8)              | 3986 (100%)  |
| PHAEDRA              | abstract| 274                  | -                        | 274          |
| Meta-knowledge_GENIA | abstract| 442 (5.5%)           | 7559 (94.5%)             | 8501 (100%)  |
| __aggregated__       | mixed   | __1572 (2.8%)__      | __53870 (97.2%)__        | __55442 (100%)__ |

## Train a classifier

Assuming the above step for creating an environment and installing the dependencies have been done, we can fine-tune a SciBERT binary classifier at sentence level (`is_hypothesis_sentence` or `is_not_hypothesis_sentence`) using [DeLFT](https://github.com/kermitt2/delft) as follow: 

```console
python3 hypothesis_detection/sentence_classifier.py train --architecture bert --transformer allenai/scibert_scivocab_cased
```

For using a LinkBERT base model: 

```console
python3 hypothesis_detection/sentence_classifier.py train --architecture bert --transformer michiyasunaga/LinkBERT-base
```

Replace the model name by `dmis-lab/biobert-v1.1` for instance to use bioBERT pre-trained model, or any other pretrained model available on HuggingFace Hub.


## Evaluation of binary classifier

Use `train_eval` action instead of just `train`, this will be an evaluation on random 10% data partition excluded from training. 

```console
python3 hypothesis_detection/sentence_classifier.py train_eval --architecture bert --transformer allenai/scibert_scivocab_cased
```

```
Evaluation on 5704 instances:
                   precision        recall       f-score       support
not_hypothesis        0.9876        0.9929        0.9903          5531
    hypothesis        0.7273        0.6012        0.6582           173
```

Here is a basic benchmarking for sentence-level hypothesis prediction with the combined dataset using the three main BERT models pre-trained on scientific contexts. These are direct fine-tuning of the pre-trained models, without usual techniques like over-sampling and training data augmentation to address very unbalanced corpus or ensemble approaches. 

| pre-trained models |  precision   |     recall   |    f-score   |    support |
|---                 |---           |---           |---           |---         |
| SciBERT            |  72.73       |   60.12      |   65.82      |   173      |
| BioBERT 1.1        |  76.34       |   57.80      |   65.79      |   173      |
| LinkBERT base      |  72.66       |   58.38      |   64.74      |   173      |


**Note:** No evaluation done with LLM and few shot learning at this stage, considering the low average results on focused task performance as compared to fine-tuned BERT-style SOTA models, see [note on LLM task performance](docs/note_on_llm_task_performance.md)
