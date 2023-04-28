FROM continuumio/miniconda3

COPY ./sample_ingester_api_min.yml /



RUN mkdir /pages && mkdir /assets && mkdir /additional_files

COPY ./additional_files/* /additional_files/

COPY ./*.py ./

RUN conda env create -f sample_ingester_api_min.yml 

WORKDIR ./

EXPOSE 4999

SHELL ["conda", "run", "-n", "sample_ingester_api_min", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "sample_ingester_api_min", "python", "./parentapi.py"]