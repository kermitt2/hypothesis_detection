import os
import lxml
import argparse
from lxml import etree
import re
import json
import csv
from blingfire import text_to_sentences

"""

Simple script to parse and assemble datasets with relevant annotations
regarding hypotheses. 

"""

art_corpus_path = "dataset/external/ART_Corpus"
mk_genia_path = "dataset/external/Meta-knowledge_GENIA_Corpus/Corpus"
mcsc_cra_path = "dataset/external/Multi-CoreSC_CRA_corpus"
phaedra_path = "dataset/external/PHAEDRA_corpus"
sciarg_path = "dataset/external/SciARG"

def process_art(output, corpus_name="art"):
    """
    CoreSC scheme `hypothesis`, noted `type="Hyp"` in XML.

    It covers also the Multi-CoreSC_CRA_corpus which has the same format
    """

    # traverse root directory and subdirectories to fish XML files
    if corpus_name == "art":
        root_path = art_corpus_path
    elif corpus_name == "mcsc_cra":
        root_path = mcsc_cra_path
    else:
        print("Invalid corpus name: ", corpus_name)
        return

    corpus = []
    nb_sentences = 0
    nb_hypothesis_sentences = 0

    for (dirpath, dirnames, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.xml'): 
                try:
                    tree = etree.parse(os.path.join(dirpath,filename))
                except:
                    print("XML parsing error with", filename)
                for sentence in tree.xpath(".//s"):
                    texts = sentence.xpath(".//text()")
                    text = " ".join(texts)
                    text = text.replace("\n", " ")
                    text = text.replace("\t", " ")
                    text = re.sub(r'( )+', ' ', text.strip())
                    text = text.strip()
                    unit = {}
                    unit["text"] = text
                    nb_sentences += 1

                    # check the sentence type which is in an empty element <CoreSc1 atype="GSC" type="Hyp"/>
                    # don't ask me why they put this mixed with the text !
                    coreSc1Types = sentence.xpath(".//CoreSc1/@type")
                    if len(coreSc1Types) == 0:
                        coreSc1Types = sentence.xpath(".//annotationART/@type")
                    if "Hyp" in coreSc1Types or "HYP" in coreSc1Types:
                        unit["class"] = "hypothesis"
                        nb_hypothesis_sentences += 1
                    else:
                        unit["class"] = "not_hypothesis"
                    corpus.append(unit)

    # simple report 
    percentage_hypothesis = round(float(nb_hypothesis_sentences*100) / nb_sentences, 1)
    percentage_non_hypothesis = round(float((nb_sentences-nb_hypothesis_sentences)*100) / nb_sentences, 1)
    print(corpus_name, "corpus - hypothesis sentences:", str(nb_hypothesis_sentences), "("+str(percentage_hypothesis) + 
        "%), non hypothesis sentences:", str(nb_sentences-nb_hypothesis_sentences), "("+str(percentage_non_hypothesis)+"%), total", str(nb_sentences))

    if len(corpus)>0:
        with open(os.path.join(output, corpus_name+".json"), "w") as outfile:
                outfile.write(json.dumps(corpus, indent=4))
    
    return corpus

def process_mk_genia(output):
    """
    event annotation `Certainty Level` L1 (medium to hugh uncertainty) are hypothetical 
    event, and L2 (some degree of uncertainty or event takes place most but not all of the time) 
    might correspond to hypotheses but not systematically, so we decided to exclude these L2 
    sentences entirely.
    
    XML corpus, attribute @CL="L1" on event element 
    """
    corpus = []
    root_path = mk_genia_path
    nb_sentences = 0
    nb_hypothesis_sentences = 0

    for (dirpath, dirnames, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.xml'): 
                try:
                    tree = etree.parse(os.path.join(dirpath,filename))
                except:
                    print("XML parsing error with", filename)
                for sentence in tree.xpath(".//sentence"):
                    texts = sentence.xpath(".//text()")
                    text = " ".join(texts)
                    text = text.replace("\n", " ")
                    text = text.replace("\t", " ")
                    text = re.sub(r'( )+', ' ', text.strip())
                    text = text.strip()
                    unit = {}
                    unit["text"] = text
                    unit["class"] = "not_hypothesis"
                    toKeep = True

                    # get next sister elements as it is an element <event>
                    sisters = sentence.xpath("./following-sibling::*")
                    if sisters == None or len(sisters) == 0:
                        continue

                    for sister in sisters:
                        if sister.tag != "event":
                            break

                        certaintyLevels = sister.xpath("./@CL")
                        if len(certaintyLevels)>0 and certaintyLevels[0] == "L1":
                            unit["class"] = "hypothesis"
                            nb_hypothesis_sentences += 1
                            toKeep = True
                            break

                        if len(certaintyLevels)>0 and certaintyLevels[0] == "L2":
                            toKeep = False

                    if toKeep:
                        nb_sentences += 1
                        corpus.append(unit)

    # simple report 
    percentage_hypothesis = round(float(nb_hypothesis_sentences*100) / nb_sentences, 1)
    percentage_non_hypothesis = round(float((nb_sentences-nb_hypothesis_sentences)*100) / nb_sentences, 1)
    print("mk_genia corpus - hypothesis sentences:", str(nb_hypothesis_sentences), "("+str(percentage_hypothesis) + 
        "%), non hypothesis sentences:", str(nb_sentences-nb_hypothesis_sentences), "("+str(percentage_non_hypothesis)+"%), total", str(nb_sentences))

    if len(corpus)>0:
        with open(os.path.join(output, "mk_genia.json"), "w") as outfile:
                outfile.write(json.dumps(corpus, indent=4))
    
    return corpus

def process_phaedra(output):
    """
    `Speculated` event and `Potential_therapeutic_effect` could be considered as hypothesis

    Parsing is more complicated because annotations are distributed in several files each time and has a 
    spagetti format
    """
    corpus = []
    root_path = phaedra_path
    nb_sentences = 0
    nb_hypothesis_sentences = 0

    for (dirpath, dirnames, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.txt') and filename != "README.txt": 
                with open(os.path.join(dirpath,filename), "r") as the_file:
                    full_text = the_file.read()
                    # we have one sentence per line, but need the whole text for offsets 

                annotation_filename = filename.replace('.txt', '.a1')
                components = {}
                # get components, we store them in a map to retrieve offsets
                with open(os.path.join(dirpath,annotation_filename), "r") as the_file:
                    lines = the_file.readlines()
                    for line in lines:
                        line = line.strip()
                        #pieces = line.split("\t")
                        pieces = re.split(" |\t", line)
                        component_id = pieces[0]
                        if pieces[2].isdigit() and pieces[3].isdigit():
                            offsets = [ int(pieces[2]), int(pieces[3]) ]
                            components[component_id] = offsets
                
                annotation_filename = filename.replace('.txt', '.a2')
                # get the component possibly associated to an hypothesis, get the offset of this component, 
                # then the sentence
                with open(os.path.join(dirpath,annotation_filename), "r") as the_file:
                    lines = the_file.readlines()
                    for line in lines:
                        line = line.strip()
                        pieces = re.split(" |\t", line)
                        component_id = pieces[0]

                        if len(pieces)>=4 and pieces[2].isdigit() and pieces[3].isdigit():
                            offsets = [ int(pieces[2]), int(pieces[3]) ]
                            components[component_id] = offsets

                        if pieces[0].startswith("E"):
                            # if we have an event, we can also index the event by the offset of its main term
                            sub_component = pieces[1][pieces[1].find(":")+1:]
                            if sub_component in components:
                                offset = components[sub_component]
                                components[pieces[0]] = offsets

                consumed_sentences = []
                with open(os.path.join(dirpath,annotation_filename), "r") as the_file:
                    lines = the_file.readlines()
                    for line in lines:
                        line = line.strip()
                        pieces = re.split(" |\t", line)
                        if pieces[1] == "Speculated":
                            if pieces[2] in components:
                                offset = components[pieces[2]]
                                local_sentence = get_sentence(full_text, offset)
                                if local_sentence != None and len(local_sentence)>0:
                                    local_sentence = local_sentence.strip(" \t\n")
                                    if local_sentence in consumed_sentences:
                                        continue 
                                    unit = {}
                                    unit["text"] = local_sentence.strip(" \t\n")
                                    consumed_sentences.append(local_sentence)
                                    unit["class"] = "hypothesis"
                                    nb_hypothesis_sentences += 1
                                    corpus.append(unit)

                        '''
                        if pieces[1].startswith("Potential_therapeutic_effect"):
                            if pieces[1].find(":") != -1:
                                sub_component = pieces[1][pieces[1].find(":"):]
                                if sub_component in components:
                                    offset = components[sub_component]
                                    local_sentence = get_sentence(full_text, offset)
                                    if local_sentence != None:
                                        unit = {}
                                        unit["text"] = local_sentence
                                        unit["class"] = "hypothesis"
                                        corpus.append(unit)
                            elif pieces[0] in components:
                                offset = components[pieces[0]]
                                local_sentence = get_sentence(full_text, offset)
                                if local_sentence != None:
                                    unit = {}
                                    unit["text"] = local_sentence
                                    unit["class"] = "hypothesis"
                                    corpus.append(unit)
                        '''
                # finally, not null sentences not hypothesis are stored too

    if len(corpus)>0:
        with open(os.path.join(output, "phaedra.json"), "w") as outfile:
                outfile.write(json.dumps(corpus, indent=4))

    return corpus

def get_sentence(text, offsets):
    """
    Given a multi-line text where we have one sentence per line, return the sentence 
    containing indicated offsets
    """
    sentences = text.split("\n")
    pos = 0
    for sentence in sentences:
        if pos <= offsets[0] and offsets[1] <= pos+len(sentence):
            # we might have several sentence by lines actually (e.g. Phaedra), so we can
            # refine with blingfire
            someSentences = text_to_sentences(sentence).split("\n")
            if len(someSentences) == 1:
                return sentence
            else:
                # refine by offset once again
                subPos = pos
                for someSentence in someSentences:
                    if subPos <= offsets[0] and offsets[1] <= subPos+len(someSentence):
                        return someSentence
                    else:
                        subPos += len(someSentence) + 1
        else:
            # +1 because of end of line character
            pos += len(sentence) + 1
    return None

def process_sciarg(output):
    """
    We have the `motivation_hypothesis` annotation class, which corresponds to hypothesis.

    This is based on simple tsv files
    """
    corpus = []
    root_path = sciarg_path
    nb_sentences = 0
    nb_hypothesis_sentences = 0

    for (dirpath, dirnames, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.tsv') and dirpath.find("single") != -1: 
                with open(os.path.join(dirpath,filename)) as file:
                    tsv_stuff = csv.reader(file, delimiter="\t")
                    start = True
                    for row in tsv_stuff:
                        if start:
                            start = False
                            continue
                        text = row[12]
                        unit = {}
                        unit["text"] = text
                        if row[5] == "motivation_hypothesis":
                            unit["class"] = "hypothesis"
                            nb_hypothesis_sentences += 1
                        else:
                            unit["class"] = "not_hypothesis"
                        nb_sentences += 1
                        corpus.append(unit)

    # simple report 
    percentage_hypothesis = round(float(nb_hypothesis_sentences*100) / nb_sentences, 1)
    percentage_non_hypothesis = round(float((nb_sentences-nb_hypothesis_sentences)*100) / nb_sentences, 1)
    print("SciARG corpus - hypothesis sentences:", str(nb_hypothesis_sentences), "("+str(percentage_hypothesis) + 
        "%), non hypothesis sentences:", str(nb_sentences-nb_hypothesis_sentences), "("+str(percentage_non_hypothesis)+"%), total", str(nb_sentences))

    if len(corpus)>0:
        with open(os.path.join(output, "sciarg.json"), "w") as outfile:
                outfile.write(json.dumps(corpus, indent=4))

    return corpus

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converter for datasets into json")
    parser.add_argument("--output", default="dataset/combined", type=str, help="path where all the assemble JSON file will be written")
    parser.add_argument("--corpus-type", default=None, type=str, help="type of input corpus, if none all the datasets will be converted and assembled")
    
    args = parser.parse_args()
    output = args.output
    corpus_type = args.corpus_type

    if os.path.exists(output) and not os.path.isdir(output):
        print("The output path is not valid, because it is a file:", output)
        exit()

    if not os.path.exists(output):
        os.makedirs(output)

    if corpus_type == None:
        corpus = process_art(output)
        corpus += process_mk_genia(output)
        corpus += process_art(output, "mcsc_cra")
        corpus += process_phaedra(output)
        corpus += process_sciarg(output)
        # write combined corpus
        with open(os.path.join(output, "frankenstein.json"), "w") as outfile:
            outfile.write(json.dumps(corpus, indent=4))
    elif corpus_type == 'art':
        process_art(output)
    elif corpus_type == 'mk_genia':
        process_mk_genia(output)
    elif corpus_type == 'mcsc_cra':
        process_art(output, "mcsc_cra")
    elif corpus_type == 'phaedra':
        process_phaedra(output)
    elif corpus_type == 'sciarg':
        process_sciarg(output)
