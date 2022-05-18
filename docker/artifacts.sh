#!/bin/bash

pybabel extract -F shweb/services/rest/babel.cfg -o shweb/services/rest/messages.pot shweb
pybabel update -i shweb/services/rest/messages.pot -d shweb/services/rest/translations
pybabel compile -d shweb/services/rest/translations