from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('site_template.html')

@app.route('/map', methods=['GET', 'POST'])
def show_map():
    req = 'request'
    if request.method == 'POST':
        event = request.form.get('event')
        req = event
    
    
    coortest = [
        #{'event_id':1, 'symbol':'$', 'x':97, 'y':97},
        #{'event_id':2, 'symbol':'&', 'x':0, 'y':0},
        {'event_id':3, 'symbol':'£', 'x':50, 'y':50}
        ]
    return render_template('index.html', image='static/world_folder/world1/world1_map.png', world=coortest, req=req)

if __name__ == '__main__':
    app.run(debug=True)