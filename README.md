# MiniAuth: Secure Session & Application Launcher

## Project Description

MiniAuth is a proof-of-concept desktop application that manages user sessions and controls access to a predefined list of programs. The project consists of a simple GUI built with Tkinter and a simulated Flask API server that handles authentication and authorization. Upon successful login, the user is granted a temporary session, during which they can only launch the specified applications. When the session expires, all launched programs are automatically closed.

### Key Features

* **Authentication:** User login via a simple GUI.
* **Session Management:** Real-time monitoring of session duration with an on-screen timer.
* **Access Control:** Restriction of application launches to an approved list from the server.
* **Automated Shutdown:** Automatic termination of all launched applications upon session expiration.
* **User Interface:** A straightforward and intuitive graphical interface.
* **Event Logging & Reporting** All key events are logger to an SQLite database and can be exported to CSV via a command-line flag.

## Project Structure

```bash 
├── data/
│   ├── offline_cache.json
│   ├── logs.csv
│   ├── logs.db
│   └── allowed_apps.json
├── mock_api/
│   └── app.py
├── src/
│   ├── api_client.py
│   ├── logger.py
│   ├── main.py
│   ├── offline_cache.py
│   ├── process_control.py
│   ├── session_manager.py
│   ├── ui_login.py
│   └── ui_session.py
├── .gitignore
├── requirements.txt
└── README.md
```

* `data/`: Stores configuration files, such as the list of allowed applications.
* `mock_api/`: Contains the simulated Flask API server used for testing and demonstration.
* `src/`: The core source code for the desktop application.
* `main.py`: The main entry point for the desktop application.

## Requirements

### 1. Python
Ensure you have Python version 3.6 or higher installed.

### 2. Dependencies
Install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```
## How to Run Project

### 1. Start the API server:
Navigate to the mock_api directory and run the Flask server:
```bash
cd mock_api
python app.py
```
### 2. Start the desktop application:
Open a new terminal window, navigate to the src directory, and run the application:
```bash
cd src
python main.py
```
### 3. Login Credentials:
Use the following credentials to log into the application:
- Email: `test@example.com`
- Password `1234`

### 4. Optional features
To generate a CSV report of all logged events, run:
```bash
python main.py --generate-csv-report 
```
To print out a local cache of last session, run:
```bash
python main.py --show-offline-cache
```

## Note

- Log files and cache directories are ignored by Git (see `.gitignore`) to keep the repository clean and avoid committing sensitive or unnecessary files.

## TODO

- [x] Logging: Implement a logging system to save events to an SQLite database and provide an option to export to CSV.

- [x] Offline Cache: Develop a module to store the last successful session details.

- [x] Session Control: Ensure automatic application closure when the session expires and add a logout button.

- [ ] UI Security: Implement UI security features, such as preventing window minimization.

- [ ] Refactoring & Testing: Conduct code refactoring and write end-to-end tests for all core functionalities.

- [ ] Documentation: Write a comprehensive README.md with detailed instructions and a project description.

- [ ] UI/UX: Apply minor improvements to the user interface and overall user experience.

- [ ] Demo: Record a video demonstration showcasing the application's features.
