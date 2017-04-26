#WASPMQ

An application to demonstrate communication between distributed applications or microservices. 

It contains the following components

- a Flask frontend web server, 
- a RabbitMQ server, 
- a backend worker

The frontend places messages on the queue while the backend consumes the message
