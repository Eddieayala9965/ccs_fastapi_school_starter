from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import our tools
# This is the database connection file
from db import session

# These are our models
from models import Students, Enrollments, Courses

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Root Route"}


@app.get('/courses')
def get_courses():
    courses = session.query(Courses)
    return courses.all()


@app.get('/students')
def get_students():
    students = session.query(Students)
    return students.all()


@app.get('/enrollments')
def get_enrollments():
    enrollments = session.query(Enrollments, Students, Courses,).join(Students, Students.id == Enrollments.student_id).join(Courses, Courses.id == Enrollments.course_id)
    results = enrollments.all()

    enrollment_list = []
    for enrollment in results:
        enrollment_dict = {
            "enrollment_id": enrollment.Enrollments.enrollment_id,
            "student_name": enrollment.Students.name, 
            "course_name": enrollment.Courses.name,
            "enrollment_date" : enrollment.Enrollments.enrollment_date
        }
        enrollment_list.append(enrollment_dict)

    return enrollment_list

@app.post('/create/student')
async def create_student(id: int, name: str):
    new_student = Students( id=id, name=name)
    session.add(new_student)
    session.commit()
    return {"student added": new_student.name}

@app.post('/create/course')
async def create_course(id: int, name: str):
    new_course = Courses(id=id, name=name)
    session.add(new_course)
    session.commit()
    return {"course added": new_course.name}

@app.post('/create/enrollment')
async def create_enrollment(enrollment_id: int, student_id: int , course_id: int, enrollment_date: datetime):
    new_enrollment = Enrollments(enrollment_id=enrollment_id, student_id=student_id, course_id=course_id, enrollment_date = enrollment_date)
    session.add(new_enrollment)
    session.commit()
    return {"enrollment added": new_enrollment}

