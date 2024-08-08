Project configuration:
    1. Install python3 in your system
    2. Create a virtual environment and activate it
    3. install the packages from requirements file by running 'pip install -r requirements.txt'
    1. Set your mysql connection string as environment varibale named 'DATABASE_URL'
    2. Run your application by 'python run.py'


API Docs:
    1. For health check
        Endpoint: {Endpoint}/
        Method: GET
    
    2. For uploading the payroll csv file
        Endpoint: {Endpoint}/uploadWorklog
        Method: POST
        payload:{
            worklogfile: file<time-report-x.csv>
        }
    
    3. For generate the payroll report
        Endpoint: {Endpoint}/worklogReport
        Method: GET