FROM python:3.9.7-slim-buster

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

# install main dependenices
RUN pip install histomicstk==1.2.10 --find-links https://girder.github.io/large_image_wheels
RUN pip install flywheel_gear_toolkit
RUN pip install fw_core_client
RUN pip install flywheel-sdk
RUN pip install scikit-image==0.19.3
RUN pip install numpy==1.23.5

# copy main files into working directory
COPY run.py manifest.json $FLYWHEEL/
COPY fw_gear_feature_extraction ${FLYWHEEL}/fw_gear_feature_extraction 
COPY ./ $FLYWHEEL/

# start the pipeline
RUN chmod a+x $FLYWHEEL/run.py
RUN chmod -R 777 .
ENTRYPOINT ["python","/flywheel/v0/run.py"]
