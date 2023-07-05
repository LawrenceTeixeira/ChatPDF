from flask import Flask, render_template, request
from autocorrect import spell
from functions import LoadPDF, Query

app = Flask(__name__)

#BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
#k = aiml.Kernel()

#book_docsearch = LoadPDF()

#if os.path.exists(BRAIN_FILE):
#    print("Loading from brain file: " + BRAIN_FILE)
 #   k.loadBrain(BRAIN_FILE)
#else:
#    print("Parsing aiml files")
#    k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
#    print("Saving brain file: " + BRAIN_FILE)
#    k.saveBrain(BRAIN_FILE)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')

    response = Query(query, book_docsearch)
    if response:
        return (str(response))
    else:
        return (str(":)"))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=8080)


