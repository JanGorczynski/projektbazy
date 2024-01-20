from app import db

class wojewodztwa(db.Model):
    nazwa = db.Column(db.Text)
    id_woj = db.Column(db.Integer, primary_key=True)
    powiat = db.relationship('powiaty', backref='wojewodztwa', lazy=False)
    __table_args__ = {'schema': 'energy'}
    def __repr__(self):
        return f'<Item {self.nazwa}>'
    
class powiaty(db.Model):
    __table_args__ = {'schema': 'energy'}
    nazwa = db.Column(db.Text)
    id_powiat = db.Column(db.Integer, primary_key=True)
    id_woj = db.Column(db.Integer, db.ForeignKey('energy.wojewodztwa.id_woj'))
    
    def __repr__(self):
        return f'<Item {self.nazwa}>'
    
class consumer_records(db.Model):
    __table_args__ = {'schema': 'energy'}
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    consumer_id = db.Column(db.Integer)


class consumer(db.Model):
    __table_args__ = {'schema': 'energy'}
    consumer_id = db.Column(db.Integer, primary_key=True)
    id_grid_member = db.Column(db.Integer)

class producer_records(db.Model):
    __table_args__ = {'schema': 'energy'}
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    producer_id = db.Column(db.Integer)

class producers(db.Model):
    __table_args__ = {'schema': 'energy'}
    id_producer = db.Column(db.Integer, primary_key=True)
    id_grid_member = db.Column(db.Integer)

class adres(db.Model):
    __table_args__ = {'schema': 'energy'}
    id_adres = db.Column(db.Integer, primary_key=True)
    ulica = db.Column(db.Text)
    nr_domu = db.Column(db.Text)

class grid_member(db.Model):
    __table_args__ = {'schema': 'energy'}
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    adres_id = db.Column(db.Integer)

class type(db.Model):
    __table_args__ = {'schema': 'energy'}
    id_type = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.Text)

class emergency_member(db.Model):
    __table_args__ = {'schema': 'energy'}
    id = db.Column(db.Integer, primary_key=True)
    grid_id = db.Column(db.Integer)
    emergency_id = db.Column(db.Integer)

class emergency(db.Model):
    __table_args__ = {'schema': 'energy'}
    id_emergency = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)




