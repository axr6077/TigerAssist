# TigerAssist

In our society, there is a persistent language barrier between the hearing and the deaf. To bridge this gap, we created TigerAssist, a machine learning-based application that converts alphabets of the American Sign Language to English language text. The program utilizes machine learning algorithms as well as virtual reality, computer vision and big data processing to parse live sign language gestures to text. 

## Getting Started

Software: 
* Install Python >= 3.0 
* Install PyCharm or any text editor 
* Clone the repo 

Hardware: 
* Install LeapMotion* sdk

*If you're using Python version >= 2.7.0, you will need to compile leapPython as described here: 
https://support.leapmotion.com/hc/en-us/articles/223784048

### Prerequisites
* LeapMotion Controller 
* A Computer!
```
pip install -r requirements.txt 
```
## How to run it
```
python main.py 
```

## Built With

* opencv - Image processing 
* sklearn - Machine Learning algorithms 
* Leap - Used to interract with the Leap Controller
* Other preprocessing libraries like numpy, scikit, re, itertools, requests

## Contributing

Feel free to submit pull requests directly.

## Versioning

We use PyCharm libs and pip for versioning. 

## Languages Utilized

* Python 
* C++

## Features
* Versatility: The model can be trained with any set of lexicons: say convert a gesture to the word "beer" (**challenged by Constellation   Brands**) 
* Easy accessibity services for the Deaf
* Increased accuracy due to two input sources (LeapMotion Controller and Webcam) - Leap VR (0.64) and Computer Vision (0.73)
* HoG algorithm and SVM model boosted learning accuracy

## Future Development

* Make camera wait until hand is detected 
* Train with larger dataset to recognize more Hand Gestures 
* Add a text to speech feature for virtual communication
* Port python backend to be used in Android app for portability 
* Better classifier between light sources and white background 

## Authors

* **Ayush Rout** 
* **Brandon Chen**
* **Jack Xu**


## References
* https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html 
* https://support.leapmotion.com/hc/en-us/articles/223784048

## Demo
https://drive.google.com/open?id=1uE14NQjI--NLLnG2NqrXQ2nJ0pkpzZQM
