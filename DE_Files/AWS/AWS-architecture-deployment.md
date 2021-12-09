# AWS Architecture

![schema](/images/POC_V1-2.JPG)



# Processing steps

- Data collection of chat activity in log files
- Storage of the logs in a S3 bucket
- new file triger the data processing
- a lambda clean the data
- a lambda do the sentiment annalysis
- a lambda associated to a SQS buffer the data (time serie generation)
- a docker image (hosted in ECR) with a prediction model is run on a lambda
- a lambda send the last data point and the futur predictions to the twitch extension



   
    