Structure:-

fastapi-online-course-platform/
│
├── main.py              # All 20 API endpoints/n
├── requirements.txt     # Dependencies\n
├── README.md            # Project documentation\n
└── screenshots/         # Swagger UI screenshots (Q1–Q20)\n

Setup And Running:-

# step-1:-Clone the repository
git clone https://github.com/
cd the-online-course-project

# step-2:-Create a virtual environment
python -m venv venv
for Windows: venv\Scripts\activate

# step-3:-Install dependencies
pip install -r requirements.txt

# step-4:-Run the server
unicorn main:app --reload
