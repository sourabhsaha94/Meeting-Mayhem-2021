Follow the below steps to set up the Meeting Mayhem application

1. Use the command "git clone https://github.com/akritianand93/Meeting-Mayhem-2021.git" to clone from the repository

2. Go to "Meeting-Mayhem-2021\Meeting-Mayhem-2021\api\venv" folder in the command prompt and run the following commands:
    
    1. python -m venv venv
    2. venv\Scripts\activate
    3. pip install flask python-dotenv
    4. pip install requests

This will install everything required to run the flask server

3. Execute the command "flask run" to start the flask server

4. To install the dependencies to run react application, go to "Meeting-Mayhem-2021\react-flask-app" in the command prompt and run the following command:
    
        "npm install"
        
    This will install the node modules required to run the application
    
5. Execute the command "npm start" to the start the react application

The application will be opened in the browser, ready to use !
