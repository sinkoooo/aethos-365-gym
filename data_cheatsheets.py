# data_cheatsheets.py
# Staff+ Battle Cards & Master Comparison Matrices

BATTLE_CARDS = [
    {
        "id": "bc-01",
        "num": "CARD #01",
        "cat": "Event Streaming",
        "q": "Why did Apache Kafka eliminate Apache ZooKeeper in favor of KRaft?",
        "ans": "ZooKeeper was an external metadata bottleneck. When a broker crashed in a cluster with millions of partitions, leader re-election took minutes because state had to be transferred from ZooKeeper into the controller. KRaft (Kafka Raft) embeds consensus directly into Kafka's internal event logs, scaling clusters to 10M+ partitions and enabling sub-second leader failover."
    },
    {
        "id": "bc-02",
        "num": "CARD #02",
        "cat": "Real-Time Protocols",
        "q": "How does Zoom or WebRTC handle packet loss without freezing audio?",
        "ans": "Zoom uses UDP with Forward Error Correction (FEC) and adaptive jitter buffers. When packets drop, redundant parity packets reconstruct missing audio frames on the fly without waiting for TCP retransmission (which would cause noticeable human conversational lag)."
    },
    {
        "id": "bc-03",
        "num": "CARD #03",
        "cat": "Distributed SQL",
        "q": "Why does Google Spanner not require read locks for linearizable reads?",
        "ans": "TrueTime bounds physical clock uncertainty across global datacenters to <= 7ms using atomic rubidium clocks and GPS. By executing 'Commit-Wait' on writes, read transactions can simply query an MVCC snapshot at a past timestamp (t <= now - epsilon) with strict serializability and ZERO read locks!"
    },
    {
        "id": "bc-04",
        "num": "CARD #04",
        "cat": "Fintech & Ledgers",
        "q": "How does Stripe prevent double-charges on network timeout?",
        "ans": "Clients supply a unique 'Idempotency-Key' in HTTP headers. Stripe atomically reserves this key in Redis and checks PostgreSQL ledger state. If a client retries after a network drop, Stripe recognizes the duplicate key and immediately returns the previously recorded response without re-charging the credit card."
    },
    {
        "id": "bc-05",
        "num": "CARD #05",
        "cat": "Caching Architecture",
        "q": "What is the XFetch algorithm for Cache Stampede?",
        "ans": "Instead of waiting for an item to expire, XFetch uses probabilistic early expiration: e^(-beta * delta * ln(rand())) > expiry - now. As TTL approaches zero, background worker threads probabilistically refresh the cache before it ever misses, completely eliminating cache stampedes."
    },
    {
        "id": "bc-06",
        "num": "CARD #06",
        "cat": "Storage Engines",
        "q": "Why do LSM-Trees beat B+ Trees for write-heavy workloads?",
        "ans": "B+ Trees perform random in-place disk page updates, bottlenecked by disk IOPS. LSM-Trees append writes sequentially to an in-memory MemTable and commit log, flushing sequentially to immutable disk SSTables. Sequential disk writes on NVMe reach 3,500+ MB/s, vastly outperforming random I/O."
    },
    {
        "id": "bc-07",
        "num": "CARD #07",
        "cat": "Social Graphs",
        "q": "How do you solve the Twitter Celebrity Fanout problem?",
        "ans": "Hybrid timeline model: Normal users (<25k followers) use Fanout-on-Write (push into followers' Redis lists for O(1) read). Celebrities (>25k followers) use Fanout-on-Read: their tweets are pulled at request time and merged with the user's cached timeline in memory."
    },
    {
        "id": "bc-08",
        "num": "CARD #08",
        "cat": "Distributed Locks",
        "q": "Why is Redis Redlock criticized by Martin Kleppmann?",
        "ans": "Redlock relies on physical system clock synchronization. A Stop-The-World GC pause or network delay can freeze a client while its TTL expires in Redis; another client acquires the lock, leading to dual writers and data corruption. Fencing tokens issued by consensus protocols (etcd) are required for safety."
    },
    {
        "id": "bc-09",
        "num": "CARD #09",
        "cat": "Geospatial Systems",
        "q": "Why did Uber create H3 hexagons instead of Geohashes?",
        "ans": "In rectangular grids or Geohashes, diagonal neighbors are sqrt(2) times farther than orthogonal neighbors, distorting radius queries. In a hexagonal grid, all 6 neighbors share identical edge lengths and center-to-center distances, enabling clean O(1) concentric K-ring radius expansions."
    },
    {
        "id": "bc-10",
        "num": "CARD #10",
        "cat": "Message Brokers",
        "q": "When should you choose Kafka over RabbitMQ?",
        "ans": "Choose Kafka for high-throughput append-only event streaming (1M+ msgs/sec), message replayability, log retention, and stream processing (Flink). Choose RabbitMQ for complex AMQP routing (topic/headers), individual message ACK/nack, and discrete task queue dispatch."
    },
    {
        "id": "bc-11",
        "num": "CARD #11",
        "cat": "Distributed Consensus",
        "q": "What is Split-Brain and how is it mathematically prevented?",
        "ans": "Split-brain occurs when a network partition cuts a cluster in half, and both sides elect independent leaders that accept conflicting writes. It is prevented by enforcing Quorum: any decision or leader election requires a strict majority (N/2 + 1) of all nodes, meaning only one partition can ever form a quorum."
    },
    {
        "id": "bc-12",
        "num": "CARD #12",
        "cat": "Microservices",
        "q": "Why is Two-Phase Commit (2PC) an anti-pattern in microservices?",
        "ans": "2PC is a blocking protocol. If the coordinator crashes during the commit phase, database locks remain held indefinitely across multiple services, choking throughput. Modern distributed architectures replace 2PC with the Saga pattern and asynchronous compensating events."
    }
]

print(f"Loaded {len(BATTLE_CARDS)} Staff+ Battle Cards.")
