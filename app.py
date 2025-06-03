import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template , request
import time

cred = credentials.Certificate("service_accountkey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

def addpatientdata(data, id1):
    db.collection('patient').document(id1).set(data)

def readpatient(table, max_retries=3):
    list = []
    temp = []
    keys = ['id', 'name', 'age', 'gender', 'address', 'phone', 'email', 'blood', 'weight', 'height', 'stage', 'history']
    
    for attempt in range(max_retries):
        try:
            result = db.collection(table).get()
            for res in result:
                dict = res.to_dict()
                for i in keys:
                    temp.append(dict.get(i, ''))  # Use get() to handle missing fields
                list.append(temp)
                temp = []
            list = sorted(list, key=lambda x: x[0])
            return list
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise Exception(f"Failed to read data after {max_retries} attempts: {str(e)}")
            print(f"Attempt {attempt + 1} failed, retrying... Error: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff
            continue

def deletedata(collection, document):
    db.collection(collection).document(document).delete()

def addlocationdata(data, id1):
    db.collection('patient').document(id1).collection('details').document("Location").set(data)

def addprescriptiondata(data, id1):
    db.collection('patient').document(id1).collection('details').document("Prescription").set(data)

def addcontactdata(data, id1):
    db.collection('patient').document(id1).collection('details').document("Contacts").set(data)

def deletecontactdata(id1):
    db.collection('patient').document(id1).collection('details').document('Contacts').delete()

@app.route("/", methods=['GET', 'POST'])
def hello():
    result = readpatient("patient")
    return render_template("index.html", data=result)

@app.route("/home", methods=['GET', 'POST'])
def homepage():
    result = readpatient("patient")
    return render_template("index.html", data=result)

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("addpatient.html")

@app.route("/locations", methods=['GET', 'POST'])
def locations():
    return render_template("locations.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route("/homemap", methods=['GET', 'POST'])
def homemap():
    return render_template("homemapdata.html")

@app.route("/prescription", methods=['GET', 'POST'])
def prescription():
    return render_template("prescription.html")

@app.route("/editpatient", methods=['GET', 'POST'])
def editpatient():
    return render_template("editpatient.html")

@app.route("/addlocation", methods=['GET', 'POST'])
def add():
    return render_template("addlocation.html")

@app.route("/addcontact", methods=['GET', 'POST'])
def addcontactpage():
    return render_template("addcontact.html")

@app.route("/editcontact", methods=['GET', 'POST'])
def editcontact():
    return render_template("editcontact.html")

@app.route("/addprescription", methods=['GET', 'POST'])
def addprescriptionpage():
    return render_template("addprescription.html")

@app.route("/editprescription", methods=['GET', 'POST'])
def editprescription():
    return render_template("editprescription.html")

@app.route("/add-patient", methods=['GET', 'POST'])
def addpatient():
    if request.method=="POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        email = request.form["email"]
        blood = request.form["blood"]
        weight = request.form["weight"]
        age = request.form["age"]
        height = request.form["height"]
        stage = request.form["stage"]
        address = request.form["address"]
        phone = request.form["phone"]
        history = request.form["history"]
        gender = request.form["gender"]

        data ={'id':id1, 'name':name,'email':email, 'blood':blood, 'weight':weight,'age':age, 'height':height,'stage':stage,'address':address,'phone':phone, 'history':history,'gender':gender}
        addpatientdata(data, id1)

        result = readpatient("patient")
    
    return render_template("index.html", data=result)

@app.route("/delete-patient", methods=['GET', 'POST'])
def deletepatient():
    if request.method=="POST":
        collection="patient"
        id1 = request.form["id1"]
        deletedata(collection, id1)
    return render_template("editpatient.html")

@app.route("/add-location", methods=['GET', 'POST'])
def addlocation():
    if request.method=="POST":
        id1 = request.form["id1"]
        location = request.form["location"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        data={'location':location, 'latitude':latitude, 'longitude':longitude}
        addlocationdata(data, id1)

    return render_template("addlocation.html")

@app.route("/add-contact", methods=['GET', 'POST'])
def addcontact():
    if request.method=="POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        relation = request.form["relation"]
        phone = request.form["phone"]

        data={'name':name, 'relation':relation, 'phone':phone}
        addcontactdata(data, id1)

        list=[]
        list.append(id1)
        keys=['name','phone','relation']
        result = db.collection("patient").document(id1).collection("details").document('Contacts').get()
        dict = result.to_dict()
        for i in keys:
            list.append(dict[i])

    return render_template("contact.html", data=list)

@app.route("/delete-contact", methods=['GET', 'POST'])
def deletecontact():
    if request.method=="POST":
        id1 = request.form["id1"]
        deletecontactdata(id1)
    return render_template("editcontact.html")

@app.route("/update-contact", methods=['GET', 'POST'])
def updatecontact():
    if request.method=="POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        relation = request.form["relation"]
        phone = request.form["phone"]

        data={'name':name, 'relation':relation, 'phone':phone}
        addcontactdata(data, id1)

    return render_template("editcontact.html")

@app.route("/add-prescription", methods=['GET', 'POST'])
def addprescription():
    if request.method=="POST":
        pid = request.form["pid"]
        id1 = request.form["id1"]
        name = request.form["name"]
        mor = request.form["mor"]
        af = request.form["af"]
        eve = request.form["eve"]
        qty = request.form["qty"]
        day = request.form["day"]

        data={'pid':pid, 'id1':id1, 'name':name, 'mor':mor, 'af':af, 'eve':eve, 'qty':qty, 'day':day}
        addprescriptiondata(data, id1)

        list=[]
        keys=['id1', 'pid', 'name', 'mor', 'af', 'eve', 'qty', 'day']
        result = db.collection("patient").document(id1).collection("details").document('Prescription').get()
        dict = result.to_dict()
        for i in keys:
            list.append(dict[i])

    return render_template("prescription.html", data=list)

@app.route("/delete-prescription", methods=['GET', 'POST'])
def deleteprescription():
    if request.method=="POST":
        id1 = request.form["id1"]
        db.collection('patient').document(id1).collection('details').document('Prescription').delete()
    return render_template("editprescription.html")

@app.route("/update-prescription", methods=['GET', 'POST'])
def updateprescriptiondata():
    if request.method=="POST":
        pid = request.form["pid"]
        id1 = request.form["id1"]
        name = request.form["name"]
        mor = request.form["mor"]
        af = request.form["af"]
        eve = request.form["eve"]
        qty = request.form["qty"]
        day = request.form["day"]

        data={'pid':pid, 'id1':id1, 'name':name, 'mor':mor, 'af':af, 'eve':eve, 'qty':qty, 'day':day}
        addprescriptiondata(data, id1)

    return render_template("editprescription.html")

@app.route("/update-patient", methods=['GET', 'POST'])
def updatepatientdata():
    if request.method=="POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        email = request.form["email"]
        blood = request.form["blood"]
        weight = request.form["weight"]
        age = request.form["age"]
        height = request.form["height"]
        stage = request.form["stage"]
        address = request.form["address"]
        phone = request.form["phone"]
        history = request.form["history"]
        gender = request.form["gender"]

        data ={'id':id1, 'name':name,'email':email, 'blood':blood, 'weight':weight,'age':age, 'height':height,'stage':stage,'address':address,'phone':phone, 'history':history,'gender':gender}
        addpatientdata(data, id1)

    return render_template("editpatient.html")

if __name__ == '__main__':
    app.run(debug=True)