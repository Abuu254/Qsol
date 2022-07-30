
                        QSOL DESIGN

routes.py

I separated all the routes into one file, routes.py. This because I needed to separate everything so that I can work more organized and be able to locate any error with an ease during the development period. The route file simply consists of all the routes of the application and nothing else.

forms.py

I decided to separate forms that I need for the users into one file. I believe this design is better in the sense that we can easily validate issues relating to what we need from the form. For example we can easily use validators that come with flask such as EqualTo, and Email(), in addition we can add our own function that validate specific things, like a function that checks if a username or email is already in user.


models

I also separated all the models into one file and added function that will work on each models like in users. There is function check_password which will be checking passwords making the code neat and organized. This is where I declare the columns needed in specific table. When I want to change structure of a table, I just need to change it from this table and then use:

flask db migrate
flask db ugrade

In this case, I will have my migrations folder which will store my data during upgrading and downgrading.


helpers.py


 I also included helpers function so that my code can easily be followed without much repetition.

config.py

I also made a configuration file where I included all my confuguration like config for sending mail, reset passwords and error messages. This design is better since it will be easier to change the configuration if you need to.

error.py

I also included an error file where I handle the errors during the running of the application

I also have the __init__.py where I initialize the application. I believed that it would be easier to track everything if I separated everything in a separate file.

Whenever I encoutered an error during the development of the app, I could easily trace back to where the error started and resolve it. 