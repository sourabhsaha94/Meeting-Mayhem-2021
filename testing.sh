#!/bin/bash

#echo Creating 100 users

counter=1
while [ $counter -le 100 ]
do
	name="a$counter"
	password="p$counter"
	email="$name@$password"
	curl -G -d "name=$name" -d "password=$password" -d "email=$email" http://localhost:5000/createuser
	((counter++))
done

echo Logging 100 users

counter=1
while [ $counter -le 100 ]
do
	email="a$counter@p$counter"
	password="p$counter"
	json="{\"email\":\"$email\",\"password\":\"$password\"}"
        curl --header "Content-Type:application/json" -d "$json" http://localhost:5000/login
        ((counter++))
done

echo All done

