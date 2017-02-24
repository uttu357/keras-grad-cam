FROM ubuntu:14.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && \
    apt-get install -y python-pip python2.7 python2.7-dev python-opencv
RUN pip install --upgrade pip
RUN pip install virtualenv
ADD requirements.txt /
ADD app.py /
ADD cvfy.py /
ADD grad-cam.py /
RUN virtualenv ./venv
RUN /bin/bash -c "source /venv/bin/activate \
    && pip install -r requirements.txt"
RUN cp /usr/lib/python2.7/dist-packages/cv2.so /venv/lib/python2.7/site-packages/

ENTRYPOINT source /venv/bin/activate \
           && python app.py
