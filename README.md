# Group Buying Platform - Availability Fitness Functions

A simple, self-contained Python implementation of availability fitness functions for a group buying platform. This focuses specifically on **availability** as the critical business requirement.

## 🎯 What This Is

This is a **mock implementation** that demonstrates how to test the availability of a group buying platform's critical path. It's designed to be:

- **Simple**: Easy to understand and modify
- **Fast**: Runs in seconds, not minutes
- **Self-contained**: No external dependencies beyond Python packages
- **Focused**: Only tests availability (no performance, scalability, etc.)

## 🏗️ Critical Path

The group buying platform's critical path for availability:

1. **Create group cart** → Group buying service
2. **Add products** → Group buying service  
3. **Check minimum participants** → Database
4. **Generate consolidated order** → Order service
5. **Process group payment** → Payment service
6. **Coordinate logistics** → Logistics service
7. **Send notifications** → Notification service

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Fitness Functions
```bash
python fitness_functions.py
```

### Run Tests
```bash
pytest test_fitness_functions.py -v
```

## 📊 What It Tests

### 1. Individual Service Health
Tests each service in isolation:
- Response time
- Availability status
- Error handling

### 2. Critical Path Availability
Tests the complete end-to-end flow:
- All steps must succeed
- Total time under threshold (2 seconds)
- Any failure breaks the entire path

### 3. Concurrent Availability
Tests system under load:
- Multiple simultaneous requests
- Success rate measurement
- Throughput calculation

## 🎮 Interactive Testing

You can simulate different scenarios:

```python
from fitness_functions import fitness_functions

# Simulate a service failure
fitness_functions.simulate_service_failure('payment_service', False)

# Run tests to see the impact
result = fitness_functions.run_availability_tests()
print(f"System healthy: {result.is_healthy}")
print(f"Score: {result.overall_score}/100")
```

## 📈 Scoring System

The system calculates an availability score (0-100):

- **Base score**: Percentage of healthy services
- **Penalties**: 
  - Slow services (>2s response time)
  - Critical path failures (-30 points)
  - Low concurrent success rate (-20 points)
- **Threshold**: 80/100 minimum for "healthy"

## 🔧 Configuration

Modify thresholds in `fitness_functions.py`:

```python
self.thresholds = {
    'max_response_time': 2.0,  # 2 seconds
    'max_failure_rate': 0.05,  # 5%
    'min_availability_score': 80  # 80/100
}
```

## 🧪 Test Scenarios

The test suite includes:

- **Healthy system**: All services working normally
- **Degraded system**: Some services slow or failing
- **Critical failure**: Essential service completely down
- **Concurrent load**: Multiple users hitting the system

## 📁 Files

- `fitness_functions.py` - Main fitness functions implementation
- `test_fitness_functions.py` - Pytest test suite
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🎯 Business Value

This fitness function system helps ensure:

- **Revenue protection**: Critical path failures directly impact sales
- **User experience**: Fast, reliable service keeps users engaged
- **Operational awareness**: Early detection of availability issues
- **Confidence**: Clear metrics for system health

## 🔄 Continuous Monitoring

You can integrate this into CI/CD:

```yaml
# Example GitHub Actions step
- name: Run Availability Tests
  run: |
    python fitness_functions.py
    if [ $? -ne 0 ]; then
      echo "❌ Availability tests failed"
      exit 1
    fi
```

## 🤝 Contributing

1. Keep it simple and focused on availability
2. Add tests for new scenarios
3. Update thresholds based on business requirements
4. Document any changes to the critical path

---

**Remember**: This is a mock implementation for demonstration. In a real system, you'd replace the mock services with actual service health checks.
