# althea
ALgoriTHms Exposed through a RESTful API
![mail](images/althea.jpeg)

*althos: "healing"*

## Purpose
The purpose of this application is to make exposing algorithms via a RESTful
API easier. After a clinical risk algorithm has been vetted, there are potentially
many consumers of this algorithm. For instance, other researchers may be interested
in coming up with new state-of-the-art algorithms, clinical operations may wish to use
the algorithm to identify cohorts for studies, or in the case of computable phenotypes,
real-time event detection. By exposing the algorithm via a RESTful API, we enable all
consumers of the algorithm(s) to utilize the power of the algorithm. In the past, the algorithm
had to be coded in whatever language each consumer used most often (e.g. SAS, PHP, JavaScript, etc.). Now
each consumer can call one central source of truth, ensuring reproducibility and consistency.

##Installation
At this time, *althea* is purely a python package. It is our hope to allow submission of other types of
code in the future. Two avenues for installation are available:

####github
```
git clone https://github.com/benneely/althea.git
cd ./althea
python setup.py install
```

####pip
```
pip install althea
```
