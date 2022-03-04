from pathlib import Path
import json
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

nlp = spacy.blank("en")  # load a new spacy model
db = DocBin()  # create a DocBin obj

f = open('./data/dataset.json')
TRAIN_DATA = json.load(f)


def main():
    # prepare training data
    prepare_data(TRAIN_DATA[0:4500], './data/training_data.spacy')
    # prepare validation data
    prepare_data(TRAIN_DATA[4500:], './data/validating_data.spacy')


def prepare_data(data, output):
    for text, annot in tqdm(data):
        doc = nlp.make_doc(text)

    ents = []

    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label,
                             alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

    db.to_disk(output)  # save the docbin object


if __name__ == "__main__":
    main()
