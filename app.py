import pandas as pd
from flask import Flask, render_template,request
app = Flask(__name__)
import pickle
import joblib
from sqlalchemy import create_engine
model = pickle.load(open("mlr_pipeline.pkl",'rb'))
#model = pickle.load(open("profit.pkl",'rb'))
#ct = joblib.load('column1')
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",# user
                               pw="dba123", # passwrd
                               db="amerdb")) #database
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST' :
        f = request.files['file']
        data = pd.read_csv(f)

        #data1 = data.to_numpy()
        # Perform PCA using the saved model
        y2 = pd.DataFrame(model.predict(data),columns=['MPG'])

        data['MPG'] = y2
        data.to_sql('mpg_predictons', con = engine, if_exists = 'replace', chunksize = 1000, index= False)
        return render_template("data.html", Z = "Your results are here" , Y = data.to_html())

if __name__ == '__main__':

    app.run(debug = True)

                           #@app.route('/user')
#def user ():
   # return "hellow user welcome"
