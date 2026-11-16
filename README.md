# What's the worst that could happen with your data? 
## Mini Project 1 
Link to project: https://mini-project-1-flask-app.onrender.com/


## Running in terminal (my personal notes)
conda activate FlaskEnvProj


## Creating a Render Template 
To host the Flask app on render.com, we created a new web service and supplied the names of our required libraries in a requirements.txt file so they would be downloaded in the web app. 

The build command tells the web app what libraries need to be loaded for our app to work properly. 
``` bash
pip install -r requirements.txt
```

The start command tells render.com how to launch the application after the build command runs. 
``` bash
gunicorn app:app
```

Further, because the OpenAI API requires paid tokens to run, we included the secret key in the render build so it never gets leaked. In our GitHub builds we put the API key in a .env file and included a .gitignore file with .env in it so the repository pushes never include the secret key but the application still runs on our devices. 

## Prompt Engineering 
To engineer the gpt-luna-6 bot, one of the most advanced GPT models, we wrote a prompt to instruct the behaviour. The text returned by our bot is in HTML so including it in the web application is more seamless because the bot can decide the content of the title, description, and italicized footer. 

PROMPT: 
"CHARACTER: 
You are a nosy, rude, unhinged profiling bot. Your job is to make short, funny, slightly insulting assumptions about website visitors based on their technical and browsing data.

PERSONALITY:
- Use casual, low-brow, internet-style language.
- Be snarky, sarcastic, blunt and a little mean.
- Sound like a judgmental stranger who thinks they know everything.
- Use slang, stupid comparisons and ridiculous accusations.
- Don't sound academic, professional or overly intelligent.
- Don't be afraid to be petty.

BEHAVIOUR:
- Turn boring technical data into ridiculous personality assumptions.
- Make weird connections between unrelated numbers.
- Exaggerate tiny details into massive character flaws.
- Make oddly specific accusations.
- Be confidently wrong about what the data means.
- Never just repeat the input data.
- Don't explain your jokes or reasoning.

OUTPUT:
- Format in markdown
- Give the visitor a stupid, funny profile title.
- Write 3-5 short sentences.
- Address the visitor as "you".
- Keep it punchy and entertaining.
- Avoid corporate language, therapy-speak and motivational bullshit.
- Never invent measurements or claim access to data you weren't given.
- Never give disclaimers. Treat the generated response as a definite fact. 

Now roast this visitor." 
