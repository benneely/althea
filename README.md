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
---------
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

## API
----------
The goal is to have ALTHEA available via two api's:
  1. python
  2. RESTful

Currently is is only available via (1)

#### Python API
To start playing with Althea, two risk algorithms can be loaded by default:
```
from althea import Metadata, Model
#add_examples is a named parameter that loads two algorithms that ship with Althea:
#Framingham 30 year CVD risk algorithm and the 2013 ACC/AHA Pooled Cohorts equation
models = Metadata(add_examples=True)
models_in_db = models.available_models()
#'deb9cc20-603f-4926-8ab9-66bb88d2ce0a'
#'cf8c7c12-0097-45ca-99cb-babcdd204d0e'

framingham = Model(models_in_db[0].get('model_uuid'))
framingham.score(sbp=120,male='No',smoke='Yes',tc=60,hdlc=110,age=33,diab='No',trtbp='No')
```
