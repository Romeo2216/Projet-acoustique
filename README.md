Listening Test Application
Overview
The Listening Test Application is designed for conducting auditory experiments by presenting users with customized audio stimuli. The application provides an interactive user interface for participant registration, instructions, and test execution, while processing audio signals in the background.

Prerequisites
To successfully set up and run the project, the following prerequisites must be met:

1. Software Requirements
Python: Version 3.11 or earlier (Python 3.12 is not recommended due to potential library incompatibilities).
Operating System: Compatible with Windows, macOS, and Linux.
2. Python Dependencies
The following Python libraries are required and are automatically installed via the provided install.py script:

numpy
scipy
librosa
sqlite3 (comes pre-installed with Python)
matplotlib
tkinter (comes pre-installed with Python on most systems)
3. Input Directories
Ensure the following directories exist and are populated with valid audio files:

Impulse_Response: Contains impulse response files.
Excitation_Files: Contains excitation signals.
HRTF: Contains Head-Related Transfer Function (HRTF) files.
OBTF: Contains Outer-Brain Transfer Function (OBTF) files.
4. File Structure
The project relies on the following folder and file organization:


project_root/
├── Db_Folder/
│   ├── result.db
│   ├── signal.db
├── Excitation_Files/
├── HRTF/
├── Impulse_Response/
├── OBTF/
├── Signal_Response/ (generated during execution)
├── IHM_Folder/
│   ├── IHM.py
│   ├── IHM_sujet.py
│   ├── IHM_instruction.py
├── init_db.py
├── signal_manager.py
├── install.py
├── main.py
├── requirements.txt
Installation Instructions
Clone the Repository:

git clone <repository_url>
cd <repository_name>
Install Dependencies: Run the provided installation script:

python install.py
This will:

Verify the Python version.
Upgrade pip, setuptools, and wheel.
Install all dependencies listed in requirements.txt.
Verify Input Files:

Populate the directories (Impulse_Response, Excitation_Files, HRTF, OBTF) with the required audio files before running the application.
Running the Application
Launch the application using the following command:

python main.py
Troubleshooting
Database Errors:
Ensure signal.db and result.db in the Db_Folder/ directory are not locked by another process.
If necessary, delete these files and rerun the main.py script to recreate them.
Missing Dependencies:
Reinstall dependencies with:
bash
Copier le code
pip install -r requirements.txt
Incorrect Python Version:
Use Python 3.11 or earlier.
