# Flask-Philo-PynamoDB

![Flask-Philo Logo](https://raw.githubusercontent.com/Riffstation/Flask-Philo-Core/master/documentation/source/_static/banner_1.png)

Flask-Philo extension that connects to DynamoDB AWS

## Motivation

[Flask-Philo-Core](http://flask-philo-core.readthedocs.io/en/latest/) implements
simple funcionality for building flask based applications. This project provides  [PynamoDB](https://pynamodb.readthedocs.io/en/latest/) support for Flask-Philo.


## Running Test Suite

We use docker and docker-compose for development, therefore you will need to install those two tools if you
want to run the test suite for this project. The following command runs the tests:


```
cd tests
python3 run_tests
```

## Resources

* [PynamoDB](https://pynamodb.readthedocs.io/en/latest/)
