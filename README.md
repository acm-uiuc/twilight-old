# Twilight

## Usage

    pip install -r requirements.txt
    FLASK_APP=twilight.py flask run
    
## POSTing

    curl -H "token: foo" -X post http://localhost:5000 -d '{"abc":1}' 
