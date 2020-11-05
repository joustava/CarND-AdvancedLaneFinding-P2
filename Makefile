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

notebook:
	docker run --rm -v $(PWD)/assets:/home/jovyan/work/assets -p 8888:8888 jupyter/scipy-notebook

profile:
	scalene alf/processor.py --profile-all --html --outfile profiling.html

run:
	export DISPLAY='127.0.0.1:0.0'
	xhost + 127.0.0.1

	docker run -it \
		--env DISPLAY=host.docker.internal:0.0 \
	  --env PYTHONDONTWRITEBYTECODE=1 \
		--net=host --ipc=host \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
	  -v $(PWD)/assets:/app/assets \
	  -v $(PWD)/:/app joustava/advanced_lane_finding $(cmd)

.PHONY: build test run	