# Image classification / AIMD Buffer - Inference server.

This project explores the use of AIMD (Adaptive Increase / Multiplicative Decrease) as a congestion control mechanism 
for Machine Learning inference task.


### Environment
- Python 3.11.11
- Poetry 1.8.4 (Poetry 2.x.x seems to be buggy as of writing this)


### Run
1. `poetry install` to install dependencies and set up server script program.
2. `poetry run server` to launch the server on `localhost:3000`

In the future there will be tests, hopefully I will get to them soon :).


### Notes
- We elected to use Tensorflow as the ML backend.
- Use Python 3.8 - 3.11 for Tensorflow support. This project uses Python 3.11.11
- For MacOS Silicon users, install `pip install tensorflow tensorflow-metal` for Tensorflow to utilize Apple Silicon GPU.


### TODOs:
- Move buffer to Redis: Buffer is currently implemented directly on-memory.
- Write tests
