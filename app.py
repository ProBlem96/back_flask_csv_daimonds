from help.test import load_csv,save_csv, CSV_FILE
from flask import Flask,request ,jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


df = pd.read_csv(CSV_FILE)


@app.route("/", methods=['GET'])
def start_site():
    daimonds = load_csv()
    print(daimonds)
    save_csv(daimonds)
    return daimonds

@app.route("/max", methods=['GET'])
def max_price():
    ar = []
    max_price = df['price'].max()
    ar.append(int(max_price))
    return ar

@app.route("/avg", methods=['GET'])
def mean_price():
    ar = []
    mean_price = df['price'].mean()
    ar.append(int(mean_price))
    return ar

@app.route("/ideal", methods=['GET'])
def count_ideal():
    ar = []
    ideal_count = df[df['cut']=='Ideal'].shape[0]
    ar.append(int(ideal_count))
    return ar

@app.route("/premium", methods=['GET'])
def count_premium():
    ar = []
    premium_carats = df[df['cut'] == 'Premium']['carat']
    median_carat = premium_carats.median()
    ar.append(str(median_carat))
    return ar

@app.route("/avgcut", methods=['GET'])
def avg_carat():
    ar = []
    cut_carat_avg = df.groupby('cut')['carat'].mean()
    # method to convert the DataFrame "cut_carat_avg" to a JSON string
    ar.append(str(cut_carat_avg))
    return ar

@app.route("/color", methods=['GET'])
def color_price_avg():
    ar = []
    color_price_avg = df.groupby('color')['price'].mean()
    ar.append(str(color_price_avg))
    return ar



@app.route("/add", methods=['POST'])
def add_daimond():
    data = request.get_json()
    global df
    last_row = df.tail(1)
    last_id = int(last_row.ID)
    new_id = last_id + 1
    data["ID"] = new_id
    df = df.append(data, ignore_index=True)
    df.dropna(inplace=True)
    df.to_csv(CSV_FILE, index=False)
    return data



@app.route("/upd_daimond", methods=['PUT'])
def update_daimond():
    daimonds = load_csv()
    data = request.get_json()
    found = False
    for i,daim in enumerate(daimonds):
        if daim["ID"] == data["ID"]:
            daimonds[i]["carat"] = data["carat"]
            # print(daimonds[i]["carat"]) 
            found = True
            break
    if found is False:
        return { "error": "daimond not found" }
    save_csv(daimonds)
    return daimonds




@app.route("/del_daimond/<int:id>", methods=['DELETE'])
def delete_daimond(id):
    global df 
    df = df[df.ID != id]
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"message": "Daimond deleted"})



if __name__ == '__main__':
    app.run(debug=True)