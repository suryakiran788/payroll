  
from datetime import datetime, timezone
from . import db

class WorkLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    job_group = db.Column(db.String(20), nullable=False)
    file_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<WorkLog {self.date} - {self.employee_id}>'
