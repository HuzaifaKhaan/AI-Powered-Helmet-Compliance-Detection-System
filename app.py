# flask active: .venv\Scripts\activate

from flask import Flask,jsonify
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
from detection import process
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Programmer.12",
    database="helmet_detection_db",
    port=3306
)

cursor = conn.cursor()


app = Flask(__name__)
app.app_context().push()
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Programmer.12@localhost/helmet_detection_db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)


class licenseplate(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    HelmetRiders=db.Column(db.String(100))
    Non_HelmetRiders=db.Column(db.String(100))
    Timestampp= db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,HelmetRiders,Non_HelmetRiders,Timestampp):
        self.HelmetRiders =HelmetRiders
        self.Non_HelmetRiders=Non_HelmetRiders
        self.Timestampp=Timestampp

class licenseplateSchemaHr(ma.Schema):
    class Meta:
        fields=('id','HelmetRiders','Timestampp')

class licenseplateSchemaNhr(ma.Schema):
    class Meta:
        fields=('id','Non_HelmetRiders','Timestampp')


licenseplate_schemaHr = licenseplateSchemaHr()
licenseplates_schemaHR = licenseplateSchemaHr(many=True)


licenseplate_schemaNhr = licenseplateSchemaNhr()
licenseplates_schemaNhR = licenseplateSchemaNhr(many=True)

licenseplate_schema =licenseplateSchemaHr()
licenseplates_schema =licenseplateSchemaHr(many=True)

licenseplate_schema =licenseplateSchemaNhr()
licenseplates_schema =licenseplateSchemaNhr(many=True)

@app.route("/")


def hello_world():
    return jsonify({"message":"hello world"})

@app.route("/licenseplates", methods=["POST"])
def add_licenseplate():
    HelmetRiders = request.json['HelmetRiders']
    Non_HelmetRiders = request.json['Non_HelmetRiders']
    new_licenseplate = licenseplate(HelmetRiders, Non_HelmetRiders, datetime.utcnow())
    db.session.add(new_licenseplate)
    db.session.commit()
    return jsonify(licenseplate_schema.dump(new_licenseplate))


# Get all records
@app.route("/licenseplates", methods=["GET"])
def get_licenseplates():
    all_licenseplates = licenseplate.query.all()
    result = licenseplates_schema.dump(all_licenseplates)
    return jsonify(result)


# Get single record by ID
@app.route("/licenseplates/<id>", methods=["GET"])
def get_licenseplate(id):
    licenseplate_record = licenseplate.query.get(id)
    return jsonify(licenseplate_schema.dump(licenseplate_record))


@app.route("/nonhelmetriders", methods=["GET"])
def count_nhr():
    lp = licenseplate.query.filter(licenseplate.Non_HelmetRiders != '').all()
    length = len(lp)
    return jsonify({'count': length})

@app.route("/helmetriders", methods=["GET"])
def count_hr():
    lp = licenseplate.query.all()
    count = sum(1 for plate in lp if plate.HelmetRiders)
    return jsonify({'count': count})




# Update a record
@app.route("/licenseplates/<id>", methods=["PUT"])
def update_licenseplate(id):
    licenseplate_record = licenseplate.query.get(id)
    HelmetRiders = request.json['HelmetRiders']
    Non_HelmetRiders = request.json['Non_HelmetRiders']
    licenseplate_record.HelmetRiders = HelmetRiders
    licenseplate_record.Non_HelmetRiders = Non_HelmetRiders
    db.session.commit()
    return jsonify(licenseplate_schema.dump(licenseplate_record))


# Delete a record
@app.route("/licenseplates/<id>", methods=["DELETE"])
def delete_licenseplate(id):
    licenseplate_record = licenseplate.query.get(id)
    db.session.delete(licenseplate_record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"})

@app.route('/detection',methods=['GET'])
def detection():
    process('main2.mp4')
    return jsonify({"message": "Detection successfully"})

if __name__ == '__main__':
    app.run(debug=True)