

FROM freesurfer/freesurfer:6.0

COPY license.txt /opt/freesurfer

RUN pip3 install flywheel-sdk

ENV FLYWHEEL=/flywheel/v0

RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py

ENTRYPOINT ["python run.py"]