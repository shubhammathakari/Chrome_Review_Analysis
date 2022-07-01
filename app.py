# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import pandas as pd
import re
from textblob import TextBlob
app = Flask(__name__)
data=request.form['df']
df = pd.read_csv("data.csv")
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/',methods=["POST"])
def clean(text):
    text_c= re.sub('[^a-zA-Z]',' ',text)
    return text_c

df["Text"] = [clean(x) for x in df['Text']]

df['polarity_t'] = df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

df1 = df[["ID","Text","Star","polarity_t"]]

def assign(x):
    if x>0:
        return "Positive"
    elif x == 0:
        return "Neutral"
    else:
        return "Negative"
    
df1['polarity_t']=df['polarity_t'].apply(assign)

result = df1[(df1.polarity_t == "Positive") & (df1.Star == 1)]
result = result.append(df1[(df1.polarity_t == "Positive") & (df1.Star == 2)])


render_template('index.html', final_result=result)

if __name__ == "__main__":
    app.run(debug=True)

