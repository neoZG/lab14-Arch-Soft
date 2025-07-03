# GitHub Actions for Fitness Functions

Automated testing and monitoring for your fitness functions.

## What it does

- **Tests on every code change** - Ensures your system stays healthy
- **Monitors continuously** - Checks system health every 30 minutes  
- **Validates deployments** - Tests before and after deployment
- **Runs different scenarios** - Tests various failure conditions

## Workflows

### 1. `fitness-functions.yml` - Main Testing
**When**: Push, Pull Request, Every 6 hours
**What**: Runs all tests, performance checks, security scans

### 2. `scenario-testing.yml` - Manual Testing  
**When**: Manual trigger
**What**: Test specific scenarios (healthy, degraded, failure modes)

### 3. `monitoring.yml` - Health Monitoring
**When**: Every 30 minutes
**What**: Continuous health checks with alerts

### 4. `deployment.yml` - Deployment Safety
**When**: Push to main, tags
**What**: Pre/post deployment validation

## Quick Setup

1. **Push the workflow files** to your repository
2. **Enable Actions** in repository settings
3. **Test locally first**:
   ```bash
   python test_github_actions.py
   ```

## Usage

### Manual Testing
1. Go to Actions tab
2. Select "Scenario Testing" 
3. Click "Run workflow"
4. Choose scenario and run

### View Results
- Check Actions tab for detailed logs
- Download artifacts for analysis
- Look at step summaries for quick overview

## Configuration

### Alert Thresholds
Set in workflow inputs or environment variables:
```yaml
ALERT_THRESHOLD: 70  # Alert if score < 70
```

### Test Scenarios
Available scenarios:
- `healthy_system` - All services working
- `degraded_system` - Some services slow
- `critical_failure` - Essential service down
- `high_load` - Performance under stress

## What You Get

- ✅ **Automated health monitoring**
- ✅ **Deployment safety checks**  
- ✅ **Performance testing**
- ✅ **Security scanning**
- ✅ **Detailed reports**
- ✅ **Historical metrics**
