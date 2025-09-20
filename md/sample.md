## Abstract

Cloud data lakes often store large volumes of logs, metrics, or event data in AWS S3. The formats vary:
newline-delimited ``JSON`` (often gzipped), ``CSV``, or more optimized columnar formats like ``Parquet``. Traditionally, querying
this data meant spinning up heavyweight tools (Athena, Spark, Presto, EMR).

But what if you could query the data instantly, from your laptop, without standing up an
entire cluster? Enter DuckDB.

DuckDB is an embedded analytical database — think “SQLite for analytics” — with first-class support for Parquet, JSON,
CSV, and remote storage like ``S3``. The dreams come true.

In this post, we’ll explore:

- Querying gzipped JSON files directly from S3
- Comparing JSON vs Parquet vs CSV performance
- Joining local and remote datasets
- Calling HTTP APIs from DuckDB (yes, you can!)

## Getting Started with DuckDB


``DuckDB`` works in Python, R, Go, Nodejs, Rust, Java, CLI, or as a C library. If you a fan of `JetBrains DataGrip` it also can includes duckdb connector. The DuckDB CLI (Command Line Interface) is a single, dependency-free executable. Installation is simple.

```shell
pip install duckdb
```

```shell
brew install duckdb
```

### 1. Querying Local FS

After starting cli, we can easily access ``csv file`` stored in local FS, querying them as they are regular tables,
using SQL operators and predicates. Very often we need to open some csv file, analyze its structure or extract particular raws based on prodicate.Here I'm querying data from local FS csv file with limit:

```sql
SELECT *
FROM read_csv_auto('/tmp/oxford_5000.csv') LIMIT 100;
```

|column0 | word    | type               | cefr | phon\_br   | phon\_n\_am | definition                                                                                                 | example                                                        |
|:--------|:--------|:-------------------|:-----|:-----------|:------------|:-----------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|
| 0       | a       | indefinite article | a1   | /ə/        | /ə/         | used before countable or singular nouns referring to people or things that have not already been mentioned | a man/horse/unit                                               |
| 1       | abandon | verb               | b2   | /əˈbændən/ | /əˈbændən/  | to leave somebody, especially somebody you are responsible for, with no intention of returning             | abandon somebody, The baby had been abandoned by its mother.   |
| 2       | ability | noun               | a2   | /əˈbɪləti/ | /əˈbɪləti/  | the fact that somebody/something is able to do something                                                   | People with the disease may lose their ability to communicate. |

### 2. Querying Gzipped JSON on AWS S3

Suppose you have logs or events data that is ingested into DataLake by pipeline and they are stored in ``AWS S3`` partitioned by date with a virtual path and also gzipped json. This is very common architecture.

Duckdb works perfectly with partitions, based on query it can access proper paths and also unzip the data. It auto-detects
``schema``, even across multiple files.

`` s3://my-bucket/logs/year=2025/month=09/day=16/data.json.gz ``

Directly querying data with DuckDB:

```sql
SELECT *
FROM read_json_auto(
  's3://my-bucket/logs/*.json.gz',
  format = 'json',
  compression = 'gzip'
     );
```

The beauty is that we do not need to bootstap any engine, create AWS IAM permissions, add service and pay for them - just use cli tool that is local on your machine.

#### Duckdb extensions and AWS credentials

 > The httpfs extension supports reading/writing/globbing files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.
 {: .prompt-tip }

To query S3 firstly we need to add and enable extensions:

```sql
-- set s3 compatibility
INSTALL
httpfs;
LOAD
httpfs;
```

> The httpfs filesystem is tested with AWS S3, Minio, Google Cloud, and lakeFS. Other services that implement the S3 API (such as Cloudflare R2)
{: .prompt-tip }

After setup add S3 credentials via environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) or IAM role of the profile (more prefered).

#### Adding secrets

```sql
-- set aws creds
INSTALL
aws;
LOAD
aws;

CREATE
SECRET env_dev (
    TYPE s3,
    PROVIDER credential_chain,
    REFRESH auto
);

SET
s3_region='us-east-1';
SET
s3_access_key_id='ASIAXXXXXX';
SET
s3_secret_access_key='';
SET
s3_session_token='';
```

#### Another option is to use exisitng AWS profiles and switch between them

```sql
CALL load_aws_credentials('dev');
CALL load_aws_credentials('prod');
```

Check credentials:

```sql
SELECT *
FROM FROM duckdb_secrets();
```

### 3. Parquet and CSV on S3

DuckDB shines with columnar formats like Parquet:

```sql
SELECT user_id, COUNT(*) AS events
FROM read_parquet('s3://my-bucket/logs/*.parquet')
GROUP BY user_id
ORDER BY events DESC;
```

#### For CSV:

```sql
SELECT *
FROM read_csv_auto('s3://my-bucket/data/*.csv.gz');
```

Parquet is much faster and smaller than JSON/CSV, but the magic is that DuckDB handles them all.

### 4. Loading Data from S3 storing locally in Parquet or other format

```sql
-- dev
CREATE
OR REPLACE VIEW events_2025_block AS
SELECT *
FROM read_json_auto(
  's3://events/block-events/block/year=2025/month=*/day=*/hour=*/*.json.gz',
  filename = true, -- adds a _filename column
  hive_partitioning = 1, -- pulls year/month/day/hour from the path into columns
  format = 'newline_delimited' -- omit if they’re arrays/objects; keep if NDJSON
     );

SELECT *
FROM events_2025_block
WHERE
  action == 'data-verified'
  LIMIT 10;
```

Writing extracted data from S3 to local FS and automatically converting into ``Parquet`` :

```sql
COPY events_2025_block TO '/tmp/dev.s3.events.parquet' (FORMAT parquet);

SELECT *
FROM '/tmp/dev.s3.events.parquet'
WHERE action == 'data-verified'
ORDER BY created_at DESC
  LIMIT 100;
```

### 5. Local + Remote Joins

You can join S3 data with local datasets:

```sql
WITH s3_data AS (
SELECT user_id, timestamp
FROM read_parquet('s3://my-bucket/events/*.parquet')
),
local_users AS (
SELECT * FROM read_csv_auto('users.csv')
)
SELECT u.name, COUNT(*) AS actions
FROM s3_data s
JOIN local_users u USING(user_id)
GROUP BY u.name;
```

This means you don’t need to ETL everything into a central DB just to query.

### 6. Calling HTTP APIs from DuckDB

DuckDB supports reading remote HTTP URLs directly. I have JSON-based ``aws news`` for different topics hosted at my ``github pages``, let's call it to get latest aws architecture news:

```sql
SELECT *
FROM read_json_auto('https://tsypuk.github.io/aws-news/news/architecture.json')
WHERE title LIKE '%Lambda%' LIMIT 50;
```

| title                                                                        | link                                                                                                                    |
|:-----------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------|
| How Zapier runs isolated tasks on AWS Lambda and upgrades functions at scale | https://aws.amazon.com/blogs/architecture/how-zapier-runs-isolated-tasks-on-aws-lambda-and-upgrades-functions-at-scale/ |
| How Launchpad from Pega enables secure SaaS extensibility with AWS Lambda    | https://aws.amazon.com/blogs/architecture/how-launchpad-from-pega-enables-secure-saas-extensibility-with-aws-lambda/    |

Same queries work with Parquet/CSV hosted over HTTPS. This is handy for blending APIs + S3 data.

### 7. Using standard DBs like MySQL Postgres

```shell
INSTALL postgres;
LOAD postgres;
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, READ_ONLY);
```


## Why DuckDB?

- Lightweight: No cluster, runs anywhere (laptop, container, Lambda).
- Format-flexible: JSON, CSV, Parquet, ORC.
- Fast: Vectorized execution engine, optimized for analytics.
- Great for ad-hoc exploration of data lakes.

## When to Use Athena vs DuckDB

- Use Athena when: queries must run at scale, multiple teams need SQL access, complex analytics require a lot of cpu/memory resources that are not available of local machine
- Use DuckDB when: you need quick exploration, prototyping, data science, or embedding analytics in an app, access to QA/STG env where not so big volume size

## Conclusions

DuckDB is like a Swiss Army knife for data lakes. With just a few lines of SQL, you can query gzipped JSON from S3, join
it with local CSVs, compare with Parquet, and even call APIs. It’s lightweight, fast, and great for both prototyping and
production embedding.

Try it next time you need to peek inside your S3 bucket without firing up a full big-data stack.

## Links:

- [https://duckdb.org/docs/stable/core_extensions/httpfs/s3api.html](https://duckdb.org/docs/stable/core_extensions/httpfs/s3api.html)
