from flask import Flask,render_template,jsonify,json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cmcc_minfadian.html')


@app.route('/test')
def index2():
    return render_template('index2.html')

@app.route('/ajax/get_tc_status')
def get_tc_status():
    data = {
  "data": [
    [
      "Tiger Nixon",
      "System Architect",
      "Edinburgh",
      "5421",
      "2011/04/25",
      "$320,800"
    ],
    [
      "Garrett Winters",
      "Accountant",
      "Tokyo",
      "8422",
      "2011/07/25",
      "$170,750"
    ]]}
    return jsonify(data)

@app.route('/ajax/get_cmcc_status')
def get_cmcc_mingfadian():
  with open('answer.json','r') as f:
    data = json.load(f)
  return jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')