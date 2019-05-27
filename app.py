
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, REAL, JSON, Boolean
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://nutrient:Nitrogen-Phosphorus-Potassium-2019@p2irc-mdd.usask.ca:5432/nutrientdb"
db_string = "postgres://nutrient:Nitrogen-Phosphorus-Potassium-2019@p2irc-mdd.usask.ca:5432/nutrientdb"
db = create_engine(db_string)
Base = declarative_base()


class NutrientApp(Base):
    __tablename__ = 'NutrientApp'

    id = Column(Integer, primary_key=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    type = Column(String, nullable=False)
    reference_measurements = Column(JSON, nullable=False) 
    measurement = Column(JSON, nullable=False)
    color_method = Column(Integer, nullable=True)  # optional
    color_correction = Column(String, nullable=True)  # optional
    mass_concentration = Column(REAL, nullable=False)
    light_condition = Column(Integer, nullable=False)
    origin_of_water = Column(String, nullable=False)
    at_sampling_location = Column(Boolean, nullable=False)  # new
    temperature = Column(String, nullable=True)
    reference_concentrations = Column(JSON, nullable=False)  # new
    mass_concentration_uncorrected = Column(REAL, nullable=False)  # new
    error_message = Column(String, nullable=False)  # new
    label = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    def __repr__(self):
        return '<NutrientAPI %r>' % self.type


Session = sessionmaker(db)
session = Session()
Base.metadata.create_all(db)  # If there is a table already in the database, by default this command will not create
# session.commit()

print('Initialized the DB')


@app.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error': 'Action not allowed'}), 403)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


@app.route('/api/v1/samples', methods=['GET'])
def get_samples():
    sl = dict()
    samples = session.query(NutrientApp)

    parameter_types = ['nitrate', 'phosphate', 'custom']

    param = request.args.get('type', 'null')

    if param == 'null' or param not in parameter_types:
        return make_response(jsonify({'error': 'You need to provide parameter type with your request. For example: /api/v1/samples?type=nitrate or phosphate or custom'}), 400)

    for s in samples:
        sl[s.id] = [s.type, s.latitude, s.longitude, s.measurement, s.origin_of_water, s.mass_concentration, s.date]

        json_samples = {"message": "",
                        "data": {
                            "type": param,
                            "samples": [{"latitude": value[1], "longitude":value[2], "measurement": value[3], "origin_of_water": value[4], "mass_concentration":value[5], "date":value[6]} for key, value in sl.items() if value[0] == param]
                        }}
    return jsonify(json_samples)


@app.route('/api/v1/samples/collect_data', methods=['GET', 'POST'])
def collect_data():

    reply = {'message': 'Sample Saved.', 'data': {'missing_param': 'nothing'}, 'success': 1}
    print(request.json)
    if not request.json:
        abort(400)

# This block is to check missing parameters
    if 'latitude' not in request.json:
        reply['data']['missing_param'] = 'latitude'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'longitude' not in request.json:
        reply['data']['missing_param'] = 'longitude'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'type' not in request.json:
        reply['data']['missing_param'] = 'type'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'reference_measurements' not in request.json:
        reply['data']['missing_param'] = 'reference_measurements'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'measurement' not in request.json:
        reply['data']['missing_param'] = 'measurement'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'mass_concentration' not in request.json:
        reply['data']['missing_param'] = 'mass_concentration'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'light_condition' not in request.json:
        reply['data']['missing_param'] = 'light_condition'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'origin_of_water' not in request.json:
        reply['data']['missing_param'] = 'origin_of_water'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'at_sampling_location' not in request.json:
        reply['data']['missing_param'] = 'at_sampling_location'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'reference_concentrations' not in request.json:
        reply['data']['missing_param'] = 'reference_concentrations'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'mass_concentration_uncorrected' not in request.json:
        reply['data']['missing_param'] = 'mass_concentration_uncorrected'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'error_message' not in request.json:
        reply['data']['missing_param'] = 'error_message'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)
    if 'label' not in request.json:
        reply['data']['missing_param'] = 'label'
        reply['success'] = 0
        reply['message'] = 'Sample Not Saved'
        abort(400, reply)

# This block is to check types of parameters
    if 'latitude' in request.json and type(request.json['latitude']) is not str:
        reply['message'] = 'latitude value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'latitude'
        abort(400, reply)
    if 'longitude' in request.json and type(request.json['longitude']) is not str:
        reply['message'] = 'longitude value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'longitude'
        abort(400, reply)
    if 'type' in request.json and type(request.json['type']) is not str:
        reply['message'] = 'type value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'type'
        abort(400, reply)
    if 'reference_measurements' in request.json and type(request.json['reference_measurements']) is not list:
        reply['message'] = 'reference_measurements value is in bad format. It should be a list.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'reference_measurements'
        abort(400, reply)
    if 'measurement' in request.json and type(request.json['measurement']) is not list:
        reply['message'] = 'measurement value is in bad format. It should be a list.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'measurement'
        abort(400, reply)
    if 'color_method' in request.json and type(request.json['color_method']) is not int:
        reply['message'] = 'color_method value is in bad format. It should be a integer.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'color_method'
        abort(400, reply)
    if 'color_correction' in request.json and type(request.json['color_correction']) is not str:
        reply['message'] = 'color_correction value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'color_correction'
        abort(400, reply)
    if 'mass_concentration' in request.json and type(request.json['mass_concentration']) is not float:
        reply['message'] = 'mass_concentration value is in bad format. It should be a double.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'mass_concentration'
        abort(400, reply)
    if 'light_condition' in request.json and type(request.json['light_condition']) is not int:
        reply['message'] = 'light_condition value is in bad format. It should be a integer.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'light_condition'
        abort(400, reply)
    if 'origin_of_water' in request.json and type(request.json['origin_of_water']) is not str:
        reply['message'] = 'origin_of_water value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'origin_of_water'
        abort(400, reply)
    if 'at_sampling_location' in request.json and type(request.json['at_sampling_location']) is not bool:
        reply['message'] = 'at_sampling_location value is in bad format. It should be a boolean.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'at_sampling_location'
        abort(400, reply)
    if 'temperature' in request.json and type(request.json['temperature']) is not str:
        reply['message'] = 'temperature value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'temperature'
        abort(400, reply)
    if 'reference_concentrations' in request.json and type(request.json['reference_concentrations']) is not list:
        reply['message'] = 'reference_concentrations value is in bad format. It should be a list.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'reference_concentrations'
        abort(400, reply)
    if 'mass_concentration_uncorrected' in request.json and type(request.json['mass_concentration_uncorrected']) is not float:
        reply['message'] = 'mass_concentration_uncorrected value is in bad format. It should be a double.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'mass_concentration_uncorrected'
        abort(400, reply)
    if 'error_message' in request.json and type(request.json['error_message']) is not str:
        reply['error_message'] = 'error_message value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'error_message'
        abort(400, reply)
    if 'label' in request.json and type(request.json['label']) is not str:
        reply['label'] = 'label value is in bad format. It should be a string.'
        reply['success'] = 0
        reply['data']['missing_param'] = 'label'
        abort(400, reply)

    lt = request.json['latitude']
    ln = request.json['longitude']
    ty = request.json['type']
    rm = request.json['reference_measurements']
    me = request.json['measurement']
    cm = request.json.get('color_method', -1)
    cc = request.json.get('color_correction', 'null')
    mc = request.json['mass_concentration']
    lc = request.json['light_condition']
    oow = request.json['origin_of_water']
    asl = request.json['at_sampling_location']
    tmp = request.json.get('temperature', 'null')
    rc = request.json['reference_concentrations']
    mcu = request.json['mass_concentration_uncorrected']
    em = request.json['error_message']
    l = request.json['label']
    dt = datetime.now()
    na = NutrientApp(latitude=lt, longitude=ln, type=ty, reference_measurements=rm, measurement=me, color_method=cm, color_correction=cc, mass_concentration=mc, light_condition=lc,origin_of_water=oow, temperature=tmp, date=dt, reference_concentrations=rc, mass_concentration_uncorrected=mcu, error_message=em, at_sampling_location=asl, label=l)
    session.add(na)
    session.commit()
    return jsonify(reply)


if __name__ == '__main__':
    app.run(debug=True)
    # db.init_app(app)
