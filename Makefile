test:
	docker

build:
	pipenv lock --requirements > requirements.txt
	docker build -t joustava/advanced_lane_finding -f ops/Dockerfile .

run:
	docker run -it -v $(PWD)/assets:/app/assets -v $(PWD)/src:/app joustava/advanced_lane_finding $(cmd)

.PHONY: run test build	