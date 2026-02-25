####
# Name: generate_courses.py
# Date: 2/23/2026
# Description: This script generates a list of courses based on predefined templates and saves them to a JSON file.
####

#importing necessary libraries
import json
import random

# Definig the course templates
course_topics = [
    "Introduction to Computer Science", "Financial Modeling", "Data Science Fundamentals", "Machine Learning Basics",
    "Web Development with Python", "Cybersecurity Essentials", "Cloud Computing Overview", "Artificial Intelligence Concepts",
    "Blockchain Technology", "Mobile App Development", "Digital Marketing Strategies", "Project Management Principles",
    "Entrepreneurship and Innovation", "Graphic Design Fundamentals", "Human-Computer Interaction", "Software Engineering Practices", "Database Management Systems", "Network Security", "Big Data Analytics", "Natural Language Processing", "Robotics and Automation"
    "public speaking", "creative writing", "philosophy of science", "environmental science", "sociology of technology", "psychology of learning", "history of computing", "ethics in technology", "quantum computing", "virtual reality development"
]

formats = ["video lectures", "interactive workshops", "self-paced modules", "live webinars", "group projects", "case studies", "hands-on labs"]
levels = ["Beginner", "Intermediate", "Advanced"]

# Function to generate a random courses
#Description: This function takes an integer input 'x' which is used to generate a unique course ID. It randomly selects a topic, format, level, and duration for the course. It also creates a description based on the selected format and compiles all the information into a dictionary representing the course.
def generate_course(x):
    topic = random.choice(course_topics) 
    frmt = random.choice(formats) 
    level = random.choice(levels) 
    duration = random.randint(5, 90) #generating a random duration between 5 and 90 mins

    # getting a simple description based on the format of the course 
    description = {
        "video lectures": f"Watch and learn {topic} concepts explained step by step.",
        "interactive workshops": f"Participate in interactive workshops to practice {topic} skills in real-time.",
        "self-paced modules": f"Self-paced modules for flexible learning at your own pace on {topic}.",
        "live webinars": f"Live webinars with industry experts and Q&A sessions on {topic}.",
        "group projects": f"Collaborative group projects to apply learned concepts in real-world scenarios on {topic}.",
        "case studies": f"In-depth case studies to analyze and solve real-world problems on {topic}.",
        "hands-on labs": f"Hands-on labs to practice and apply skills in a controlled environment on {topic}."
    }

    # Compiling all the course information into a dictionary and returning it kinda like tokenizing the course attributes into a structured format for easy storage and retrieval
    return {
        "id": f"course_{x:03d}", #generating a unique course ID where 3 digits are used to represent the course number
        "title": f"{level.capitalize()} {topic.title()} - {frmt.title()}", #generating a course title based on the level, topic, and format
        "topic": topic, 
        "format": frmt, 
        "level": level, 
        "duration_minutes": duration, 
        "description": description[frmt],
        "tags": [topic, frmt, level, f"{duration} mins"], #generating tags for the course based on its attributes
        #generating a searchable text field that combines all relevant information about the course for easy searching and indexing
        "searchable_text" : f"{topic} {level} {frmt} {duration} minutes. {description[frmt]}" 
    }

courses = [generate_course(i) for i in range (1, 501)] #500 mock courses

#Writing the generated courses to a JSON file
with open("courses.json", "w") as file:
    json.dump(courses, file, indent=2) #dumping the list of courses to a JSON file with an indentation of 2 

print(f"Generated {len(courses)} courses")