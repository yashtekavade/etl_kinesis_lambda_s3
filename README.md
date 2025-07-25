# AWS Kinesis Data Stream ETL Pipeline

````markdown

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using AWS services:

- **Amazon Cognito** for authentication (used with Kinesis Data Generator)
- **Amazon Kinesis Data Stream** for streaming data ingestion
- **AWS Lambda** for processing Kinesis records
- **Amazon S3** for storing processed data

---

## Architecture Overview

![Architecture Diagram](docs/architecture-diagram.png)  
*Diagram showing Cognito → Kinesis Data Generator → Kinesis Data Stream → Lambda → S3*

---

## Prerequisites

- AWS CLI configured with appropriate permissions
- AWS Account with permissions for Lambda, Kinesis, S3, Cognito, and CloudFormation
- Python 3.x (for local Lambda testing and packaging)

---

## Setup Instructions

### 1. Deploy Cognito User with CloudFormation

1. Navigate to the `cloudformation/` directory.
2. Deploy the stack:

```bash
aws cloudformation deploy \
  --template-file cognito-kdg-user.yaml \
  --stack-name KDG-Cognito-User \
  --parameter-overrides Username=yourusername Password=yourpassword \
  --capabilities CAPABILITY_NAMED_IAM
````

3. After stack creation, get the Kinesis Data Generator URL from stack outputs.

---

### 2. Create Amazon Kinesis Data Stream

1. Create a Kinesis data stream named `tbsm-data-stream` in **On-demand** mode via AWS Console or CLI.

---

### 3. Deploy Lambda Function

1. Package your Lambda function:

```bash
cd lambda
zip -r ../lambda_function.zip .
cd ..
```

2. Create or update your Lambda function via AWS Console or CLI.

3. Attach required IAM policies to Lambda execution role:

   * `AmazonS3FullAccess`
   * `AWSLambdaBasicExecutionRole`
   * Custom policy for Kinesis read permissions (if needed).

---

### 4. Configure Lambda Trigger

* Add the Kinesis Data Stream (`tbsm-data-stream`) as an event source trigger for your Lambda.
* Set batch size to 100.

---

### 5. Send Test Data Using Kinesis Data Generator

* Open the Kinesis Data Generator URL.
* Configure:

  * Region: `ap-south-1` (Mumbai)
  * Stream: `tbsm-data-stream`
  * Records per second: `100`
  * Template:

```json
{
  "sensorId": {{random.number(50)}},
  "currentTemperature": {{random.number({"min": 10, "max": 150})}},
  "status": "{{random.arrayElement(["OK", "FAIL", "WARN"])}}"
}
```

* Generate \~500 records.

---

### 6. Verify Data in Amazon S3

* Check the configured S3 bucket (`tbsm-kinesis-etl-bucket`).
* You should see JSON files named by sequence number, each containing a sensor record.

---

## Lambda Function Overview

The Lambda function decodes Kinesis data, parses JSON, writes files locally in `/tmp/`, uploads them to S3, and cleans up.

---

## Notes

* Replace placeholders with your actual bucket names and AWS account details.
* Ensure Lambda has sufficient IAM permissions.
* Use CloudFormation stack outputs for URLs and ARNs.


```


