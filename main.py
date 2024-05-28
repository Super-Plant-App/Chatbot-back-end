from fastapi import FastAPI

app = FastAPI()

"""
amazon.com/create-user
GET - GET AN INFORMATION
POST - CREATE SOMETHING NEW
PUT - UPDATE 
DELETE - DELETE SOMETHING
"/" = home
"""
students = {1: {"name": "Saad", "age": "21", "class": "year 12"}}


@app.get("/")
def index():
    return students


@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    return students[student_id]


# my route : /computer-vision/disease-detection
