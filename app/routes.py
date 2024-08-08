import io
import re
import traceback
from flask import current_app as app, request, jsonify
from .models import WorkLog, db
from datetime import datetime, date
import pandas as pd
import calendar


@app.route('/', methods=['GET'])
def index():
    '''
    This is the endpoint for health check
    '''
    return jsonify({"message": "This is for health check"}), 200


@app.route('/uploadWorklog', methods=['POST'])
def worklog_upload():
    '''
    Created by surya kiran on Aug 7, 2024
    To fetch the payroll data from the csv
    file and save to database
    '''
    try:
        if 'worklogfile' not in request.files:
            return jsonify({'message': 'Invalid file'}), 400
        
        wrk_log_file = request.files['worklogfile']
        pattern = r'^time-report-(\d+)\.csv$'
        check_file_name = re.match(pattern, wrk_log_file.filename)
        
        if (check_file_name is None):
            return jsonify({'message': 'Invalid file'}), 400
        
        file_id = int(check_file_name.group(1))
        
        read_data = pd.read_csv(io.BytesIO(wrk_log_file.read())) 
        formatted_data = read_data.to_dict(orient='records')
        existing_worklog = WorkLog.query.filter_by(file_id=file_id).first()
        
        if existing_worklog is not None:
            return jsonify({'message': 'File content already exists'}), 400
        
        for item in formatted_data:
            ins_object = WorkLog(
                date = datetime.strptime(item['date'], '%d/%m/%Y').date(),
                hours_worked = item['hours worked'],
                employee_id = item['employee id'],
                job_group = item['job group'],
                file_id = file_id
            )
            db.session.add(ins_object)
        
        db.session.commit()
        
        return jsonify({"message": "Work log added successfully!"}), 200

    except Exception:
        print(traceback.format_exc())
        return jsonify({"message": "An unexpected error occured"}), 500


@app.route('/worklogReport', methods=['GET'])
def generate_worklog_report():
    '''
    Created by surya kiran on Aug 8, 2024
    To generate the payroll report
    '''
    
    try:
        worklogs = WorkLog.query.with_entities(
            WorkLog.id,
            WorkLog.date,
            WorkLog.hours_worked,
            WorkLog.employee_id,
            WorkLog.job_group,
            WorkLog.created_date
        ).order_by(WorkLog.employee_id, WorkLog.created_date).all()
        
        employee_report = []
        employee_obj = {}
        
        for log in worklogs:
            
            convert_date_obj = convert_date(log.date)
            ammount = calculate_ammount(log.hours_worked, log.job_group)
            
            if log.employee_id in employee_obj:
                if str(convert_date_obj['startDate']) in employee_obj[log.employee_id]:
                    employee_obj[log.employee_id][str(convert_date_obj['startDate'])]['amountPaid'] += ammount
                else:
                    employee_obj[log.employee_id][str(convert_date_obj['startDate'])] = {
                        "employeeId": log.employee_id,
                        "payPeriod": {
                            "startDate": convert_date_obj['startDate'],
                            "endDate": convert_date_obj['endDate']
                        },
                        "amountPaid": ammount
                    }
            else:
                employee_obj[log.employee_id] = {
                    # 'payPeriod': {
                    str(convert_date_obj['startDate']): {
                        "employeeId": log.employee_id,
                        "payPeriod": {
                            "startDate": convert_date_obj['startDate'],
                            "endDate": convert_date_obj['endDate']
                        },
                        "amountPaid": ammount
                        }
                    # }
                }
        for _, value in employee_obj.items():
            for _, payvalue in value.items():
                payvalue['amountPaid'] = "$" + str( payvalue['amountPaid'])
                employee_report.append(payvalue)
        response = {
            'payrollReport': {
                'employeeReports': employee_report
            }
        }
        return jsonify(response), 200
        
    except Exception:
        print(traceback.format_exc())
        return jsonify({"message": "An unexpected error occured"}), 500


def calculate_ammount(hour, group):
    try:
        if group == 'A':
            ammount = hour * 20
        else:
            ammount = hour * 30
        return ammount
    
    except Exception:
        print(traceback.format_exc())
        return jsonify({"message": "An unexpected error occured"}), 500


def convert_date(dateObj):
    try:
        if dateObj.day < 15:
            start_date = date(dateObj.year, dateObj.month, 1)
            end_date = date(dateObj.year, dateObj.month, 15)
        else:
            start_date = date(dateObj.year, dateObj.month, 16)
            _, last_day = calendar.monthrange(dateObj.year, dateObj.month)
            end_date = date(dateObj.year, dateObj.month, last_day)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        return {'startDate': start_date, 'endDate': end_date}
    
    except Exception:
        print(traceback.format_exc())
        return jsonify({"message": "An unexpected error occured"}), 500