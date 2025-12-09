"""Sample Data Module - Test Resumes and Job Description.

Contains mock data for testing the SmartFit semantic matching engine.
Includes a sample job description and candidate resumes with varying qualifications.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

JOB_DESCRIPTION = """
    We are looking for an Engineering Manager for a Fintech company. Must have experience with Microservices, Python, and AWS.
    Leadership experience managing teams of 10+ engineers is required.
    Knowledge of Kafka and Event-Driven Architecture is. a huge plus.
"""

CANDIDATES = [
    {
        "name": "Aman Kishore Agarwal (The Perfect Fit)",
        "resume": "Associate Director of Engineering. 10+ years of Exp. Managing 35 engineers. Built lending platforms using Node.js, MongoDB, and Kafka. AWS Expert."
    },
    {
        "name": "Rohan (THe Junior)",
        "resume": "Junior Developer. 2 years experience with React and HTML. Learning Node.js. Enthusiastic about Fintech."
    },
    {
        "name": "Sarah (The Python Pivot)",
        "resume": "Senior Data Scientist. Expert in Python, PyTorch, and AI. Leading a small research team. No experience with Microservices or Kafka."
    },
    {
        "name": "John (The Legacy)",
        "resume": "Engineering Manager with 15 years experience. Worked on Monolithic Java applications. Managed large teams. No Cloud/AWS experience."
    }
]
