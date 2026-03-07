# Mitly

Url shortener app with FatAPI inspired by Bitly

### Table of contents

* [System Design](#system-design)
* [Setup](#setup)


# System Design

## Delivery Framework

![delivery_framework.png](media/delivery_framework.png)

## -------------------- 1. Requirements

### Functional Requirements

Core features

1. create a short url from a long url
    - [optional] support a custom alias
    - [optional] support expiration time
2. redirection to the original url from the short one

### Non-functional Requirements

Qualities like Scalability, Latency, Security, Fault Tolerance

1. Ensure **uniqueness**   
   We must guarantee that each short URL maps to exactly one long URL, otherwise users could be redirected to an
   unexpected website.

2. Low **latency** on redirects (~200ms)

3. **Scale** to support:
    - 100M daily active users (DAU)
    - 1B stored URLs

4. **CAP Theorem** (Brewer's theorem says that **distributed systems** can guarantee only 2 guaranties at the same
   time)  
   **AP + eventual consistency** (Tech: Cassandra, DynamoDB)  
   eventual consistency means that updates propagate to all replicas over time  
   Because we would prefer the system to be always working, despite a node failure. Having the most recent data as soon
   as possible is not priority.
    - ✅ Guarantee **[A]vailability**: (информацията винаги е налична, но не винаги е актуална) Every request receives
      a (non-error) response, even if a node has dropped, without the guarantee that it contains the most recent
      write/data.
    - ✅ Guarantee **[P]artition tolerance (устойчивост при разделяне)**: System continues to work even if network
      communication between nodes is interrupted
    - ❌ **[C]onsistency**: (информацията е винаги актуална, но не винаги е налична) All clients/nodes see the same data
      at the same time  
      Usecases: Banking, Stocks, Ticket booking system, etc.  
      Strong consistency guarantees that the following example will **NOT** happen:  
      p1 from EU buys last ticket to a concert and p2 buys it at the same time from US.

💡Note : [P]artition Tolerance is usually not optional in modern distributed systems because networks will eventually
fail

## -------------------- 2. Core Entities

- Original url
- Short url
- [optional] User

## -------------------- 3. API or Interface

💡 Tip: Functional Requirements hint the endpoints

- shorten url  
  POST /urls > short_url

```json
{
  "original_url": "https://github.com/miray-mustafov/mitly",
  "optional_alias": null,
  "optional_expiration_time": null
}
```

- redirect  
  GET {short_url} > redirect to original_url

```json
{
  "short_url": "https://mitly/asd123"
}
```

## -------------------- 4. Data Flow (skipped)

## -------------------- 5. High-level Design

![basic_high_level_design.png](media/basic_high_level_design.png)

## -------------------- 6. Deep Dives

todo

# Setup
Local setup for Windows OS

### Configure and activate python virtual environment
```shell
uv venv --python 3.13
```

### Activate venv
```
.venv\Scripts\activate
```
todo