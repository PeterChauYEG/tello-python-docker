FROM python:2

WORKDIR /usr/src/app

RUN pip install cmake
RUN apt-get update -y && apt-get install libboost-all-dev libavcodec-dev libswscale-dev python-numpy python-matplotlib -y
RUN pip install opencv-python==4.2.0.32 pillow
RUN apt-get install python-imaging-tk -y

COPY ./Tello-Python/Tello_Video/h264decoder ./h264decoder
RUN mkdir ./h264decoder/build
RUN cd ./h264decoder/build && cmake .. && make
RUN cp ./h264decoder/build/libh264decoder.so ../

COPY ./Tello-Python/Tello_Video_With_Pose_Recognition/model /usr/src/model
RUN cd /usr/src/model && ./getModels.sh
