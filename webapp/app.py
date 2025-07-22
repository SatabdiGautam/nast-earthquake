from flask import Flask 

app= Flask(__name__)

@app.route('/')
def home():
    name = "Downloading earthquake data from USGS and raspberryshake"
    return name

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=int("3050"),debug=True)