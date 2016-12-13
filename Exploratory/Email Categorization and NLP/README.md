## Automatic E-mail Categorization

The focus of this project is to accurately classify e-mails into folders based on e-mail content.  This is a Natural Language Processing challenge that uses a Bag-of-words model to convert text documents into numerical feature vectors.  Two standard classifiers were trained and tested on the email foldering task.   I found this to be an interesting angle to tackle the Enron Corpus, the largest public domain database in the world containing real-world email messages.  The version used contains over 500,000 emails from about 150 users, mostly senior management at Enron. You can visit [here](https://en.wikipedia.org/wiki/Enron_scandal) to learn more about the Enron scandal.  You can get a copy of the dataset [here](https://www.cs.cmu.edu/~./enron/).  

### Installation

* Install the requirements using `pip install -r requirements.txt`

### Requirements

* pandas
* matplotlib
* seaborn
* scikit-learn
* numpy
* ipython
* scipy

### References

1. [Bekkerman et al. (Ron Bekkerman, Andrew McCallum and Gary Huang). *Automatic Categorization of Email into Folders: Benchmark Experiments on Enron and SRI Corpora*](http://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1217&context=cs_faculty_pubs)

2. [Bryan Klimt and Yiming Yang. *The Enron Corpus: A New Dataset for Email Classification Research*](http://nyc.lti.cs.cmu.edu/yiming/Publications/klimt-ecml04.pdf)






