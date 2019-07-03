from flask import Flask,render_template,jsonify,json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Condor_overall_status.html')

@app.route('/ajax/get_tc_status')
def get_tc_status():
    with open('./resource/data_2.json','r') as f:
        data = json.load(f)
        print(data)
    return jsonify(data=data)


@app.route('/test_case')
def test_case_status():
    return render_template('dt.html')


@app.route('/bg')
def bg():
    return render_template('bg.html')


@app.route('/<file_name>')
def specify_index(file_name):
    return render_template('{}.html'.format(file_name))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')