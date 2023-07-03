# ena-datahub-dashboard

## Usage: 
```
git clone https://github.com/KhadimGueyeKGY/ena-datahub-dashboard.git
cd ena-datahub-dashboard
pip install --no-cache-dir -r requirements.txt
```
You can either modify the ```authentication.tsv``` file by adding your username and password, or the running application will prompt you for your username and password.

```
python manage.py runserver

```

## Docker commands  (ongoing)

```
docker build -t khadimgueyekgy/ena-datahub-dashboard .
docker run --rm -it -p 8000:8000 --name ena-cohort-dashboard khadimgueyekgy/ena-datahub-dashboard

```

## view

  * http://127.0.0.1:8000/ena-data-dashboard/ 

