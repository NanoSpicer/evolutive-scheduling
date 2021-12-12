.ONESHELL:

run:
	python3 code/main.py

run-once:
	# Change the argument with the test you would like to run
	python3 code/main.py 3


start-visor:
	echo "Esto puede tardar un rato debido a que descargara dependencias graficas"
	npm i
	npm start &
	cd visualizador-horarios
	npm i
	npm start 

