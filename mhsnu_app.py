import pandas as pd
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load("mh_snu_dac1.pkl")

@app.route('/')
def hi():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print(request.form.values())
    inp = [i for i in request.form.values()]

    try :
        for r in range(0,4) :
            if not isinstance(int(inp[r]), int):
                mess = "Please enter valid input"
                return render_template('index.html', prediction = mess)
    except :
        mess = "Please enter valid input"
        return render_template('index.html', prediction = mess)

    test = {"Item_ID":inp[0],
            "Item_W":inp[1],
            "Item_Type":inp[2],
            "Item_MRP":inp[3],
            "Outlet_ID":inp[4],
            "Outlet_Year":inp[5],
            "Outlet_Size":inp[6],
            "Outlet_Type":inp[7]
            }
    print(test)
    test_cols =['Item_ID', 'Item_W', 'Item_Type', 'Item_MRP', 'Outlet_ID','Outlet_Year', 'Outlet_Size', 'Outlet_Location_Type']
    test_df = pd.DataFrame([test],columns=test_cols)
    print(test_df)
    res = model.predict(test_df)
    print(res[0])
    #return str(res[0])
    if isinstance(res[0], float):
        mess = "Predicted Sales is {} ".format(str(res[0]))
    else:
        mess = "Please enter valid input"
    return render_template('index.html', prediction = mess)

if __name__ == "__main__":
    app.run(debug = True)