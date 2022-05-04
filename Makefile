run:
	docker-compose up -d --build 
	echo "Waiting mariadb to be up"
	sleep 10
	docker exec dev_web_1 python TiersMonde/manage.py migrate
	docker exec dev_web_1 bash -c "python TiersMonde/manage.py shell < script.py"
	docker exec dev_web_1 python TiersMonde/manage.py loaddata db.json
	docker exec -d dev_web_1 python TiersMonde/manage.py runserver 0.0.0.0:8000
