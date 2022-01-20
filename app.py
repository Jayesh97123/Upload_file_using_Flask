from flask import *  
import pandas as pd
import os
from os.path import join, dirname, realpath
import mysql.connector

app = Flask(__name__)  
 
# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="mysql",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
  print(x)

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
        li=list(Objects)
        new_list=[]
        for i in li:
          a=i.split(',')
          new_list.extend(a)
        new_list1=set(new_list)
        new_list1=list(new_list1)
        new_list2=new_list1
        # my data rows as dictionary objects
        final=[]
        # field names
        h=['object','count']
        for i in new_list2: 
          n=[]
          n.append(i)
          no=new_list.count(i)
          n.append(no)
          final.append(dict(zip(h,n)))
        # name of csv file
        filename='static/files/record.csv'
        # writing to csv file
        with open(filename,'w') as csvfile:
          # creating a csv dict writer object
          writer=csv.DictWriter(csvfile, fieldnames=h)
          # writing headers (field names)
          writer.writeheader()
          # writing data rows
          writer.writerows(final)
        
    return render_template('form.html',pair=pairs)

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['timestamp','timestamp','image_name']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
             sql = "INSERT INTO addresses (timestamp,objects_detected,image_name) VALUES (%s, %s, %s)"
             value = (row['timestamp'],row['timestamp'],row['image_name'])
             mycursor.execute(sql, value, if_exists='append')
             mydb.commit()
if __name__ == '__main__':  
    app.run(debug = True)  
