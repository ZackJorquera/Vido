# Vido

Video but shorter

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

You will need to install ffmpeg. We are using the ffmpeg python bindings in the ffmpeg-python library. 
```
pip install ffmpeg-python
```

You will also need to install the ffmpeg executable from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
You will need to set up this executable as a system variable in order for everything to work properly.

In windows add the path to the Path system variable.
In linux for mac you need to create an alias.

additionally google cloud vision will need to be downloaded which can be done with
```
pip install google-cloud-speech
```
more instruction can be found online.

Adding env variables
in pycharm. Run -> config > env variable
add GOOGLE_APPLICATION_CREDENTIALS with value of the cred json file
