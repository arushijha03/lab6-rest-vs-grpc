# Lab 6 — Comparing REST and gRPC

## REST Results

| Method           | Localhost (ms/op) | Same-Zone (ms/op) | Cross-Region (ms/op) |
|------------------|------------------:|------------------:|---------------------:|
| REST add         | 4.15              | 4.37              | 323.60               |
| REST rawimage    | 9.26              | 23.67             | 1287.17              |
| REST jsonimage   | 45.81             | 84.57             | 1466.56              |
| REST dotproduct  | 4.82              | 6.13              | 324.14               |
| PING (baseline)  |        —          | 0.49              | 155.92               |

## gRPC Results

| Method            | Localhost (ms/op) | Same-Zone (ms/op) | Cross-Region (ms/op) |
|-------------------|------------------:|------------------:|---------------------:|
| gRPC add          | 0.82              | 1.02              | 150.13               |
| gRPC rawimage     | 14.88             | 13.87             | 225.64               |
| gRPC jsonimage    | 28.35             | 34.21             | 227.63               |
| gRPC dotproduct   | 0.95              | 1.23              | 165.72               |

### Observations
- **Overhead vs RTT:** For tiny calls (`add`, `dotProduct`), gRPC cuts per-call overhead a lot (≈0.8–1.2 ms) vs REST (≈4–6 ms) when network is short (localhost / same-zone). Across regions, both stacks rise toward the RTT floor (ping ≈156 ms), but gRPC still stays closer to RTT than REST.
- **Payload format matters:** Binary `rawimage` consistently beats `jsonimage`. Base64 adds ~33% size plus JSON parse cost; that’s why `jsonimage` is slowest in each column.
- **Compute is tiny here:** `dotproduct(n=100)` doesn’t dominate runtime; transport/serialization overheads do, so it tracks `add`.
- **Takeaway:** Use gRPC for low-latency, high-throughput micro-RPCs and binary payloads; REST is fine for broader interoperability but adds overhead, especially for large JSON bodies.

