from fastapi import FastAPI, Path
from typing import Optional

# data validation library
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {"name": "Saad", "age": "21", "year": "year 12"},
    2: {"name": "Yasser", "age": "21", "year": "year 12"},
}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    return students


@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="Enter the ID of the student")):
    if student_id not in students:
        return {"Error": "Student not found"}
    return students[student_id]


# Query parameter
@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None, test: int):
    for id in students:
        if students[id]["name"] == name:
            return students[id]
    return {"Data": "Not Found"}


# Path parameter
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int):
    for id in students:
        if students[id]["name"] == name:
            return students[id]
    return {"Data": "Not Found"}


# request body and the post method
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student Exist"}
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/}{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student doesn't exist"}
    if student.name != None:
        students[student_id]["name"] = student.name

    if student.age != None:
        students[student_id]["age"] = student.age

    if student.year != None:
        students[student_id]["year"] = student.year

    return students[student_id]


# delete
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student doesn't exist"}

    del students[student_id]
    return {"Msg": "Studen deleted successfully"}


"""
gt = greater than
lt = less than
ge = greater than or equal
le = less than or equal
"""
# google.com/results?search=Python
# Path(description="Enter the ID of the student", gt=0)
