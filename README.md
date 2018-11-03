# budget

```
export GOOGLE_APPLICATION_CREDENTIALS=../budget-data-d6bdc-firebase-adminsdk-bu5t8-383b28eb2d.json
export FLASK_APP=app.py
flask run
```

## Backend API Doc

curl -v -X POST -d @spiderman.json -H "Content-type: application/json" http://localhost:5000/heroes

curl -X DELETE http://localhost:5000/heroes/-LQNfxvlYuLEj8QIGU3A