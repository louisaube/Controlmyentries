# API Documentation

## Endpoints

### Health Check

```
GET /api/health
```

Returns: `{"status": "ok"}`

### Analysis (Coming Soon)

```
POST /api/analyze
```

Upload GL + baseline files for anomaly detection.

### Generate Baseline (Coming Soon)

```
POST /api/generate-baseline
```

Upload GL N-1 to generate baseline.json.

### WebSocket Progress (Coming Soon)

```
WS /ws/progress/{job_id}
```

Real-time progress updates during analysis.

## Interactive Documentation

When running locally, visit:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc
