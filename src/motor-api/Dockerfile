FROM balenalib/raspberrypi3-python

# Enable cross building of ARM on x64 hardware, Remove this and the cross-build-end if building on ARM hardware.
RUN [ "cross-build-start" ]

RUN apt update -y
RUN apt install gcc -y

RUN apt-get install -y \
        build-essential \
        python3-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        zlib1g-dev \
        libjpeg-dev \
        libatlas-base-dev \
        wget

RUN  apt-get -y update
RUN  apt-get -y install python3-rpi.gpio


RUN pip3 install --upgrade pip 
RUN pip3 install --upgrade setuptools 
RUN pip3 install --upgrade wheel 
RUN pip3 install --upgrade RPi.GPIO 


ENV PATH="/home/api/.local/bin:${PATH}"


WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# End cross building of ARM on x64 hardware, Remove this and the cross-build-start if building on ARM hardware.
RUN [ "cross-build-end" ]

COPY app/ /code/app

CMD ["python", "app/main.py"]
