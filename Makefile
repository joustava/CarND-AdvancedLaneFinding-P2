test:
	pipenv lock --dev --requirements > requirements.txt
	docker build \
	-t joustava/advanced_lane_finding:dev \
	-f ops/Dockerfile .
	docker run -it \
	  --env PYTHONDONTWRITEBYTECODE=1 \
	  -v $(PWD)/assets:/app/assets \
	  -v $(PWD)/:/app joustava/advanced_lane_finding:dev green -vvv

build:
	pipenv lock --requirements > requirements.txt
	docker build \
	-t joustava/advanced_lane_finding \
	-f ops/Dockerfile .

run:
	docker run -it \
	  --env PYTHONDONTWRITEBYTECODE=1 \
	  -v $(PWD)/assets:/app/assets \
	  -v $(PWD)/:/app joustava/advanced_lane_finding $(cmd)

.PHONY: build test run	