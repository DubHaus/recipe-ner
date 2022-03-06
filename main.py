import os

import spacy
from flask import Flask
from flask import request

app = Flask(__name__)

nlp = None


def load_model():
    global nlp
    model_dir = "./model/model-best"
    print("loading from {}".format(model_dir))
    nlp = spacy.load(model_dir)


@app.route('/', methods=['GET'])
def ner_get():
    global nlp
    data = request.args.get('str')
    print(data)

    if nlp is None:
        load_model()
    doc = nlp(data)
    return {"recipes": [(ent.text, ent.label_) for ent in doc.ents]}



@app.route('/', methods=['POST'])
def ner_post():
    global nlp
    data = request.get_json()
    print(data)

    if nlp is None:
        load_model()
    doc = nlp(data["str"])
    return {"recipes": [(ent.text, ent.label_) for ent in doc.ents]}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
