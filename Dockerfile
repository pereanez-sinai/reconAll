

FROM freesurfer/freesurfer:6.0

COPY license.txt /opt/freesurfer

RUN pip3 install flywheel-sdk

ENV FLYWHEEL=/flywheel/v0

RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py

RUN python3 -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'

#ENTRYPOINT ["python3 ${FLYWHEEL}/run.py"]
