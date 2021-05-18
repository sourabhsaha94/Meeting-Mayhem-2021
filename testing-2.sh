#!/bin/bash
START="$(date +%s%3N)"
curl http://localhost:5000/getrecipients
DURATION=$[ $(date +%s%3N) - ${START} ]
echo ${DURATION}
