run:
	docker-compose up --build

stop:
	docker-compose down

test:
	docker-compose exec backend pytest

