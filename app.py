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
    
    print(request.method)
    mid = (57.057007632597355, 10.177105367389393)
    print('lat:', mid[0]*1E7,'lon:', mid[1]*1E7)
    print(int(round(mid[0]*1E7))/1E7, int(round(mid[1]*1E7))/1E7)
    coortest = [
        {'event_id':1, 'symbol':'$', 'x':30, 'y':30},
        {'event_id':2, 'symbol':'&', 'x':50, 'y':50},
        {'event_id':3, 'symbol':'£', 'x':10, 'y':10}
        ]
    return render_template('index.html', image='static/world_folder/world1/world1_map.png', world=coortest, req=req)

if __name__ == '__main__':
    app.run(debug=True)