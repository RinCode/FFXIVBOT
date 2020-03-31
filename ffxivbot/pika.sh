#!/bin/sh
kill `ps -ef | grep "pika_rabbit" | grep -v grep | awk '{print $2}'`
python pika_rabbit.py 1>pika.log 2>&1 &
while :
do
        if [ `grep -c "ERROR" pika.log` -eq '0' ]; then
                kill `ps -ef | grep "pika_rabbit" | grep -v grep | awk '{print $2}'`
                python pika_rabbit.py 1>pika.log 2>&1 &
                echo "Found!"
        fi
        sleep 1m
done
