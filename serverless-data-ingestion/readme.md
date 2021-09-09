# Serverless Data Ingestion using Step Functions, Lambda & S3

## About:
In my earlier post, I spoke abot how to ingest rapidly changing table schemas while staging to datawarehouse.
https://nraghu366.medium.com/how-to-dynamically-adapt-and-ingest-rapidly-changing-table-schemas-while-staging-to-datawarehouse-a3ba32f0fba9

In this post, let us see how to ingest data using servless components of Amazon by using scripts from earlier project with minimal changes.


## Scenario:
1. We get differential updates of several tables in a database compressed as a zip file.
2. zip file consists of data files and JSON files which has destination tablename with partition and sort keys.
3. There can also be multiple zip files which are holding data and JSON from different tables of a database.
4. EventBridge triggers the Lambda to Scan S3 files and create a list of valid zip files.
5. The response is consumed by another Lambda to open the zip files without unzipping and create a list of filenames and their destination with partition keys.
6. Finally, we have a ingestion Lambda which is mapped dynamically to the filelist and spawns as many as required and lazy load(using itertools) the data file inside zip.


## Steps of StepFunction
Lets the functioning of each step in the State machine.

### Lamba - ScanS3
This is the first state to be executed, this Lambda scans the S3 bucket for zip files. The S3 bucket to be scanned is configured as environment variable of the Lambda.

### Check Response
This is a _Choice_ type step which helps quits the job if no files are present. Since Amazon bills each state transistion, this step helps us to save money by not invoking all preceeding steps.

### Safe Exit
This is _Succeed_ type step to safe exit from the cycle if no files are present.

### Create Ingestion List
This invokes a Lambda in the backend to open the zip files and create a list of filenames to be ingested. We used a third-party library `smart_open` to open and analyze the files inside the zip. The response has the filenames and the destination DynamoDB table with partition key.

### Data Ingestion
This is the final step which dumps data file inside zip to DynamoDB. It is a _Map_ type step which dynamically invokes a Lambda function as many times as files are in queue to be ingested. It starts with creating the table with partition key and then opens the zip file and lazy loads the data file using `itertools.islice`. Table name, partition key and sort key are available in the zip as a JSON.

## Alternatives
Amazon provides `Glue` which can automatically generate code to perform the ETL tasks. It has friendly interface to set up crawlers to connect to data sources, classify and ingest data. It also maintains the data catalogs for future use. However, Glue works best with compressed data file and might not be a good fit when the source is a zip file with multiple data files.

Amazon also provides `Data Pipeline` to move all the data into preferred data warehouse without having to write any code. It launches and manages the lifecycle of EMR clusters and EC2 instances to execute jobs thus making not a serverless. AWS also charges for the infrastructure created by Data Pipeline to process the files along with the Pipeline charges.

## Pricing
Lets have glance on the pricing of the services used
1. __EventBridge__: There are no additional charges for rules and all state change events published by AWS services are free.

2. __Lambda__ counts a request each time it starts executing in response to an event notification or invoke call, including test invokes from the console. It charges $0.20 per 1M requests and $0.0000166667 for every GB-second duration. Additional charges will be incurred when Lambda function utilizes other AWS services or transfers data. For example, if your Lambda function reads and writes data to or from Amazon S3, you will be billed for the read/write requests and the data stored in Amazon S3.

3. __Step Functions__ Express Workflows counts a request each time it starts executing a workflow, and you are charged for the total number of requests across all your workflows. It charges about $1 per 1M requests.

4. __AWS Glue__ charges $0.44 per Data Processing Unit hour, billed at every second of use. Data Processing Units are consumed when you run crawlers or jobs. $1 is also charged per 100,000 objects that you manage in the data catalog and also $1 per million requests to the data catalog

5. __AWS Data Pipeline__ charges a fee of $1 per month per pipeline if it is run more than once a day and $0.68 per month per pipeline if run one time or less per day. You are also required to pay for EC2 and any other resources you may consume

_Note: Since this article more focuses on Ingestion methods, I have excluded listing the pricing of datastores like S3, RDS, DynamoDB_

## Best Practices
1. Though I chose the destination as DynamoDB for the ease of NoSQL, I personally observed dumping data into RDS was much faster where the data is dumped into table, however, DynamoDB checks for duplicate partition keys which is an overhead.
2. DynamoDB Streams is also a good option to dynamically invoke Lambda which can replace Map step of Step Functions.
