from flask import *  
import pandas as pd
import os
from os.path import join, dirname, realpath
app = Flask(__name__)  
 
# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Here we upload file
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html") 



@app.route('/uploadFiles', methods = ['POST'])  
def uploadFiles():
      # get the uploaded file
      
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      return render_template('date.html')


# Get date range data from uploaded csv file 
@app.route('/getData',methods=['POST'])
def getData():
    if request.method=='POST':
        Start_Date=request.form['sdate']
        End_date=request.form['edate']
        dateset=pd.read_csv(UPLOAD_FOLDER+'/data.csv')
        mask=(dateset['timestamp']>=Start_Date)&(dateset['timestamp']<=End_date)
        Dates=dateset['timestamp'].loc[mask]
        Objects=dateset['objects_detected'].loc[mask]
        Image=dateset['image_name'].loc[mask]
        pairs=[(date,objects,image) for date,objects,image in zip(Dates,Objects,Image)]
        
    return render_template('form.html',pair=pairs)
if __name__ == '__main__':  
    app.run(debug = True)  
