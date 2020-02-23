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

## Running the tests

by running the ``

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

