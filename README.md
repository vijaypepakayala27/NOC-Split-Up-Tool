# NOC Ticket Splitting Tool

## Overview
The idea of dividing VIP and HP tickets to evenly share the workload among Network Operations Center (NOC) agents is a good one. However, Agents have to manually split a large number of support tickets at the start of their shifts takes a bit of time and can lead to mistakes, especially when the tickets are stored in different formats like CSV files or ZIP files containing CSVs.

The **NOC Ticket Splitting Tool** is a web application designed for Network Operations Center (NOC) agents to help streamline the morning process of splitting tickets. 
The tool allows agents to upload CSV files/ZIP files with CSV files containing tickets and automatically distribute these tickets among team members based on specified names.

## Features
- **User Authentication**: Secure login page for NOC agents.
- **Ticket Splitting**: Upload VIP and HP tickets in CSV format, and split them among team members by providing their names.
- **Multiple Type File Upload Support**: Supports CSV files/ZIP files with CSV file uploads with intuitive UI feedback.
- **Logout Functionality**: Ensures secure sessions with a logout option.

## Tech Stack
- **Python**: Backend logic with Flask framework.
- **HTML/CSS**: Frontend structure and styling. (Build using GPT) 
- **JavaScript**: Animations and form interaction logic.
- **GSAP**: Used for smooth animations on the webpage.
- **These are the key packages:**
    Flask: A web framework.
    Werkzeug: A WSGI utility library, typically used with Flask.
    pandas: For data manipulation and analysis.

## File Structure
- `app.py`: The main backend script containing the Flask application & Ticket Split Up logic.
- `index.html`: The main page where NOC agents can upload CSV files and split tickets.
- `login.html`: The login page for user authentication.
- `styles.css`: The CSS file for styling the pages, including the layout, colours, and animations.
- `logo.png`: The Telnyx logo is displayed on the login page.
- `requirements.txt`: Contains the necessary libraries needed to run the code 

## Setup and Installation

### Clone the Repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

### Install Dependencies:
Ensure you have Python installed. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Run the Application:
Start the Flask application:

```bash
python app.py
```

The application should now be running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Access the Tool

- Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.
- Log in using the default credentials:
  - **Username**: admin
  - **Password**: password
- After logging in, you'll be redirected to the ticket-splitting tool.

## Usage
- **Login**: Enter the provided credentials to access the tool.
- **Upload CSV Files**: Upload the VIP and HP tickets CSV files on the main page.
- **Split Tickets**: Enter the names of the agents (comma-separated) to distribute the tickets. Click on the "Split Tickets" button.
- **Logout**: Once done, click the "Logout" button to securely end your session.

## Notes
- The tool is designed to take ZIP files or plain CSV files  only. 
- The login credentials are hard-coded for demonstration purposes and should be updated before deploying in a production environment.
- You should remove the line " if __name__ == '__main__': app.run(debug=True) " block when deploying your Flask application to a production environment, like PythonAnywhere, or any other production server that uses a WSGI server (such as Gunicorn, uWSGI, or the built-in   WSGI server provided by PythonAnywhere).
- This tool has been developed to the best of my ability, but it may still have bugs or vulnerabilities. Please don't hesitate to reach out if you discover any issues.

This tool is deployed on pythonanywhere for testing purposes 
https://vijaypepakayala27.pythonanywhere.com/ 
