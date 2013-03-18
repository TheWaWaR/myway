#!/usr/bin/env bash

ROOT=/root/projects/myway

ps aux | grep uwsgi
echo "-----------"
pkill -KILL uwsgi
sleep 1
ps aux | grep uwsgi
echo "=---------="

ps aux | grep supervisord
echo "-----------"
pkill -KILL supervisord
sleep 3
ps aux | grep supervisord
echo "=---------="

supervisord -c ${ROOT}/deploy/supervisor.conf
sleep 2
ps aux | grep supervisord
echo "-----------"

