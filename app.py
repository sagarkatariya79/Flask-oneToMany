from ast import Try
import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_restful import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.Text)

class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employe_detail = db.Column(db.String(120))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class MyClassget(Resource):

    def get(self,id):
        try:    
            pData = Person.query.get(id)
            print("-------------",pData)
            eData = Employment.query.filter_by(person_id =id).all()
            print(pData.name,"---------")
            print(eData,"============")
            emp = []
            for i in eData:
                emp.append(i.employe_detail)
            print("eeeeeee",emp)
            display = {"id":id,"name":pData.name , "address":pData.address,"employe_detail":emp}
            return display , 200
        except:
            return {"msg":"Somthing went wrong"} ,400

class MyClasspost(Resource):
    def post(self):
        data = request.get_json()
        print("===============",data)
        pData = Person.query.get(data["id"])
        print("========",pData)
        personData = Person(id = data["id"],name = data["name"], address =data["address"])
        employmentData = Employment(employe_detail= data["employe_detail"],person_id =data["id"])
        if pData.id:
            db.session.add(employmentData)
        else:
            db.session.add_all([personData,employmentData])
        db.session.commit()
        if data:
            return {"msg":"Sucessfully added"} , 201
        return {"msg":"some error occers"} , 400



class AllDataclass(Resource):
    def get(self):
        pData = Person.query.all()
       
        allData = {}
        for i in pData:
            display = {}
            eData = Employment.query.filter_by(person_id =i.id).all()
            emp = []
            for j in eData:
                emp.append(j.employe_detail)
            display = {"id":i.id,"name":i.name , "address":i.address,"employe_detail":emp}
            allData[i.id] = display
        print(allData)
        return allData , 200


api.add_resource(AllDataclass,"/all")
api.add_resource(MyClasspost,"/personpost")
api.add_resource(MyClassget,"/personget/<int:id>")


if __name__=='__main__':
    db.create_all()
    app.run(port = 8080, debug=True)

#200 = Sucessful, 404 = Not Found, 201 = Created Sucessfully
