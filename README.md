

                        Title- QSOL

link to video: https://youtu.be/KnRHs3OnYig


Web application used by organization to enable their customers to jon queues and track their positions in queues.

                        USAGE

Fist, you need to have a source code editor such as vscode or a command line interface of your choice such the CS50 IDE. Then, you need to download the folder with all the contents of the project. Then you need to cd into that folder of the project.

    execute:   cd project

Once you are in the folder project, you need to create a virtual environment to work with by executing:

    python3 -m venv venv

This command creates a new folder named venv, you can call the folder whichever name you like but I have used venv in this case.
Check if the folder is made after executing the command.

You then need to activate the virtual environment by executing the command below:

    source venv/bin/activate

The command above will activate the virtual environment and you should be able to see (venv) appearing in your terminal



                    INSTALLING REQUIREMENTS

After setting up the virtual environment, you will need to install all the required extensions for the program to run

I have included all the requirements in a file (requirements.txt). What you need to do is simply execute the command below to install all the requirements.

pip install -r requirements.txt

Afterwords you are set to run the project

Normally one needs to set a FLASK_APP environment variable, however I have it already set in a file with a flaskenv extension.

Therefore, you simply need to execute;

    flask run


                            USERS
After following the above steps, the web app will be running on the local host. Thus you can create account and login. You can also book a ticket and see your postion in queue and also delete ticket.

                            ADMIN
My web app has  admin users, admin portal is not visible to  users and thus you need to insert /admin in the link address

see below:
             http://127.0.0.1:5000/admin

After that, you will be prompted for a password which is provided in the config.py
        admin password: pass

Afterwards, you will be able to navigate the admin side of the web application.







