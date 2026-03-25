from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

app = FastAPI(
    title="Online Course Platform API",
    description="A complete backend system for managing online courses, students, and enrollments.",
    version="1.0.0",
)


courses_db = [
    {"id": 1, "title": "Python for Beginners", "category": "Programming",
     "instructor": "Alice Johnson", "price": 499.0, "duration_hours": 20,
     "rating": 4.5, "enrolled": 120, "available": True},
    {"id": 2, "title": "Web Development with FastAPI", "category": "Programming",
     "instructor": "Bob Smith", "price": 799.0, "duration_hours": 30,
     "rating": 4.8, "enrolled": 85, "available": True},
    {"id": 3, "title": "Data Science Fundamentals", "category": "Data Science",
     "instructor": "Carol White", "price": 999.0, "duration_hours": 40,
     "rating": 4.6, "enrolled": 200, "available": True},
    {"id": 4, "title": "Machine Learning A-Z", "category": "Data Science",
     "instructor": "David Lee", "price": 1299.0, "duration_hours": 60,
     "rating": 4.9, "enrolled": 350, "available": True},
    {"id": 5, "title": "UI/UX Design Basics", "category": "Design",
     "instructor": "Eva Martinez", "price": 599.0, "duration_hours": 25,
     "rating": 4.3, "enrolled": 75, "available": False},
    {"id": 6, "title": "Digital Marketing Mastery", "category": "Marketing",
     "instructor": "Frank Wilson", "price": 699.0, "duration_hours": 35,
     "rating": 4.1, "enrolled": 95, "available": True},
]

students_db = [
    {"id": 1, "name": "Ravi Kumar", "email": "ravi@example.com",
     "phone": "9876543210", "enrolled_courses": []},
    {"id": 2, "name": "Sneha Patel", "email": "sneha@example.com",
     "phone": "9123456780", "enrolled_courses": []},
]

enrollments_db = []

next_course_id = 7
next_student_id = 3
next_enrollment_id = 1



class Course(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Course title")
    category: str = Field(..., min_length=2, description="e.g. Programming, Data Science, Design")
    instructor: str = Field(..., min_length=3, description="Instructor full name")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    duration_hours: int = Field(..., gt=0, description="Course duration in hours")
    rating: float = Field(0.0, ge=0.0, le=5.0, description="Rating between 0 and 5")
    available: bool = Field(True, description="Is the course currently available?")


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    category: Optional[str] = None
    instructor: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    duration_hours: Optional[int] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    available: Optional[bool] = None


class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Full name")
    email: str = Field(..., description="Valid email address")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = None



def find_course(course_id: int):
    """Return course dict or None."""
    return next((c for c in courses_db if c["id"] == course_id), None)


def find_student(student_id: int):
    """Return student dict or None."""
    return next((s for s in students_db if s["id"] == student_id), None)


def find_enrollment(enrollment_id: int):
    """Return enrollment dict or None."""
    return next((e for e in enrollments_db if e["id"] == enrollment_id), None)


def find_enrollment_by_pair(student_id: int, course_id: int):
    """Check if a student-course enrollment already exists."""
    return next(
        (e for e in enrollments_db
         if e["student_id"] == student_id and e["course_id"] == course_id),
        None,
    )


def calculate_total_revenue() -> float:
    """Sum of (price × enrolled) for all courses."""
    return round(sum(c["price"] * c["enrolled"] for c in courses_db), 2)


def filter_logic(
    keyword=None,
    category=None,
    min_price=None,
    max_price=None,
    available=None,
):
    """Apply multiple optional filters to courses_db and return results."""
    result = courses_db[:]
    if keyword is not None:
        kw = keyword.lower()
        result = [
            c for c in result
            if kw in c["title"].lower() or kw in c["instructor"].lower()
        ]
    if category is not None:
        result = [c for c in result if c["category"].lower() == category.lower()]
    if min_price is not None:
        result = [c for c in result if c["price"] >= min_price]
    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]
    if available is not None:
        result = [c for c in result if c["available"] == available]
    return result



# Q1 ── Home Route
@app.get("/", tags=["General"])
def home():
    """Welcome endpoint with platform overview."""
    return {
        "platform": "Online Course Platform",
        "version": "1.0.0",
        "message": "Welcome! Explore, enroll, and grow your skills.",
        "total_courses": len(courses_db),
        "total_students": len(students_db),
        "total_enrollments": len(enrollments_db),
    }


# Q2 ── Get All Courses
@app.get("/courses", tags=["Courses"])
def get_all_courses():
    """Return the complete list of courses."""
    return {"total": len(courses_db), "courses": courses_db}


# Q3 ── Get Course by ID  ← variable route AFTER fixed routes
@app.get("/courses/{course_id}", tags=["Courses"])
def get_course_by_id(course_id: int):
    """Fetch a single course by its ID."""
    course = find_course(course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with ID {course_id} not found.",
        )
    return course


# Q4 ── Course Summary / Count Endpoint
@app.get("/courses/summary/stats", tags=["Courses"])
def course_summary():
    """Return platform-level statistics."""
    categories = list({c["category"] for c in courses_db})
    avg_price = round(sum(c["price"] for c in courses_db) / len(courses_db), 2) if courses_db else 0
    top_course = max(courses_db, key=lambda c: c["enrolled"]) if courses_db else None
    return {
        "total_courses": len(courses_db),
        "available_courses": sum(1 for c in courses_db if c["available"]),
        "unavailable_courses": sum(1 for c in courses_db if not c["available"]),
        "total_enrolled_students": sum(c["enrolled"] for c in courses_db),
        "categories": categories,
        "average_price": avg_price,
        "total_revenue": calculate_total_revenue(),
        "most_popular_course": top_course["title"] if top_course else None,
    }



# Q5 ── Add New Course
@app.post("/courses", status_code=201, tags=["Courses"])
def add_course(course: Course):
    """Create a new course with full Pydantic validation."""
    global next_course_id
    new_course = {"id": next_course_id, **course.dict()}
    courses_db.append(new_course)
    next_course_id += 1
    return {"message": "Course created successfully.", "course": new_course}


# Q6 ── Register New Student
@app.post("/students", status_code=201, tags=["Students"])
def register_student(student: Student):
    """Register a new student. Prevents duplicate email addresses."""
    global next_student_id
    if any(s["email"] == student.email for s in students_db):
        raise HTTPException(
            status_code=400,
            detail="A student with this email already exists.",
        )
    new_student = {"id": next_student_id, **student.dict(), "enrolled_courses": []}
    students_db.append(new_student)
    next_student_id += 1
    return {"message": "Student registered successfully.", "student": new_student}


# Q7 ── Get All Students
@app.get("/students", tags=["Students"])
def get_all_students():
    """Return list of all registered students."""
    return {"total": len(students_db), "students": students_db}



# Q8 ── Search Courses by Keyword
@app.get("/courses/search/keyword", tags=["Search & Filter"])
def search_courses(
    keyword: str = Query(..., min_length=1, description="Search in title or instructor name"),
):
    """Search courses by keyword (title or instructor)."""
    results = filter_logic(keyword=keyword)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No courses found for keyword '{keyword}'.",
        )
    return {"keyword": keyword, "total_found": len(results), "courses": results}


# Q9 ── Filter Courses by Category / Price / Availability
@app.get("/courses/filter/category", tags=["Search & Filter"])
def filter_courses_endpoint(
    category: Optional[str] = Query(None, description="e.g. Programming, Data Science"),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    available: Optional[bool] = Query(None),
):
    """Filter courses using one or more optional query parameters."""
    results = filter_logic(
        category=category,
        min_price=min_price,
        max_price=max_price,
        available=available,
    )
    return {
        "filters_applied": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "available": available,
        },
        "total_found": len(results),
        "courses": results,
    }


# Q10 ── Revenue Report (uses calculate_total_revenue helper)
@app.get("/reports/revenue", tags=["Reports"])
def revenue_report():
    """Detailed revenue breakdown per course."""
    breakdown = [
        {
            "course_id": c["id"],
            "title": c["title"],
            "price": c["price"],
            "enrolled": c["enrolled"],
            "revenue": round(c["price"] * c["enrolled"], 2),
        }
        for c in courses_db
    ]
    return {
        "total_revenue": calculate_total_revenue(),
        "breakdown": sorted(breakdown, key=lambda x: x["revenue"], reverse=True),
    }


# Q11 ── Update Course (PUT)
@app.put("/courses/{course_id}", tags=["Courses"])
def update_course(course_id: int, updates: CourseUpdate):
    """Partially update a course. Only provided fields are changed."""
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found.")
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields were provided.")
    course.update(update_data)
    return {"message": "Course updated successfully.", "course": course}


# Q12 ── Delete Course (DELETE)
@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course(course_id: int):
    """Permanently remove a course by ID."""
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found.")
    courses_db.remove(course)
    return {"message": f"Course '{course['title']}' deleted successfully."}


# Q13 ── Update Student (PUT)
@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, updates: StudentUpdate):
    """Partially update a student record."""
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields were provided.")
    student.update(update_data)
    return {"message": "Student updated successfully.", "student": student}


# Q14 ── Delete Student (DELETE)
@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):
    """Remove a student from the platform."""
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")
    students_db.remove(student)
    return {"message": f"Student '{student['name']}' removed successfully."}



# Q15 ── Step 1: Enroll Student in a Course
@app.post("/enroll", status_code=201, tags=["Enrollment Workflow"])
def enroll_student(
    student_id: int = Query(..., description="ID of the student"),
    course_id: int = Query(..., description="ID of the course to enroll in"),
):
    """
    **Step 1 of 3** – Enroll a student in a course.
    Status after this step: `enrolled`
    """
    global next_enrollment_id
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    if not course["available"]:
        raise HTTPException(status_code=400, detail="This course is currently unavailable.")
    if find_enrollment_by_pair(student_id, course_id):
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course.")

    enrollment = {
        "id": next_enrollment_id,
        "student_id": student_id,
        "student_name": student["name"],
        "course_id": course_id,
        "course_title": course["title"],
        "status": "enrolled",
        "enrolled_on": str(date.today()),
        "completed_on": None,
        "certificate_issued": False,
    }
    enrollments_db.append(enrollment)
    course["enrolled"] += 1
    student["enrolled_courses"].append(course_id)
    next_enrollment_id += 1
    return {"message": "Enrollment successful! Proceed to start the course.", "enrollment": enrollment}


# Q16 ── Step 2: Start the Course
@app.put("/enroll/{enrollment_id}/start", tags=["Enrollment Workflow"])
def start_course(enrollment_id: int):
    """
    **Step 2 of 3** – Mark the course as started.
    Requires status to be `enrolled`.
    Status after this step: `started`
    """
    enrollment = find_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment record not found.")
    if enrollment["status"] != "enrolled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start. Current status is '{enrollment['status']}'. Must be 'enrolled'.",
        )
    enrollment["status"] = "started"
    return {"message": "Course started! Keep learning and finish strong.", "enrollment": enrollment}


# Q17 ── Step 3: Complete Course & Issue Certificate
@app.put("/enroll/{enrollment_id}/complete", tags=["Enrollment Workflow"])
def complete_course(enrollment_id: int):
    """
    **Step 3 of 3** – Mark the course as completed and issue a certificate.
    Requires status to be `started`.
    Status after this step: `completed`
    """
    enrollment = find_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment record not found.")
    if enrollment["status"] != "started":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete. Current status is '{enrollment['status']}'. Must be 'started'.",
        )
    enrollment["status"] = "completed"
    enrollment["completed_on"] = str(date.today())
    enrollment["certificate_issued"] = True

    course = find_course(enrollment["course_id"])
    student = find_student(enrollment["student_id"])
    return {
        "message": "Congratulations! You have successfully completed the course!",
        "certificate": {
            "certificate_id": f"CERT-{enrollment['id']:04d}",
            "issued_to": student["name"] if student else "N/A",
            "course": course["title"] if course else "N/A",
            "issued_on": str(date.today()),
        },
        "enrollment": enrollment,
    }


# Q18 ── Sort Courses
@app.get("/courses/sort/results", tags=["Advanced"])
def sort_courses(
    sort_by: str = Query(
        "rating",
        description="Field to sort by: price | rating | duration_hours | enrolled | title",
    ),
    order: str = Query("desc", description="Sort order: asc | desc"),
):
    """Sort all courses by a chosen field in ascending or descending order."""
    valid_fields = ["price", "rating", "duration_hours", "enrolled", "title"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by value. Choose from: {valid_fields}",
        )
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'.")
    sorted_courses = sorted(courses_db, key=lambda c: c[sort_by], reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "total": len(sorted_courses), "courses": sorted_courses}


# Q19 ── Pagination
@app.get("/courses/page/list", tags=["Advanced"])
def paginate_courses(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(3, ge=1, le=10, description="Number of results per page"),
):
    """Retrieve courses with pagination support."""
    total = len(courses_db)
    total_pages = -(-total // page_size)   # ceiling division
    start = (page - 1) * page_size
    end = start + page_size
    if start >= total:
        raise HTTPException(status_code=404, detail=f"Page {page} does not exist. Total pages: {total_pages}.")
    return {
        "page": page,
        "page_size": page_size,
        "total_courses": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "courses": courses_db[start:end],
    }


# Q20 ── Combined Browse  (Search + Filter + Sort + Paginate)
@app.get("/courses/browse/all", tags=["Advanced"])
def browse_courses(
    keyword: Optional[str] = Query(None, description="Search in title or instructor"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, gt=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, gt=0, description="Maximum price"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    sort_by: str = Query("rating", description="price | rating | duration_hours | enrolled"),
    order: str = Query("desc", description="asc | desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=10),
):
    
    # Filter
    results = filter_logic(
        keyword=keyword,
        category=category,
        min_price=min_price,
        max_price=max_price,
        available=available,
    )

    # Sorting
    valid_fields = ["price", "rating", "duration_hours", "enrolled", "title"]
    if sort_by in valid_fields:
        results = sorted(results, key=lambda c: c[sort_by], reverse=(order == "desc"))

    #Paginate
    total = len(results)
    total_pages = -(-total // page_size) if total > 0 else 1
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "filters": {
            "keyword": keyword,
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "available": available,
        },
        "sort": {"sort_by": sort_by, "order": order},
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_results": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
        "courses": results[start:end],
    }