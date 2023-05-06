# Notes

Few papers are really addressing hypothesis recognition in scientific articles. Most research are rather interested in hypothesis generation (for example drug repurposing hypotheses) or "questions/problems" seen as hypothesis for textual entailment (find the passage in an article that entails a question view as an hypothesis). 

For the research really on hypothesis recognition, there are different definitions for what is an hypothesis (as you pointed out when we discussed). Some work consider hypothesis as the main goal/problem of a research paper "the problem statement" - so usually a single one in the abstract. It seems harder to find approaches on hypotheses at lower grained within research papers, but clearly there could be multiple hypothesis expressed in a paper at different stage of the work description - for example 5 to 10 seems quite common. 

Some work associate "hypothesis" as part of the "argument" recognition, trying to annotate scientific articles to identify its the flow of arguments. Hypotheses here are one of the discursive function involved in scientific argumentation.

For practical experiments, here are a couple of datasets relevant to the question:

## Relevant Datasets

- ART Corpus: "conceptualisation zones" in scientific articles, annotations are following the CoreSC scheme, which includes a category "hypothesis" ("A statement not yet confirmed rather than a factual statement"), in the domains of chemistry and biochemistry. 

- Multi-CoreSC CRA corpus: similar to above ART/CoreSC Corpus on cancer risk assessment.

- AbstRCT corpus: argumentative annotations (Randomized Controlled Trial Abstracts), annotates "claims" (premises) and "major claims" (concluding statements)

- SciARG: argumentative quality assessment in scientific abstracts, it includes a "motivation-hypothesis" annotation class, for the main hypothesis the authors want to corroborate through the described work

- Meta-knowledge GENIA corpus: the GENIA event corpus with additional annotations relative to assertion and uncertainty on the biomedical statements/events 

- PHAEDRA corpus: semantically annotated corpus for pharmacovigilence (597 MEDLINE abstracts), it has "Interpretative attributes" annotations relative the events, including a speculative attribute ("Potential_therapeutic_effect"/"Speculated")

These datasets would typically help to formalize and refine an hypothesis into entities/events and relations:  

- BioCause corpus: Biomedical corpora annotated with event-level information, it focuses on annotating causality relations between 2 events 

- CRAFT dataset: well-known dataset, it has concept annotations following Open Biomedical Ontologies (OBOs) and co-reference annotations

Also relevant somehow, the well-known dataset:

- PubMed 200k RCT dataset: 200,000 abstracts of randomized controlled trials with zone annotations in the following classes: background, objective, method, result, conclusion (based on existing authors subsections in the abstracts).


## References 

Some relevant prior work. 

- 10.1186/s12911-018-0639-1: Identification of research hypotheses and new knowledge from scientific literature. BMC medical informatics and decision making, 2018.
_[ Identify for relation/events "Research Hypothesis" and "New Knowledge". No extra annotated data shared (to be checked), simply using classifier on pre-defined "clues" (dictionary of words/phrases) for detection. ]_

- 10.1371/journal.pcbi.1003117: ‘HypothesisFinder:’ A Strategy for the Detection of Speculative Statements in Scientific Text, PLOS 2013. 
_[ Old school dictionary and automatic pattern recognition, some data share (some "clues" and hypothesis sentences). ]_

- 10.1109/ICSE-NIER.2019.00017: Mining Plausible Hypotheses from the Literature, 2019
_[ Crowdsourcing/communty based effort to curate the hypothesis data from papers. ]_

- The CISP Annotation Schema Uncovers Hypotheses and Explanations in Full-Text Scientific Journal Articles, ACL-HLT 2011. 
_[ Simply presents an annotation schema. ]_

- Causal Knowledge Extraction from Scholarly Papers in Social Sciences, 2020. 
_[ Very simplistic pattern matching to identify hypotheses in social science papers, very "dirty" code and no shared data. ]_

- Incorporating Zoning Information into Argument Mining from Biomedical Literature, LREC 2022. 
_[ Not covering hypotheses ]_

- Multi-label Annotation in Scientific Articles - The Multi-label Cancer Risk Assessment Corpus, LREC 2016
http://www.sapientaproject.com/wp-content/uploads/2016/05/LREC2016_Ravenscroft.pdf
Multi-CoreSC CRA corpus (similar to ART/CoreSC Corpus) on cancer risk assessment.
