# DCATS – Digital Class Attendance Tracking System

##  Project Overview
The **Digital Class Attendance Tracking System (DCATS)** is a web-based application developed for the Namibia University of Science and Technology (NUST).  

The system helps lecturers record student attendance digitally and allows students to view their attendance records بسهولة and accurately.

This project was developed as part of the **Software Processes (SPS611S)** course.

##  Group Members
- Philipus Nefuma (223010006)  
- Esther Gabriel (222101717)  
- Elikana Joba (223081965)  
- Kelvin Gora (221026916)  
- Markus NFT (214021254)  


##  Problem Statement
Traditional attendance methods (paper registers and roll calls) are:
- Time-consuming  
- Prone to errors  
- Difficult to manage and analyze  

DCATS solves this by providing a **digital, reliable, and efficient attendance system**.


##  Objectives
- Develop a digital attendance tracking system  
- Allow lecturers to record attendance electronically  
- Store attendance data securely  
- Enable students to view attendance records  
- Generate attendance reports  


##  Features
- Lecturer and student login system  
- Record student attendance (Present/Absent)  
- View attendance records  
- Generate attendance reports  
- Search student attendance history  
- Admin management (students, lecturers, courses)  


## System Architecture
The system follows a **3-layer architecture**:

1. **Presentation Layer (UI)**
   - Login page  
   - Dashboard  
   - Attendance pages  

2. **Application Layer (Logic)**
   - Authentication  
   - Attendance processing  
   - Report generation  

3. **Database Layer**
   - Stores students, lecturers, classes, and attendance records  


##  Database Entities
- Lecturer  
- Student  
- Class  
- Attendance  


##  Technologies Used
- **Backend:** Python (Flask MVC)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS  
- **Testing:** pytest, pytest-flask  
- **Browser Testing:** Microsoft Edge  


##  Software Development Model
This project uses the **Scrum (Agile) model**:
- Work divided into **sprints**
- Continuous improvement after each sprint
- Strong teamwork and communication


##  Testing
- 53 automated test cases executed  
- 100% pass rate 
- Manual testing for:
  - Registration  
  - Admin panel  

### Testing Types:
- Unit Testing  
- Integration Testing  
- System Testing  


##  Functional Requirements
- Lecturer login  
- Record attendance  
- View attendance records  
- Student access to attendance  
- Generate reports  
- Store attendance data  
- Search student records  


##  Non-Functional Requirements
- Usability  
- Performance  
- Security  
- Reliability  
- Maintainability  
- Availability  


##  How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/dcats.git# dcats
