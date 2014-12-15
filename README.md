Getting Started
---------------

Recommend installing pew to manage virtual environments (can't remember if you need to sudo):

    pip install pew


Once pew is installed create a new virtual environment:

    pew new bbc_voice_api


This will launch into the virtual environment in a subshell.  Clone this git repository:

    git clone git@github.com:tomcollins/bbc-voice-api.git
    cd bbc-voice-api


Set the project directory so when you later issue "pew workon bbc_voice_api" it will return
you to the correct directory.

    pew setproject .


Run the setup.py command to install the dependencies:

    python setup.py develop


To start the built in web server run:

    pserve development.ini --reload


Developing
----------

* Add dependencies into the setup.py script
* Add named routes into bbc_voice_api/__init__.py reference them from bbc_voice_api/views.py
