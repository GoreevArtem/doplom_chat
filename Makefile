build:
	docker-compose build

up:
	docker-compose up -d

debug:
	docker-compose up --build

stop:
	docker-compose down

down:
	docker-compose down -v

rebuild:
	docker-compose down -v && docker-compose up --build