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


class MyClass(Resource):

    def get(self,id):
        pass
        # pData = Person.query.get(id)
        # eData = Employment.query.filter_by(person_id =id).all()
        # for i in pData:
        #     print(i)
        # print(pData.name,"---------")
        # print(eData.employe_detail,"============")
        # return {"msg":"displayed"}




    def post(self):
        data = request.get_json()
        print("===============",data)
        pData = Person.query.get(data["id"])
        print("========",pData)
        personData = Person(id = data["id"],name = data["name"], address =data["address"])
        employmentData = Employment(employe_detail= data["employe_detail"],person_id =data["id"])
        if data["id"] != pData.id:
            db.session.add_all([personData,employmentData])
        else:
            db.session.add(employmentData)
        db.session.commit()
        if data:
            return jsonify({"msg":"Sucessfully added"})
        return jsonify({"msg":"some error occers"})



api.add_resource(MyClass,"/person")
# api.add_resource(MyClass,"/person/<int:id>")


if __name__=='__main__':
    db.create_all()
    app.run(port = 8080, debug=True)

#200 = Sucessful, 404 = Not Found, 201 = Created Sucessfully
