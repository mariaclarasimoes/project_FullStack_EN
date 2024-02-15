## HOW TO RUN

1) Install all python libraries listed in the `requirements.txt` file.

2) After cloning the repository, access the terminal and execute the commands described below:

    * Create a virtual environment -> Command in the terminal: python -m venv env
    * Activate the virtual environment -> Command in the terminal FOR WINDOWS: .\env\Scripts\activate (For MAC and LINUX, another command is used)
    * Install the requirements -> Command in the terminal: pip install -r requirements.txt
      If necessary, update using the command in the terminal: python.exe -m pip install --upgrade pip
    * Run the API using the reload parameter, which will automatically restart the server after a change in the source code.
      Command in the terminal: flask run --host 0.0.0.0 --port 5000 --reload
      
    * Open [http://localhost:5000/#/](http://localhost:5000/#/) in the browser to check the status of the running API.