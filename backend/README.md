# Backend

### execute tests
```bash
docker compose exec backend pytest . -vv -p no:warnings
```

### coverage
```bash
docker-compose exec backend pytest --cov=api --cov-report=html --cov-report=term-missing -p no:warnings -vv
```