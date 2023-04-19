import json
import argparse
import time
import numpy as np
import re
import random

from delft.utilities.Embeddings import Embeddings
from delft.utilities.Utilities import split_data_and_labels
from delft.utilities.Tokenizer import tokenizeAndFilterSimple
from delft.textClassification.reader import vectorize as vectorizer
from delft.textClassification.reader import normalize_classes
from delft.utilities.numpy import shuffle_triple_with_view
import delft.textClassification
from delft.textClassification import Classifier
from delft.textClassification.models import architectures

from blingfire import text_to_sentences

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning) 

"""
    A simple binary classifier to predict if a sentence is expressing an hypothesis or not.
"""

list_classes = ["not_hypothesis", "hypothesis"]

class_weights = {
                    0: 1.,
                    1: 1.
                }

def configure(architecture):
    batch_size = 256
    maxlen = 300
    patience = 5
    early_stop = True
    max_epoch = 60

    # default bert model parameters
    if architecture == "bert":
        batch_size = 32
        early_stop = False
        max_epoch = 3
        maxlen = 100

    return batch_size, maxlen, patience, early_stop, max_epoch

def load_hypothesis_corpus_json(json_path):
    texts_list = []
    classes_list = []

    with open(json_path, 'r') as fin:
        units = json.load(fin)
        for unit in units:
            #if unit["class"] == "hypothesis" or random.uniform(0, 1) < 0.1:
            texts_list.append(unit["text"])
            classes_list.append(unit["class"])

    list_possible_classes = np.asarray(list_classes)
    classes_list_final = normalize_classes(classes_list, list_possible_classes)

    texts_list_final = np.asarray(texts_list)
    texts_list_final, classes_list_final, _ = shuffle_triple_with_view(texts_list_final, classes_list_final)

    return texts_list_final, classes_list_final

def train(embeddings_name, fold_count, architecture="gru", transformer=None):
    print('loading binary hypothesis dataset...')
    xtr, y = load_hypothesis_corpus_json("dataset/combined/frankenstein.json")

    model_name = 'hypothesis_'+architecture
    #class_weights = None

    batch_size, maxlen, patience, early_stop, max_epoch = configure(architecture)

    model = Classifier(model_name, architecture=architecture, list_classes=list_classes, max_epoch=max_epoch, fold_number=fold_count, patience=patience,
        use_roc_auc=True, embeddings_name=embeddings_name, batch_size=batch_size, maxlen=maxlen, early_stop=early_stop,
        class_weights=class_weights, transformer_name=transformer)

    if fold_count == 1:
        model.train(xtr, y)
    else:
        model.train_nfold(xtr, y)
    # saving the model
    model.save()


def train_and_eval(embeddings_name, fold_count, architecture="gru", transformer=None): 
    print('loading binary hypothesis dataset...')
    xtr, y = load_hypothesis_corpus_json("dataset/combined/frankenstein.json")

    nb_hypothesis = 0
    for the_class in y:
        if the_class[1] == 1.0:
            nb_hypothesis += 1
    nb_not_hypothesis = len(y) - nb_hypothesis
    print("\ttotal:", len(y))
    print("\tnot hypothesis:", nb_not_hypothesis)
    print("\thypothesis:", nb_hypothesis)

    model_name = 'hypothesis_'+architecture
    #class_weights = None

    # segment train and eval sets
    x_train, y_train, x_test, y_test = split_data_and_labels(xtr, y, 0.9)

    batch_size, maxlen, patience, early_stop, max_epoch = configure(architecture)

    model = Classifier(model_name, architecture=architecture, list_classes=list_classes, max_epoch=max_epoch, fold_number=fold_count, patience=patience,
        use_roc_auc=True, embeddings_name=embeddings_name, batch_size=batch_size, maxlen=maxlen, early_stop=early_stop,
        class_weights=class_weights, transformer_name=transformer)

    if fold_count == 1:
        model.train(x_train, y_train)
    else:
        model.train_nfold(x_train, y_train)
    model.eval(x_test, y_test)

    # saving the model
    model.save()


# classify a list of texts
def classify(texts, output_format, embeddings_name=None, architecture="gru", transformer=None):
    # load model
    model = Classifier('hypothesis_'+architecture, architecture=architecture, list_classes=list_classes, embeddings_name=embeddings_name, transformer_name=transformer, class_weights=class_weights)
    model.load()
    start_time = time.time()
    result = model.predict(texts, output_format)
    runtime = round(time.time() - start_time, 3)
    if output_format == 'json':
        result["runtime"] = runtime
    else:
        print("runtime: %s seconds " % (runtime))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Classify whether a sentence expressed an hypothesis or not, using the DeLFT library")

    word_embeddings_examples = ['glove-840B', 'fasttext-crawl', 'word2vec']
    pretrained_transformers_examples = [ 'bert-base-cased', 'bert-large-cased', 'allenai/scibert_scivocab_cased', 'michiyasunaga/LinkBERT-base', 'dmis-lab/biobert-v1.1' ]

    parser.add_argument("action")
    parser.add_argument("--fold-count", type=int, default=1)
    parser.add_argument("--architecture",default='gru', help="type of model architecture to be used, one of "+str(architectures))
    parser.add_argument(
        "--embedding", 
        default=None,
        help="The desired pre-trained word embeddings using their descriptions in the file. " + \
            "For local loading, use delft/resources-registry.json. " + \
            "Be sure to use here the same name as in the registry, e.g. " + str(word_embeddings_examples) + \
            " and that the path in the registry to the embedding file is correct on your system."
    )
    parser.add_argument(
        "--transformer", 
        default=None,
        help="The desired pre-trained transformer to be used in the selected architecture. " + \
            "For local loading use, delft/resources-registry.json, and be sure to use here the same name as in the registry, e.g. " + \
            str(pretrained_transformers_examples) + \
            " and that the path in the registry to the model path is correct on your system. " + \
            "HuggingFace transformers hub will be used otherwise to fetch the model, see https://huggingface.co/models " + \
            "for model names"
    )

    args = parser.parse_args()

    if args.action not in ('train', 'train_eval', 'classify'):
        print('action not specified, must be one of [train,train_eval,classify]')

    embeddings_name = args.embedding
    transformer = args.transformer

    architecture = args.architecture
    if architecture not in architectures:
        print('unknown model architecture, must be one of '+str(architectures))

    if transformer == None and embeddings_name == None:
        # default word embeddings
        embeddings_name = "glove-840B"

    if args.action == 'train':
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")

        train(embeddings_name, args.fold_count, architecture=architecture, transformer=transformer)

    if args.action == 'train_eval':
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")

        y_test = train_and_eval(embeddings_name, args.fold_count, architecture=architecture, transformer=transformer)    

    if args.action == 'classify':
        someTexts = ['Transketolase (TKT) is an enzyme that is ubiquitously expressed in all living organisms and has been identified as an important regulator of cancer. Recent studies have shown that the TKT family includes the TKT gene and two TKT-like (TKTL) genes; TKTL1 and TKTL2. TKT and TKTL1 have been reported to be involved in the regulation of multiple cancer-related events, such as cancer cell proliferation, metastasis, invasion, epithelial-mesenchymal transition, chemoradiotherapy resistance, and patient survival and prognosis. Therefore, TKT may be an ideal target for cancer treatment. More importantly, the levels of TKTL1 were detected using EDIM technology for the early detection of some malignancies, and TKTL1 was more sensitive and specific than traditional tumor markers. Detecting TKTL1 levels before and after surgery could be used to evaluate the surgery\'s effect. While targeted TKT suppresses cancer in multiple ways, in some cases, it has detrimental effects on the organism. In this review, we discuss the role of TKT in different tumors and the detailed mechanisms while evaluating its value and limitations in clinical applications. Therefore, this review provides a basis for the clinical application of targeted therapy for TKT in the future, and a strategy for subsequent cancer-related research.']
        someSentences = text_to_sentences(someTexts[0]).split("\n")
        result = classify(someSentences, "json", architecture=architecture, embeddings_name=embeddings_name, transformer=transformer)
        print(json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False))
