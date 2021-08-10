### What is this about?
Finding the correct database for an application is not easy; sometimes, it takes a lot of effort and brainstorming of application architects to identify the best pick for the requirements. This article does not discuss the scenarios for a particular database but might be handy if you are planning to host a datastore/cache on AWS. This article also believes that you have prior knowledge of DBaaS and have already shortlisted a datastore viz Cache/SQL/NoSQL.

Amazon is now offering a wide range of datastores, that cater almost all the needs an application would require. Let us start with whether you need a cache or database and delve more as per the need.

<DIAGRAM>

## Cache
If you are looking for a Cache store for your application, Amazon offers the two best ElastiCache services Memcached and Redis. Memcached is chosen to cache simple data structures, however, the latter has more capabilities to cache advanced data structures and has significantly more features than Memcached. The below link compares both the services and should help you to choose the best.
https://aws.amazon.com/elasticache/redis-vs-memcached/
You can also find more info here:
https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/SelectEngine.html


## SQL - OLTP
For traditional applications, Amazon offers RDS & AuroraDB. Though RDS and AuroraDB serve a similar purpose to host the most reputed database engines (PostgreSQL, MariaDB & SQL Server), the underlying storage structure and replication factors differ, which makes AuroraDB much powerful and expensive.
This Amazon blog sheds light on how and when to choose between RDS & AuroraDB.
https://aws.amazon.com/blogs/database/is-amazon-rds-for-postgresql-or-amazon-aurora-postgresql-a-better-choice-for-me/


## SQL - OLAP
Snowflake is one of the most widely adopted cloud services for data warehousing. Though it is a partner offering on Amazon(also available on Microsoft and Google cloud), it scales up instantly, making it a perfect choice for low-latency queries and semi-structured data like JSON, XML and parquet.
Amazon native products in this segment are Redshift and Athena, which also fulfil the DW requirements. Redshift is used in predefined schema use cases, whereas Athena is for similar and contrast scenarios.
Athena is primarily a SQL layer on top of the data in S3, which is quick to easy to set up.
Redshift and Snowflake are a petabyte-scale data warehouse with MPP(Massively Parallel Processing) architecture to handle analytical workloads on massive datasets.

## NoSQL
Amazon offers a wide range of products for NoSQL datastores, from a simple DynamoDB to Ledger type QLDB. Let us learn more about which datastore works best for the use case.

### DynamoDB
DynamoDB is a key-value and document type database. If you have identified most of your access patterns and the object relationships are not complex, then DynamoDB is the best fit. It scales up blazingly fast and can query millions of queries per second. You can also connect DynamoDB with DAX(DynamoDB Accelerator) for ultra-fast retrieval of data. DAX is an in-memory cache for DynamoDB that delivers up to a 10 times performance improvement without the need to refactor application logic.

### DocumentDB
It is an implementation of MongoDB on AWS. Choose this if you already have an existing MongoDB instance and wants to migrate to serverless on Amazon. It is also the best choice if the access patterns are not identified, or have complex JSON structures.
Amazon offers a free migration(AWS Database Migration) of your self-managed MongoDB database to DocumentDB with virtually no downtime.

### Amazon Keyspaces
It is a Wide-column datastore available on AWS. Amazon Keyspaces is a scalable, highly available, and managed Apache Cassandra–compatible database service.

### Amazon Neptune
Graph type datastore is the best fit if you are working with complex and dynamic relationships. Amazon Neptune is a fast, reliable, fully-managed graph database service and supports the popular graph query languages Apache TinkerPop Gremlin and W3C’s SPARQL

### Amazon Timestream
If you are working on weather analysis which requires you to store and analyse a huge number of time-series data points per day then Timestream should be your pick. Per Amazon, Timestream data can be used for visualisation and machine learning. It saves you time and cost in managing the lifecycle of time series data by keeping recent data in memory and moving historical data to a cost-optimized storage tier based upon user-defined policies.

### QLDB
If your application requires a verifiable history of all data changes but does not involve multiple, untrusted parties, the QLDB is a great fit. If you have a use case for distributed ledgers or blockchain then check (Amazon)[https://aws.amazon.com/managed-blockchain/]

## Marketplace
In addition to the native products offered by Amazon, there is also Marketplace which is a platform to buy and use products created and maintained by Third-party Software vendors. Despite not being backed by Amazon, a few architects prefer these if Amazon products do not meet their requirements.
Please note that there is always a trade-off between Amazon native products and Partner products, native products integrate with the rich suite of AWS cloud services and built-in security, and Partner products offer best-in-class features.
