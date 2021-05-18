#!/bin/bash
for i in {1..500}
do
	./testing-2.sh >> output$i.txt &
done
