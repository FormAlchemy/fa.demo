#!/bin/sh
cd $HOME/fa.demo
$PWD/bin/paster serve --stop-daemon development.ini
rm -f $PWD/development.db
$PWD/bin/paster setup-app development.ini
$PWD/bin/paster serve --daemon development.ini
