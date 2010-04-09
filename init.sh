#!/bin/sh
bin/paster serve --stop-daemon development.ini
bin/paster setup-app development.ini
bin/paster serve --daemon development.ini
