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


@app.route('/ner', methods=['GET'])
def ner():
    global nlp
    print("classify")
    req_data = request.get_json(force=True, silent=True)
    if req_data is None:
        return 'bad request', 400

    if nlp is None:
        load_model()
    payload = str(req_data['payload'])
    doc = nlp(payload)
    return [(ent.text, ent.label_) for ent in doc.ents]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
