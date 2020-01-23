

FROM freesurfer/freesurfer:6.0

COPY license.txt /opt/freesurfer

RUN pip3 install flywheel-sdk
