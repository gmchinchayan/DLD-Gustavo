# AWS Architecture

![schema](/DE_Files/AWS/images/POC_V1-2.JPG)



## Processing steps

- Data collection of chat activity in log files
- Storage of the logs in a S3 bucket
- new file triger the data processing
- a lambda clean the data
- a lambda do the sentiment annalysis
- a lambda associated to a SQS buffer the data (time serie generation)
- a docker image (hosted in ECR) with a prediction model is run on a lambda
- a lambda send the last data point and the futur predictions to the twitch extension



  ## Deployment steps

- deploy the EC2 (see twitch-import-AWS.md)

- Create the S3 bucket "twitch-logs"

- Create IAM role "S3toLambda" with the "AWSLambdaBasicExecutionRole" strategy and create "S3getLambdaInvoke"  stategy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::twitch-logs",
                "arn:aws:s3:::twitch-logs/*"
            ]
        }
    ]
}
```

- Create the Lambda "CleanLog" with "S3toLambda" role and deployment package.

- Add "CleanLog" to the S3 PUT notification event

- Create IAM role "ChainLambda" with the "ChainLambda" strategy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "lambda:InvokeFunction",
                "lambda:InvokeAsync",
                "logs:CreateLogGroup"
            ],
            "Resource": [
                "arn:aws:logs:*:954227610772:log-group:*",
                "arn:aws:lambda:*:954227610772:function:*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "logs:PutLogEvents",
            "Resource": "arn:aws:logs:*:954227610772:log-group:*:log-stream:*"
        }
    ]
}
```

- Create "pred" lambda with "ChainLambda" role and deployment package.

- Create IAM role "LambdaStoreToQueue" with the "ChainLambda" strategy and the "SendPredToQueue" strategy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:GetQueueUrl",
                "sqs:ChangeMessageVisibility",
                "sqs:SendMessage",
                "sqs:GetQueueAttributes",
                "sqs:SetQueueAttributes"
            ],
            "Resource": "arn:aws:sqs:*:954227610772:*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "sqs:ListQueues",
            "Resource": "*"
        }
    ]
}
```
- Create "buffer" lambda with "LambdaStoreToQueue" role and deployment package.

- Create the "history.fifo" SQS as FIFO and content based deduplication enabled. Add the acess strategy:

```
{
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::954227610772:root"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:eu-north-1:954227610772:history.fifo"
    },
    {
      "Sid": "__sender_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::954227610772:role/LambdaStoreToQueue"
      },
      "Action": "SQS:SendMessage",
      "Resource": "arn:aws:sqs:eu-north-1:954227610772:history.fifo"
    },
    {
      "Sid": "__receiver_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::954227610772:role/LambdaStoreToQueue"
      },
      "Action": [
        "SQS:ChangeMessageVisibility",
        "SQS:DeleteMessage",
        "SQS:ReceiveMessage"
      ],
      "Resource": "arn:aws:sqs:eu-north-1:954227610772:history.fifo"
    }
  ]
}
```

- Build the docker image with the steps descibed in "steps.txt" (extensions_ebs\Sentiment_POC\timepred\container) with your user id (your aws cli must be configured)

- Create the "timepred" lambda with the ECR image and with "ChainLambda" role.

- Create the "broadcast" lambda with the default role and the deployment package.

You are ready to run the application with the EC2 script.



    