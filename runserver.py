import subprocess
import os

try:
    os.environ['SERVER'] = 'dev'
    subprocess.run(['python', '-V'])
    print('------------ Local Server Starting at 0.0.0.0:8000 ------------')
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])

except Exception as e:
    print('------------ Exception Occurred ------------')
    print(e)
