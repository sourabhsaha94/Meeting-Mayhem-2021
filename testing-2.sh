#!/bin/bash
START="$(date +%s%3N)"
#get recipients
#curl http://3.133.147.109:5000/getrecipients
#login
#json="{\"email\":\"sourabh\",\"password\":\"password\"}"
#curl --header "Content-Type:application/json" -d "$json" http://3.133.147.109:5000/login
#send message
#json="{\"sender\":\"akritia1@umbc.edu\",\"receiver\":\"akritia1@umbc.edu\",\"message\":\"hello\"}"
#curl --header "Content-Type:application/json" -d "$json" http://3.133.147.109:5000/sendmessage
#get message
curl http://3.133.147.109:5000/getmessages?receiver=akritia1@umbc.edu
DURATION=$[ $(date +%s%3N) - ${START} ]
echo ${DURATION}
