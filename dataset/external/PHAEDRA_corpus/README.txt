PHAEDRA CORPUS README
=====================

1. DESCRIPTION
--------------

The PHAEDRA corpus is a semantically annotated corpus for pharmacovigilence (PV), consisting of 597 MEDLINE abstracts. Its fine-grained, multiple levels of annotation, added by domain-experts, make it a unique resource within the field, and aim to encourage the development/adaption of novel machine learning tools for extracting PV-related information from text. It is intended that such tools will lead to novel means of supporting curators to efficiently increase the coverage, consistency and completeness of the information in PV resources.

The corpus includes five different levels of information, which allow detailed information about drug effects to be encoded.

- Named entities that participate in the description of drug effects.
        - Some categories of named entities have been automatically linked to concept identifiers in domain-specific terminological resources through the application of an automatic normalisaton method.
- Events that encode descriptions of drug effects.
- Interpretative attributes assigned to events to denote whether the event is negated and/or speculated, and to indicate the severity of the interaction/effect.
- Binary relations between NEs, to encode enriched descriptions of certain event participants.
- Coreference relations between certain NEs, to allow the interpretation of event participants that are not fully described within the scope of the event-containing sentence.

For further details about the corpus, please see http://www.nactem.ac.uk/PHAEDRA/ and the following article:

Paul Thompson, Sophia Daikou, Kenju Ueno, Riza Batista-Navarro, Jun'ichi Tsujii and Sophia Ananiadou (2018). Annotation and Detection of Drug Effects in Text for Pharmacovigilance. Journal of Cheminformatics.


2. LICENCE
----------

The annotations in the PHAEDRA corpus were created at the National Centre for Text Mining (NaCTeM), School of Computer Science, University of Manchester, UK.
They are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.  (http://creativecommons.org/licenses/by-sa/4.0/).

PLEASE ATTRIBUTE NaCTeM WHEN USING THE CORPUS, AND PLEASE CITE THE FOLLOWING ARTICLE:

Paul Thompson, Sophia Daikou, Kenju Ueno, Riza Batista-Navarro, Jun'ichi Tsujii and Sophia Ananiadou (2018). Annotation and Detection of Drug Effects in Text for Pharmacovigilance. Journal of Cheminformatics, 10:37. 


3. CORPUS STRUCTURE
-------------------

The corpus is spilt into training, development and test sets. Each set is contained within a separate directory of the downloadable corpus ("train", "dev" and "test", respectively).


4. ANNOTATION FORMAT
-------------------

The downloadable corpus consists of:

- A set of annotation files, containing the manually-added annotations associated with each document file.
- A set of text files corresponding to the abstracts.

The text file and associated annotation files have the same base name, i.e., the PMIDs of the abstract.
Annotation file formats

Annotations are encoded in the BioNLP Shared Task 2013 format (http://2013.bionlp-st.org/file-formats).
Based on this format, there are two annotation files associated with each text file:

- "a1" files - encode information about entity annotations, event triggers and cues used to assign event attributes
- "a2" files - encode information about relation and event annotations.

4.1 a1 Files
------------

In a1 files, each line corresponds to one of the following:

- An NE mention
- A cue phrase annotated as evidence for the assignment of an event attribute
- A "Coreferring_mention" phrase, correponding to an event participant that is referenced using an anaphoric expression
- A link to a concept identifier in an external terminoogical resource.

A sample of lines encoding entity annotations and their links to concept identifiers is shown below:


T1      Disorder 0 18   Serotonin syndrome
N1      Reference T1 UMLS:C0024586	Serotonin syndrome
T2      Pharmacological_substance 49 59 citalopram
N1000 	Reference T2 MeSH:D015283	citalopram
T3      Pharmacological_substance 64 72 fentanyl
N1001 	Reference T3 MeSH:D005283	fentanyl
T4      Disorder 94 112 serotonin syndrome
N3      Reference T4 UMLS:C0024586	serotonin syndrome
T40     Subject 280 301 A 65-year-old patient
T51     Coreferring_mention 523 525	He
T59     Adverse_effect 1314 1325        development
T60     Speculation_cue 1305 1313       possible
T64     Disorder 1161 1168;1182 1186    chronic pain
N23 	Reference T64 UMLS:C0150055 chronic pain

There are two types of lines, beginning either with "T" or with "N"

- Lines beginning with "T" (text-bound annotations) consist of the following information:

    - A unique id for the annotation. By convention, this starts with T, followed by a numerical value.
    - A TAB character.
    - The semantic label assigned to the annotation. This is either:
        - The NE type (for NE annotations)
        - The label Coreferring_mention label anaphoric event participants
        - The cue type (for event attribute cue annotations). This can be "Speculation_cue", "Negation_cue" or "Manner_cue"
        - The character-based offsets of the annotated span in the corresponding text file. There are two formats for the offsets, depending on whether the annotated span consists of a single, continuous span or a discontinuous span, consisting of multiple, connected spans.
            - For continuous spans (as in the first eight lines in the sample above), there are two offsets, corresponding to the start and end offsets of the span. The first offset is separated by a space from the entity type label, and there is a space between the start and end offsets.
            - For discontinuous spans (as in the final line of the sample above), there are two or more pairs of start and end offsets, each separated by a semi-colon. Each pair of offsets corresponds to a part of the complete annotated span.
    - Another TAB character
    - The text covered by the annotated span in the corresponding text file.

- Lines beginning with "N" provide information about normalisations, i.e. links to concept IDs in terminological resources. They consist of the following information:

    - A unique id for the annotation. By convention, this starts with N, followed by a numerical value.
    - A TAB character.
    - The word "Reference"
    - The id of the NE annotation to which the normalisation applies
    - Information about the concept to which the NE has been normalised. This consists of:
        - The name of the terminological resource containing the specified concept. This is either "UMLS" (for disorders) or "MeSH" (for phamacological substances)
        - A colon
        - The unique concept identifier assigned to the NE within the specified resource
    - Another TAB character.
    - The text covered by the NE to which the concept ID has been assigned.

4.2 a2 Files
-------------

In a2 files, each line corresponds to one of the following:

- a relation annotation
- an event trigger
- information about event participants
- values of event attributes

The format of the lines varies according to the annotation type.

Relation annotations
--------------------

The same format is used to encode both the two binary relation types (i.e., Subject_Disorder and is_equivalent) and coreference annotations between anaphoric event participants and the NE to which they refer in neighbouring sentences.


R1  is_equivalent Arg1:T8 Arg2:T9
R4	Subject_Disorder Arg1:T32 Arg2:T33
R7	Coreference Arg1:T51 Arg2:T26

Each line consists of:

- A unique id for the relation annotation. By convention, this starts with R, followed by a numerical value.
- A TAB character.
- The Relation type label assigned to the annotation. This is either Subject_Disorder, is_equivalent or Coreference.
- Details of the two text spans that are linked in the relation. Each text span that is linked in a relation annotation is referred to as an argument. The first argument is denoted by the label "Arg1" and the second argument is denoted by the label "Arg2". In each case, the argument label is followed by a colon, and then by the ID of the corresponding text span (which corresponds to one of the T annotations introduced above).
     - is_equivalent relations link two NE spans of the same that refer to the same concept
     - In Subject_Disorder relations, Arg1 corresponds to the Subject annotation, and Arg2 corresponds to the Disorder.
     - In Coreference relations, Arg1 corresponds to the anaphoric Coreferring_mention annotation, and Arg2 corresponds to the NE to which the anaphoric expression refers

Event annotations
-----------------

There are three types of lines associated with event annotations, each having a different format. These are exemplified below:


T59     Adverse_effect 1314 1325        development
E10     Potential_therapeutic_effect:T40 affects:T22 has_subject:T41 has_agent:T20 has_cue:T42
E13 	Potential_therapeutic_effect:T48 has_agent:E14 has_subject:T42
A1      Speculated E12
A2      Negated E10
A5      Manner E8 High

- Lines beginning with "T" - These correspond to event trigger phrases. They have exactly the same format as the lines in a1 files (see above), except that the semantic label corresponds to an event type.
- Lines beginning with "E" - These lines link together event triggers, event participants and cues for event attribute assignment. Each such line consists of the the following:
    - A unique id for the event. By convention, this starts with E, followed by a numerical value.
    - A TAB character.
    - The event type, followed by a colon and then the id of the event trigger.
    - Information about event participants and cues for attribute assignment, each separated by a space. For each partiicpant/cue, the format is as follows:
        - The semantic role label assigned to the participant (or has_cue for attribute cues), followed by a colon
            - The id of the participant/cue.
                - For cues, the id will always start with a "T", corresponding the an annotation in the associated a1 files
                - For participants, the id may start with a "T" if the participant is an NE (the id will correspond to an annotation in the a1 file), or the participant may start with an "E" is the participant is itself an event (which is listed in the same a2 file)
- Lines beginning with "A" - These correspond to event attribute annotations. Note that these will only occur if a non-default value for one or more of the attributes has bee n assigned to the event. The lines have the following format:
    - A unique id for the attribute annotation. By convention, this starts with A, followed by a numerical value.
    - A TAB character.
    - The name of the attribute
    - The id of the event to which the attribute has been assigned
    - For the "Manner" attribute ONLY, the non-default value assigned to the attribute (i.e, either "High" or "Low"). For the binary-valued "Speculated" and "Negated" attributes, it is implicit that the value is True, since the annotation is not present if the attribute has the default value of False
