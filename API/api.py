from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os

DB_LOCATION = 'LOCAL' # 'CLOUD' # 

app = Flask(__name__)

if (DB_LOCATION == 'CLOUD'):
    DATABASE_URL = "" # Provide PostgreSQL Cloud DB Connection String here.
else:
    DATABASE_URL = "" # Provide PostgreSQL local DB Connection String here.
    
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, but recommended to disable
db = SQLAlchemy(app)

class SystemData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.String)
    cpu_usage = db.Column(db.Float)
    memory_usage = db.Column(db.Float)
    ram_usage = db.Column(db.Float)
    disk_usage = db.Column(db.Float)
    disk_space = db.Column(db.Float)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    try:
        record = SystemData(
            ip_address=data['ip_address'],
            timestamp=data['timestamp'],
            cpu_usage=data['cpu_usage'],
            memory_usage=data['memory_usage'],
            ram_usage=data['ram_usage'],
            disk_usage=data['disk_usage'],
            disk_space=data['disk_space']
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created within the application context
    app.run(host='0.0.0.0', port=5000)
