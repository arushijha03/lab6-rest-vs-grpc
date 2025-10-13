# Lab 6 — Comparing REST and gRPC

## REST Results

| Method           | Localhost (ms/op) | Same-Zone (ms/op) | Cross-Region (ms/op) |
|------------------|------------------:|------------------:|---------------------:|
| REST add         | 4.15              | 4.37              | 323.60               |
| REST rawimage    | 9.26              | 23.67             | 1287.17              |
| REST jsonimage   | 45.81             | 84.57             | 1466.56              |
| REST dotproduct  | 4.82              | 6.13              | 324.14               |
| PING (baseline)  |         —         | 0.49              | 155.92               |

### Observations
- **Latency dominates tiny calls.** `add` ~4 ms (localhost/same-zone) → ~324 ms cross-region, roughly tracking RTT (ping ~156 ms).
- **Payload format matters.** `rawimage` (binary) beats `jsonimage` (base64 bloat ~33% + JSON parse).
- **Compute vs transport.** `dotproduct(n=100)` behaves like `add`; network/HTTP overhead dwarfs compute.
- Expect **gRPC** to reduce per-call overhead vs REST for small messages and to narrow the gap for image transfer compared to `jsonimage`.

