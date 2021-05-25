# Tello Drone

Based on `https://github.com/dji-sdk/Tello-Python`

## Purpose
- learn to control a dji / rzye robotics drone

-----------------------------

## Stack 
- docker
- python 2.7

-----------------------------

## Setup

### Environment
- `yarn build-image` or `docker build -t tello .`

-----------------------------

## Hello world
- `yarn start-container`
- in your container run:
    - `python ./hello-world.py`
- make changes to `python ./hello-world.py` locally.

- in your container run:
    - `python ./hello-world.py` again

- local changes get reflected in the docker container.
- this will be important for keeping iteration time low.

-----------------------

## Tello Hello World
- `yarn start-container`
- turn on tello and connect to it's wifi network on your laptop

- in your container run:
    - `cd Tello-Python/Single_Tello_Test && python tello_test.py command.txt`
    
- update `command.txt` 
- more commands
    - `https://dl-cdn.ryzerobotics.com/downloads/tello/0228/Tello+SDK+Readme.pdf`

----------------------------

## Tello Video

### Setup Mac GUI proxy
- `brew install socat`
- `brew install xquartz`

### Run
- `socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"`
- `open -a Xquartz`

- turn on tello and connect to it's wifi network on your laptop

- get your ip address: 
    - `ifconfig en0` 

- `yarn start-container`

- inside the container:
    - copy deps: `yarn copy-deps:pose`
    - start: `cd ./Tello-Python/Tello_Video_With_Pose_Recognition && python main.py` 
    
------------------------------

## Tello Video with pose recognition
- based on `https://github.com/dji-sdk/Tello-Python`

### Setup Mac GUI proxy
- `brew install socat`
- `brew install xquartz`

### Run
- `socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"`
- `open -a Xquartz`

- turn on tello and connect to it's wifi network on your laptop

- get your ip address: 
    - `ifconfig en0`

- `yarn start-container`

- inside the container:
    - copy deps: `yarn copy-deps:pose`
    - start: `cd ./Tello-Python/Tello_Video_With_Pose_Recognition && python main.py`

-----------------------------

## Tello Video with pose recognition - 2.0
- based on `https://github.com/dji-sdk/Tello-Python`

### Setup Mac GUI proxy
- `brew install socat`
- `brew install xquartz`

### Run
- `socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"`
- `open -a Xquartz`

- turn on tello and connect to it's wifi network on your laptop

- get your ip address:
  - `ifconfig en0`

- `yarn start-container`

- inside the container:
  - copy deps: `yarn copy-deps:2`
  - start: `cd ./Tello-Python/Tello_Video_With_Pose_Recognition_2 && python index.py`
  
-----------

## Tello local

### ensure that your terminal has camera permissions but running these

brew install ffmpeg
ffmpeg -f avfoundation -list_devices true -i ""
ffmpeg -f avfoundation -i "0:0" -vf  "crop=1024:768:400:800" -pix_fmt yuv420p -y -r 10 out.mov
sudo killall VDCAssistant
imagesnap -w 2 snapshot.png -d "HD Pro Webcam C920"

## need
- brew install wget
- conda

`yarn env:create`
`yarn env:activate`
`yarn env:install`
`yarn start:local`



## References 
https://cntnr.io/running-guis-with-docker-on-mac-os-x-a14df6a76efc
