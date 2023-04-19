Dataset with binary sentence classification `hypothesis-sentence` `not-hypothesis-sentence`.

## Building the dataset

This dataset is based on a combination of the following ones: 

- [ART/CoreSC Corpus](https://www.aber.ac.uk/en/cs/research/cb/projects/art/art-corpus/): 225 (265 is reported in one paper?) papers manually annotated with CISP concepts (ART Corpus > 1 million words, 35,040 sentences). These papers cover topics in physical chemistry and biochemistry and were provided by the Royal Society of Chemistry (RSC) Publishing. (CC-BY-NC)

- [Multi-CoreSC CRA corpus](http://www.sapientaproject.com/links#multi-coresc-cra-corpus-mccra): similar to the above ART/CoreSC Corpus but on cancer risk assessment, 50 articles. 

- [SciARG](https://github.com/LaSTUS-TALN-UPF/SciARG): argumentative quality assessment in scientific abstracts

- [PHAEDRA corpus](http://www.nactem.ac.uk/PHAEDRA): semantically annotated corpus for pharmacovigilence (597 MEDLINE abstracts)  

- [Meta-knowledge_GENIA_Corpus](http://www.nactem.ac.uk/meta-knowledge/download.php): a version of the entire GENIA event corpus, which has been enriched with meta-knowledge annotation, including on relative certainty of the events. 

We mapped the classes from these datasets as follow: 

- ART/CoreSC and Multi-CoreSC CRA corpus: conceptualisation zone from the CoreSC scheme "hypothesis" ("A statement not yet confirmed rather than a factual statement"), ART corpus: 656 sentences out of 34,680, Multi-CoreSC CRA: 152 sentences out of 8,501

- SciARG: "motivation_hypothesis" annotation class, for the main hypothesis the authors want to corroborate through the described work

- PHAEDRA corpus: from the "Interpretative attributes" annotations relative the events, "Speculated" event and "Potential_therapeutic_effect" could be considered as "hypothesis". "Potential_therapeutic_effect" is usually a claim that is discussed in the article, for which some new knowledge is reported. 

- Meta-knowledge_GENIA_Corpus: event annotation "Certainty Level" L1 (medium to huge uncertainty) are hypothetical event, and L2 (some degree of uncertainty or event takes place most but not all of the time) might correspond to hypotheses but not systematically, so we decided to exclude these L2 sentences entirely.

TBD: analyze the AbstRCT corpus.

## Statistics

Based on the described mapping and a combination of the datasets, we arrive to the following statistics for the "Frankenstein" hypothesis dataset: 


| corpus               | Level   | Hypothesis sentences | Non-hypothesis sentences | total        | 
|---                   |---      |---                   |---                       |---           |
| ART/CoreSC           |full-text| 656 (1.9%)           | 34024 (98.1%)            | 34680 (100%) |
| Multi-CoreSC CRA     |full-text| 152 (1.8%)           | 8349 (98.2%)             | 8501 (100%)  |
| SciARG               | abstract| 48 (1.2%)            | 3938 (98.8)              | 3986 (100%)  |
| PHAEDRA              | abstract| -                    | -                        | -            |
| Meta-knowledge_GENIA | abstract| 442 (5.5%)           | 7559 (94.5%)             | 8501 (100%)  |
| __aggregated__       | mixed   | __1298 (2.4%)__      | __53870 (97.6%)__        | __55168 (100%)__ |

The results in a significantly unbalanced corpus, with a minority class represented in less than 3% of the sentences. 

Note that the inter-annotator agreement with Cohen's Kappa for SciARG for instance is 0.59 (all annotations), which can be interpreted as "moderate" aggreement.
