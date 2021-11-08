# BigPT

## Dependencies
- Python 3.5.2
- MongoDB 4.2.12
- pymongo 3.9.0
- ANTLR4 (Java target)
- TensorFlow 1.10.0
- Numpy 1.13.3
- Keras 2.2.2

## Construct feature vector for all the programs in the database
(this process is offline, all the feature vectors will be saved)

`sh db_feature_vector.sh path_to_your_db`

## Train auto-encoder and build QTM

`python3 qtm.py`

## Active training of QTM
(can be used when the user is able to label some data)

First preprocess the database to get statistics for sampling (offline):

`python3 statistics.py`

Then select samples for labeling based on user's requirements:

`python3 select_sample.py source_language target_language label_amount_threshold`

Once a small labeled dataset has been created, QTM can be updated actively:

`python3 qtm_AL.py source_language target_language`

## Retrieve translation for your input (with feedback mechanism)

`sh translate_retrieval.sh path_to_input target_language`

If there is a new user feedback, just simple run the above command again.

