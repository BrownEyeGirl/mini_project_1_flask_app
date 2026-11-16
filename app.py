import os, shutil, psutil
from flask import Flask, render_template, jsonify, request, session
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

app = Flask(__name__)


# 1. Load the variables from the .env file into the environment
load_dotenv()

# 2. Initialize the OpenAI client (it automatically reads OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# needed to sign the session cookie ( uses a placeholder like this for testing)
app.secret_key = 'BAD_SECRET_KEY'

# build the info dictionary: this visitor's session values + live system stats
def read():
    info = {
        "clicks": session.get("clicks", 0),
        "tab_leaves": session.get("tab_leaves", 0),
        "first_visit": session.get("first_visit"),
        "city": session.get("city"),
        "region": session.get("region"),
        "org": session.get("org"),
    }

    # live stats are not saved, they are measured fresh each time
    info.update({
        "ram_free_gb": round(psutil.virtual_memory().available / 1e9, 1), # turns into gb and rounds to nearest 10th 
        "ram_total_gb": round(psutil.virtual_memory().total / 1e9, 1), # ''
        "disk_free_gb": round(shutil.disk_usage(os.path.expanduser("~")).free / 1e9, 1),
        "disk_total_gb": round(shutil.disk_usage(os.path.expanduser("~")).total / 1e9, 1),
    })
    return info

@app.route("/")
def index():
    # first visit from THIS browser, only saved once
    if "first_visit" not in session:
        session["first_visit"] = datetime.now().isoformat(timespec="seconds")

    return render_template("index.html", info=read())

# add one to an event (clicks or tab_leaves), store in the session, return totals
@app.route("/log", methods=["POST"])
def log():
    event = (request.get_json(silent=True) or {}).get("event")
    if event in ("clicks", "tab_leaves"):  # ignore anything else
        session[event] = session.get(event, 0) + 1
    return jsonify(read())

# read-only route for the buttons (does not count as a click)
@app.route("/info")
def info_route():
    return jsonify(read())


# the page looks up its location once on load and posts it here to store in the session
@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()
    session["city"] = data["city"]
    session["region"] = data["region"]
    session["org"] = data["org"]

    return jsonify(read())


@app.route("/prompt")
def profile(): 
    context = request.args.get("context", "")   # "" if none was sent
    response = client.responses.create(
        model="gpt-6-luna", # small depreciated model 
        instructions="""
            CHARACTER: 
            You are a nosy, rude, unhinged profiling bot. Your job is to make short, funny, slightly insulting assumptions about website visitors based on their technical and browsing data.

            PERSONALITY:
            - Use casual, low-brow, internet-style language.
            - Be snarky, sarcastic, blunt and a little mean.
            - Sound like a judgmental stranger who thinks they know everything.
            - Use slang, stupid comparisons and ridiculous accusations.
            - Don't sound academic, professional or overly intelligent.
            - Don't be afraid to be petty.

            BEHAVIOUR:
            - Base your response on the context provided, use exact numbers or locations provided.  
            - Turn boring technical data supplied in into ridiculous personality assumptions.
            - Make weird connections between unrelated numbers.
            - Exaggerate tiny details into massive character flaws.
            - Make oddly specific accusations.
            - Be confidently wrong about what the data means.
            - Never just repeat the input data.
            - Don't explain your jokes or reasoning.

            OUTPUT:
            - Format in basic html, with h1 title, p info, and <b> or <br> when applicable. 
            - Give the visitor a stupid, funny profile title.
            - Write 3-5 short sentences.
            - Address the visitor as "you".
            - Keep it punchy and entertaining.
            - Avoid corporate language, therapy-speak and motivational bullshit.
            - Never invent measurements or claim access to data you weren't given.
            - Never give disclaimers. Treat your generated response as a definite fact. 

            Now roast this visitor.
        """,
        input= f"Use the context to formulate your response: {context}"
    )
    return response.output_text


if __name__ == "__main__":
    app.run(debug=True, port=1111) # change port if its not loading, sometimes it glitches.