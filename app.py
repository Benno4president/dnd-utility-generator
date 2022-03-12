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
    
    coortest = [
        {'symbol':'$', 'x':100, 'y':100},
        {'symbol':'&', 'x':50, 'y':50},
        {'symbol':'£', 'x':10, 'y':20}
        ]
    return render_template('index.html', image='/static/images/test_map.png', world=coortest, req=req)

if __name__ == '__main__':
    app.run(debug=True)