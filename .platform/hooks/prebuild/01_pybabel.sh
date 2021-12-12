#!/bin/bash

pip3 install flask-babel==2.0.0
pybabel extract -F shweb/babel.cfg -o shweb/messages.pot shweb
pybabel update -i shweb/messages.pot -d shweb/translations
pybabel compile -d shweb/translations
