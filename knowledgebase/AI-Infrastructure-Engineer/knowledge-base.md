# AI Infrastructure Engineer Knowledge Base

## Core Concepts

### GPU Serving Systems
- GPU instance types and memory considerations
- Model quantization and batching
- Multi-tenant serving vs. dedicated inference
- Serving frameworks: Triton, NVIDIA NeMo, BentoML, Ray Serve

### Inference Pipelines
- Request routing and preprocessing
- Model selection and prompt batching
- Latency optimization and throughput tuning
- Caching and result reuse

### Vector Databases
- Embedding generation and storage
- Similarity search algorithms (cosine, dot product, L2)
- Indexing strategies for large corpora
- Operational considerations: replication, backups, consistency

### Distributed Systems
- Kubernetes architecture for AI workloads
- Service mesh, networking, and load balancing
- Data pipelines and messaging systems
- Fault tolerance, retries, and circuit breakers

### Observability
- Metrics: latency, error rate, throughput, GPU utilization
- Logging and tracing for inference workflows
- Alerting and SLO-based monitoring
- Profiling and root cause analysis

### Scaling and Cost Control
- Horizontal vs. vertical scaling
- Autoscaling policies and capacity planning
- Spot instances, reserved capacity, and serverless options
- Cost monitoring and optimization best practices

## Practical Reference

### Recommended Tools
- Kubernetes, Docker, Helm
- NVIDIA Triton, TorchServe, Ray, Seldon
- Vector DBs: Qdrant, Milvus, Pinecone
- Monitoring: Prometheus, Grafana, Jaeger, OpenTelemetry
- Cloud providers: AWS, Azure, GCP, OCI

### Architecture Patterns
- Inference gateway with async workers
- Hybrid retrieval and embedding pipeline
- Multi-region deployment for resilience
- Data plane separation for storage, compute, and retrieval

### Example Focus Areas
- Build a low-latency LLM inference cluster
- Deploy a vector search service with autoscaling
- Integrate GPU-based model serving into production API
- Implement observability for ML inference and data stores

## Study Plan

1. Learn GPU and serving fundamentals
2. Build a prototype inference pipeline
3. Deploy vector DB and retrieval service
4. Add Kubernetes orchestration and autoscaling
5. Implement monitoring, alerting, and reliability practices
