import json
import boto3

def lambda_handler(event, context):
    print(event)
    
    #get the parameters
    data=event["body"]
    Channel=event["Channel"].strip()
    
    #access queue an get prediction history
    SQS_client = boto3.client('sqs')

    q = SQS_client.get_queue_url(QueueName='history.fifo').get('QueueUrl')
    
    response = SQS_client.receive_message(QueueUrl=q)
    
    print(response.keys())
    
    history=[]
    
    # if there is no messages, initate at all 0
    if 'Messages' not in response.keys():
        history = [0 for k in range(60)]
        
    else:
        #if message exist, get the data and delete the message
        print('recieved')
        print(json.loads(response['Messages'][0]['Body'])['history'])
        history = json.loads(json.loads(response['Messages'][0]['Body'])['history'])
        if history: del_response = SQS_client.delete_message(QueueUrl=q, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
        
    #update the history  
    history.pop(0)
    history.append(float(data))
    
    print(history)
    
    #store the updated history
    response = SQS_client.send_message(QueueUrl=q, MessageBody = json.dumps({"history": json.dumps(history)}), MessageGroupId = Channel )  

    
    #send the history for time prediction
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
	FunctionName='timepred',
	InvocationType='Event',
	LogType='None',
	Payload=json.dumps({"body": history,"newPoint": float(data),"Channel":Channel}))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
