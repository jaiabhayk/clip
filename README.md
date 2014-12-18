1) External Dependencies:- Install NLTK (http://www.nltk.org/install.html) and Vowpal Wabbit (http://hunch.net/~vw/)
2) Edit the vw_interface.py and change the variable "path_to_vw" to point vw 
3) Running the tool:- sh run_sentiment_analyzer.sh (optional train and test files, otherwise default will be taken). This will do k-fold cross validation and will also perform training on the training set and test on the test set.
