# Runbooks

## Purpose

Provide incident response procedures that can be followed under pressure. Each runbook should be actionable by an on-call engineer who may not be familiar with the specific service.

## Runbook Template

```markdown
# Runbook: [Alert Name]

## Metadata
- **Severity**: [Critical/Warning/Info]
- **Service**: [Service name]
- **Last Updated**: [Date]
- **Owner**: [Team/Person]

## Summary
One-sentence description of what this alert means.

## Impact
- **User-facing**: [Yes/No]
- **Data integrity**: [At risk/Safe]
- **Estimated blast radius**: [Number/Percentage of users]

## Detection
How this alert is triggered:
- **Metric**: [metric name]
- **Threshold**: [value]
- **Duration**: [time]

## Diagnosis Steps
1. [First thing to check]
2. [Second thing to check]
3. [Third thing to check]

## Resolution Steps
### Option A: [Most common fix]
[Commands and steps]

### Option B: [Alternative fix]
[Commands and steps]

### Option C: Escalate
[Who to contact]

## Post-Incident
- [ ] Update this runbook if new information discovered
- [ ] Schedule post-mortem if severity >= Warning
- [ ] File ticket for permanent fix
```

---

## High Error Rate

### Metadata
- **Severity**: Warning/Critical
- **Service**: API Gateway, Backend Services
- **Alert**: `HighErrorRate`, `CriticalErrorRate`

### Summary
Service is returning more 5xx errors than acceptable threshold.

### Impact
- **User-facing**: Yes
- **Data integrity**: Usually safe (errors prevent operations)
- **Blast radius**: Depends on endpoint affected

### Detection
- Error rate > 1% for 5 minutes (Warning)
- Error rate > 5% for 2 minutes (Critical)

### Diagnosis Steps

1. **Check which endpoints are affected**
   ```bash
   # Grafana query
   sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint)
   ```

2. **Check error messages in logs**
   ```bash
   # Loki query
   {service="$SERVICE"} |= "error" | json | level="error"
   ```

3. **Check recent deployments**
   ```bash
   kubectl rollout history deployment/$SERVICE
   ```

4. **Check dependent services**
   ```bash
   # Database
   kubectl exec -it postgres-0 -- pg_isready

   # Redis
   kubectl exec -it redis-0 -- redis-cli ping
   ```

5. **Check resource utilization**
   ```bash
   kubectl top pods -l app=$SERVICE
   ```

### Resolution Steps

#### Option A: Rollback recent deployment
```bash
# Check if recent deploy
kubectl rollout history deployment/$SERVICE

# Rollback
kubectl rollout undo deployment/$SERVICE

# Verify
kubectl rollout status deployment/$SERVICE
```

#### Option B: Scale up if resource-constrained
```bash
# Check current replicas
kubectl get deployment $SERVICE

# Scale up
kubectl scale deployment $SERVICE --replicas=5

# Verify
kubectl get pods -l app=$SERVICE -w
```

#### Option C: Restart pods if stuck
```bash
# Rolling restart
kubectl rollout restart deployment/$SERVICE

# Watch progress
kubectl get pods -l app=$SERVICE -w
```

#### Option D: Escalate
- **Database issues**: Contact @dba-oncall
- **Infrastructure issues**: Contact @platform-oncall
- **Unknown**: Contact @engineering-lead

### Post-Incident
- [ ] Identify root cause
- [ ] Update runbook with new learnings
- [ ] File ticket for permanent fix
- [ ] Schedule post-mortem

---

## High Latency

### Metadata
- **Severity**: Warning/Critical
- **Service**: All services
- **Alert**: `HighLatencyP95`, `CriticalLatencyP99`

### Summary
Request latency has exceeded acceptable thresholds.

### Impact
- **User-facing**: Yes (slow responses)
- **Data integrity**: Safe
- **Blast radius**: All users of affected endpoints

### Detection
- p95 > 1s for 5 minutes (Warning)
- p99 > 5s for 2 minutes (Critical)

### Diagnosis Steps

1. **Identify slow endpoints**
   ```promql
   histogram_quantile(0.95,
     sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
   )
   ```

2. **Check database query times**
   ```promql
   histogram_quantile(0.95,
     sum(rate(db_query_duration_seconds_bucket[5m])) by (le, query)
   )
   ```

3. **Check external API latency**
   ```promql
   histogram_quantile(0.95,
     sum(rate(external_api_duration_seconds_bucket[5m])) by (le, api)
   )
   ```

4. **Check for connection pool exhaustion**
   ```promql
   pg_stat_activity_count / pg_settings_max_connections
   ```

5. **Check garbage collection**
   ```promql
   rate(go_gc_duration_seconds_sum[5m])
   ```

### Resolution Steps

#### Option A: Database slow queries
```bash
# Check running queries
kubectl exec -it postgres-0 -- psql -c "
  SELECT pid, now() - pg_stat_activity.query_start AS duration, query
  FROM pg_stat_activity
  WHERE state = 'active' AND query_start < now() - interval '30 seconds'
  ORDER BY duration DESC;
"

# Kill long-running query if needed
kubectl exec -it postgres-0 -- psql -c "SELECT pg_terminate_backend(PID);"
```

#### Option B: Scale up replicas
```bash
kubectl scale deployment $SERVICE --replicas=5
```

#### Option C: Increase connection pool
```bash
# Update configmap
kubectl edit configmap $SERVICE-config
# Increase DB_POOL_SIZE

# Restart to apply
kubectl rollout restart deployment/$SERVICE
```

---

## Database Connection Pool Exhausted

### Metadata
- **Severity**: Critical
- **Service**: Database-dependent services
- **Alert**: `DatabaseConnectionPoolExhausted`

### Summary
Database connection pool is near or at capacity, new connections will fail.

### Impact
- **User-facing**: Yes (requests will fail)
- **Data integrity**: Safe
- **Blast radius**: All database operations

### Diagnosis Steps

1. **Check connection count**
   ```bash
   kubectl exec -it postgres-0 -- psql -c "
     SELECT count(*) FROM pg_stat_activity;
   "
   ```

2. **Check who's holding connections**
   ```bash
   kubectl exec -it postgres-0 -- psql -c "
     SELECT application_name, state, count(*)
     FROM pg_stat_activity
     GROUP BY application_name, state
     ORDER BY count DESC;
   "
   ```

3. **Check for connection leaks**
   ```bash
   kubectl exec -it postgres-0 -- psql -c "
     SELECT pid, usename, application_name, state,
            query_start, state_change, query
     FROM pg_stat_activity
     WHERE state = 'idle'
     AND query_start < now() - interval '10 minutes';
   "
   ```

### Resolution Steps

#### Option A: Kill idle connections
```bash
kubectl exec -it postgres-0 -- psql -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE state = 'idle'
  AND query_start < now() - interval '10 minutes';
"
```

#### Option B: Restart service with connection leak
```bash
# Identify service with most connections
# Then restart it
kubectl rollout restart deployment/$LEAKY_SERVICE
```

#### Option C: Increase max connections (temporary)
```bash
# This requires PostgreSQL restart - use with caution
kubectl exec -it postgres-0 -- psql -c "ALTER SYSTEM SET max_connections = 200;"
kubectl delete pod postgres-0  # Will restart and apply
```

---

## Memory Pressure

### Metadata
- **Severity**: Warning/Critical
- **Service**: All services
- **Alert**: `HighMemoryUsage`, `CriticalMemoryUsage`

### Summary
Container/node memory usage is high, OOM kills may occur.

### Impact
- **User-facing**: Potentially (if OOM kills occur)
- **Data integrity**: Potentially at risk (in-flight requests lost)
- **Blast radius**: Service instances on affected nodes

### Diagnosis Steps

1. **Check which pods are using memory**
   ```bash
   kubectl top pods --sort-by=memory
   ```

2. **Check for memory leaks (trend)**
   ```promql
   container_memory_usage_bytes{pod="$POD"}
   ```

3. **Check for recent traffic spike**
   ```promql
   sum(rate(http_requests_total[5m])) by (service)
   ```

4. **Check heap usage (if Java/Go)**
   ```promql
   go_memstats_heap_alloc_bytes
   jvm_memory_used_bytes
   ```

### Resolution Steps

#### Option A: Restart leaking pod
```bash
kubectl delete pod $POD_NAME
# Will be recreated by deployment
```

#### Option B: Scale horizontally
```bash
kubectl scale deployment $SERVICE --replicas=5
```

#### Option C: Increase memory limits
```bash
kubectl patch deployment $SERVICE -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "$CONTAINER",
          "resources": {
            "limits": {"memory": "2Gi"},
            "requests": {"memory": "1Gi"}
          }
        }]
      }
    }
  }
}'
```

---

## No Traffic

### Metadata
- **Severity**: Critical
- **Service**: All customer-facing services
- **Alert**: `NoTraffic`

### Summary
Service is receiving zero requests, indicating complete outage.

### Impact
- **User-facing**: Yes (complete outage)
- **Data integrity**: Unknown
- **Blast radius**: 100% of users

### Diagnosis Steps

1. **Check if service is running**
   ```bash
   kubectl get pods -l app=$SERVICE
   kubectl describe pod $POD
   ```

2. **Check ingress/load balancer**
   ```bash
   kubectl get ingress
   kubectl describe ingress $INGRESS
   ```

3. **Check DNS**
   ```bash
   nslookup $DOMAIN
   dig $DOMAIN
   ```

4. **Check certificate**
   ```bash
   echo | openssl s_client -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates
   ```

5. **Check upstream (if behind CDN)**
   ```bash
   curl -I https://$DOMAIN --resolve "$DOMAIN:443:$ORIGIN_IP"
   ```

### Resolution Steps

#### Option A: Service crashed - restart
```bash
kubectl rollout restart deployment/$SERVICE
```

#### Option B: Ingress misconfigured
```bash
kubectl get ingress -o yaml > ingress-backup.yaml
# Review and fix configuration
kubectl apply -f ingress-fix.yaml
```

#### Option C: DNS issue
```bash
# Check and update DNS records in your provider
# Verify propagation
dig $DOMAIN @8.8.8.8
```

#### Option D: Certificate expired
```bash
# Trigger certificate renewal (cert-manager)
kubectl delete certificate $CERT_NAME
# Or manually renew and update secret
```

---

## Runbook Index

| Alert | Runbook | Severity |
|-------|---------|----------|
| HighErrorRate | [High Error Rate](#high-error-rate) | Warning |
| CriticalErrorRate | [High Error Rate](#high-error-rate) | Critical |
| HighLatencyP95 | [High Latency](#high-latency) | Warning |
| CriticalLatencyP99 | [High Latency](#high-latency) | Critical |
| DatabaseConnectionPoolExhausted | [DB Connections](#database-connection-pool-exhausted) | Critical |
| HighMemoryUsage | [Memory Pressure](#memory-pressure) | Warning |
| CriticalMemoryUsage | [Memory Pressure](#memory-pressure) | Critical |
| NoTraffic | [No Traffic](#no-traffic) | Critical |
