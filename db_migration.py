import subprocess

try:
    print('------------ DB Migrations Started ------------')
    subprocess.run(["python", "manage.py", "makemigrations"])

    subprocess.run(["python", "manage.py", "migrate"])

except Exception as e:
    print('------------ Exception Occurred ------------')
    print(e)
