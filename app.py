from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect, insert
import json
import os
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')

db=SQLAlchemy(app)

from models import wojewodztwa,powiaty,consumer_records,consumer,producer_records,producers,adres,grid_member,emergency_member,emergency

@app.route('/wojewodztwa', methods=['GET'])
def get_woj():
    items = wojewodztwa.query.all()
    return jsonify({'items': [{'id': item.id_woj, 'name': item.nazwa} for item in items]})

@app.route('/powiaty', methods=['GET'])
def get_powiat():
    items = powiaty.query.all()
    return jsonify({'items': [{'id': item.id_woj, 'name': item.nazwa,'wojewodztwo':item.wojewodztwa.nazwa} for item in items]})

@app.route('/consumer_records', methods=['GET'])
def get_consumer_records():
    id = request.args.get('id')
    try:
       id = consumer.query.filter_by(id_grid_member=id)[0].consumer_id
       items = consumer_records.query.filter_by(consumer_id=id)
       return jsonify({'items': [{'date': str(item.date),'amount':item.amount} for item in items]}) 
    except:
       items = []
       return jsonify({'items': [{'date': str(item.date),'amount':item.amount} for item in items]})

@app.route('/consumer_records', methods=['POST'])
def add_consumer_records(): 
    try:
        id_grid = request.args.get('id_grid')
        amount = request.args.get('amount')
        date = request.args.get('date')
        records = consumer_records.query.all()
        consumer_id = consumer.query.filter_by(id_grid_member=id_grid)[0].consumer_id
        id = max([record.id for record in records]) + 1
        new_record = consumer_records(id=id,date=date,amount=amount,consumer_id=consumer_id)
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"succes":True})
    except:
        return 400
    
@app.route('/producer_records', methods=['GET'])
def get_producer_records():
    id = request.args.get('id')
    try:
        id = producers.query.filter_by(id_grid_member=id)[0].id_producer
        items = producer_records.query.filter_by(producer_id=id)
        return jsonify({'items': [{ 'date': str(item.date),'amount':item.amount} for item in items]}) 
    except Exception as e:
       print(e)
       items = []
       return jsonify({'items': [{'date': str(item.date),'amount':item.amount} for item in items]})

@app.route('/producer_records', methods=['POST'])
def add_producer_records(): 
    try:
        id_grid = request.args.get('id_grid')
        amount = request.args.get('amount')
        date = request.args.get('date')
        records = producer_records.query.all()
        producer_id = producers.query.filter_by(id_grid_member=id_grid)[0].id_producer
        id = max([record.id for record in records]) + 1
        new_record = producer_records(id=id,date=date,amount=amount,producer_id=producer_id)
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"succes":True})
    except:
        return 400 

#Views
@app.route('/consumers_view', methods=['GET'])
def get_consumers_view():
    try:
        connection = db.engine.connect()
        raw_query = text(f'SELECT * FROM consumers_view;')
        result = connection.execute(raw_query)
        dane_list = []
        columns = result.keys()
        for row in result:
            dane_dict = dict(zip(columns, row))
            dane_list.append(dane_dict)
        dane_json = json.dumps({'items': dane_list}, default=str)
        return app.response_class(response=dane_json, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}, 500)

@app.route('/producers_view', methods=['GET'])
def get_producers_view():
    try:
        connection = db.engine.connect()
        raw_query = text(f'SELECT * FROM producers_view;')
        result = connection.execute(raw_query)
        dane_list = []
        columns = result.keys()
        for row in result:
            dane_dict = dict(zip(columns, row))
            dane_list.append(dane_dict)
        dane_json = json.dumps({'items': dane_list}, default=str)
        return app.response_class(response=dane_json, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}, 500)
    
@app.route('/avg_production_grid', methods=['GET'])
def get_avg_production_grid():
    try:
        connection = db.engine.connect()
        raw_query = text(f'SELECT * FROM avg_production_grid;')
        result = connection.execute(raw_query)
        dane_list = []
        columns = result.keys()
        for row in result:
            dane_dict = dict(zip(columns, row))
            dane_list.append(dane_dict)
        dane_json = json.dumps({'items': dane_list}, default=str)
        return app.response_class(response=dane_json, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}, 500)
    
@app.route('/avg_consumption_grid', methods=['GET'])
def get_avg_consumption_grid():
    try:
        connection = db.engine.connect()
        raw_query = text(f'SELECT * FROM avg_consumption_grid;')
        result = connection.execute(raw_query)
        dane_list = []
        columns = result.keys()
        for row in result:
            dane_dict = dict(zip(columns, row))
            dane_list.append(dane_dict)
        dane_json = json.dumps({'items': dane_list}, default=str)
        return app.response_class(response=dane_json, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}, 500)
@app.route('/emergencies', methods=['GET'])
def get_emergencies():
    try:
        connection = db.engine.connect()
        raw_query = text(f'SELECT * FROM emergencies;')
        result = connection.execute(raw_query)
        dane_list = []
        columns = result.keys()
        for row in result:
            dane_dict = dict(zip(columns, row))
            dane_list.append(dane_dict)
        dane_json = json.dumps({'items': dane_list}, default=str)
        return app.response_class(response=dane_json, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}, 500)

#Other post requests
@app.route('/wojewodztwa', methods=['POST'])
def add_wojewodztwa():
    data = request.get_json()
    new_woj = wojewodztwa()
    new_woj.nazwa = data["nazwa"]
    new_woj.id_woj = data["id"]
    db.session.add(new_woj)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/powiaty', methods=['POST'])
def add_powiaty():
    data = request.get_json()
    new_powiaty = powiaty(
        id_powiat=data['id_powiat'],
        nazwa=data['nazwa'],
        id_woj=data['id_woj']
    )

    db.session.add(new_powiaty)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_consumer', methods=['POST'])
def add_consumer():
    data = request.get_json()

    new_consumer = consumer(
        consumer_id=data['consumer_id'],
        id_grid_member=data['id_grid_member']
    )

    db.session.add(new_consumer)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_producers', methods=['POST'])
def add_producers():
    data = request.get_json()

    new_producers = producers(
        id_producer=data['id_producer'],
        id_grid_member=data['id_grid_member']
    )

    db.session.add(new_producers)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_adres', methods=['POST'])
def add_adres():
    data = request.get_json()

    new_adres = adres(
        id_adres=data['id_adres'],
        ulica=data['ulica'],
        nr_domu=data['nr_domu']
    )

    db.session.add(new_adres)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_grid_member', methods=['POST'])
def add_grid_member():
    data = request.get_json()

    new_grid_member = grid_member(
        id=data['id'],
        type_id=data['type_id'],
        adres_id=data['adres_id']
    )

    db.session.add(new_grid_member)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_type', methods=['POST'])
def add_type():
    data = request.get_json()

    new_type = type(
        id_type=data['id_type'],
        nazwa=data['nazwa']
    )

    db.session.add(new_type)
    db.session.commit()
    return jsonify({"succes":True})

@app.route('/add_emergency_member', methods=['POST'])
def add_emergency_member():
    data = request.get_json()

    new_emergency_member = emergency_member(
        id=data['id'],
        grid_id=data['grid_id'],
        emergency_id=data['emergency_id']
    )

    db.session.add(new_emergency_member)
    db.session.commit()
    return jsonify({"succes":True})


@app.route('/add_emergency', methods=['POST'])
def add_emergency():
    data = request.get_json()

    new_emergency = emergency(
        id_emergency=data['id_emergency'],
        description=data['description']
    )

    db.session.add(new_emergency)
    db.session.commit()
    return jsonify({"succes":True})

#Templates
@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")
@app.route('/przeglad', methods=['GET'])
def przeglad():
    return render_template("przeglad.html")
@app.route('/czytniki', methods=['GET'])
def czytniki():
    return render_template("czytniki.html")

@app.route('/dodawanie', methods=['GET'])
def dodawanie():
    return render_template("dodawanie.html")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

