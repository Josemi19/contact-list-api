"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/contacts", methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_contacts():
    # METODO GET
    if request.method == 'GET':
        contacts = Contact.query.all()
        contacts = list(map(lambda contact: contact.serialize(), contacts))
        return jsonify(contacts), 200

    #METODO POST
    if request.method == 'POST':

        body = request.json
        email = body.get("email", None)
        full_name = body.get("full_name", None)
        phone_number = body.get("phone_number", None)
        adress = body.get("adress", None)

        if email is None or full_name is None or phone_number is None or adress is None:
            return jsonify("Todos los campos son requeridos"), 400
        if email == "" or full_name == "":
            return jsonify("El email y el correo no pueden estar vacios"), 400

        try:
            new_contact = Contact(
            email = email,
            full_name = full_name,
            phone_number = phone_number,
            adress = adress
            )
            db.session.add(new_contact)
            db.session.commit()
            return "Contacto creado", 201

        except Exception as error:

            db.session.rollback()
            return jsonify(error.args), 500

    #METODO PUT
    if request.method == 'PUT':
        body = request.json
        id = body.get('id', None)

        if id == None:
            return jsonify("Debe enviar el id del contacto a actaulizar"), 400
        contact = Contact.query.filter_by(id = id).first()
        if contact == None:
            return jsonify("El contacto no existe"), 400

        email = body.get('email', None)
        full_name = body.get("full_name", None)
        phone_number = body.get("phone_number", None)
        adress = body.get("adress", None)
        
        if email is None or full_name is None or phone_number is None or adress is None:
            return jsonify("Todos los campos son requeridos"), 400

        try:
            contact.email = email
            contact.full_name = full_name
            contact.phone_number = phone_number
            contact.adress = adress
            db.session.commit()
            return jsonify("Contacto actualizado"), 200
        except Exception as error:
            db.session.rollback()
            return jsonify(error.args), 500

    #METODO DELETE
    if request.method == 'DELETE':
        body = request.json
        id = body.get('id', None)
        contact = Contact.query.filter_by(id = id).first()
        db.session.delete(contact)
        db.session.commit()
        return "Contacto eliminado", 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
