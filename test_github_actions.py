#!/usr/bin/env python3
"""
Local GitHub Actions Testing Script
==================================

This script simulates the GitHub Actions workflows locally to help you test
your fitness functions before pushing to GitHub.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Add current directory to path to import fitness_functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fitness_functions import fitness_functions


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)


def print_result(result):
    """Print formatted test results"""
    print(f"\n📊 Results:")
    print(f"   Overall Score: {result.overall_score}/100")
    print(f"   System Healthy: {'✅' if result.is_healthy else '❌'}")
    print(f"   Critical Path: {'✅' if result.critical_path_available else '❌'}")
    
    if result.issues:
        print(f"   Issues Found: {len(result.issues)}")
        for issue in result.issues:
            print(f"     ❌ {issue}")
    else:
        print("   ✅ No issues detected")


def run_availability_testing():
    """Simulate the main fitness-functions.yml workflow"""
    print_header("SIMULATING: Main Fitness Functions Workflow")
    
    # Create test results directory
    os.makedirs("test-results", exist_ok=True)
    
    print("🚀 Starting fitness functions testing...")
    
    # Set deterministic behavior for consistent testing
    for service_name in fitness_functions.services:
        fitness_functions.services[service_name].failure_rate = 0.001
    
    # Run availability tests
    result = fitness_functions.run_availability_tests()
    
    # Generate test report
    report = {
        'timestamp': time.time(),
        'overall_score': result.overall_score,
        'is_healthy': result.is_healthy,
        'critical_path_available': result.critical_path_available,
        'issues': result.issues,
        'services': {
            name: {
                'is_healthy': health.is_healthy,
                'response_time': health.response_time,
                'error_message': health.error_message
            }
            for name, health in result.services.items()
        }
    }
    
    # Save report
    with open('test-results/availability-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print_result(result)
    
    # Check if system is healthy
    if result.is_healthy:
        print("✅ System is healthy - would pass GitHub Actions")
        return True
    else:
        print("❌ System is unhealthy - would fail GitHub Actions")
        return False


def run_scenario_testing(scenario, iterations=3):
    """Simulate the scenario-testing.yml workflow"""
    print_header(f"SIMULATING: Scenario Testing - {scenario}")
    
    # Create scenario results directory
    os.makedirs("scenario-results", exist_ok=True)
    
    print(f"🎯 Running scenario: {scenario}")
    print(f"🔄 Iterations: {iterations}")
    
    results = []
    
    for i in range(iterations):
        print(f"\n--- Iteration {i+1}/{iterations} ---")
        
        # Reset all services to healthy state and set deterministic behavior
        for service_name in fitness_functions.services:
            fitness_functions.simulate_service_failure(service_name, True)
            # Set very low failure rates for consistent testing
            fitness_functions.services[service_name].failure_rate = 0.001
        
        # Apply scenario-specific conditions
        if scenario == 'healthy_system':
            pass  # All services healthy (default state)
            
        elif scenario == 'degraded_system':
            fitness_functions.services['payment_service'].base_response_time = 2.5
            fitness_functions.services['logistics_service'].base_response_time = 2.0
            
        elif scenario == 'critical_failure':
            fitness_functions.simulate_service_failure('group_buying_service', False)
            
        elif scenario == 'partial_failure':
            fitness_functions.simulate_service_failure('notification_service', False)
            
        elif scenario == 'high_load':
            result = fitness_functions.run_availability_tests()
            concurrent_results = fitness_functions.test_concurrent_availability(50)
            
            iteration_result = {
                'iteration': i+1,
                'timestamp': time.time(),
                'overall_score': result.overall_score,
                'is_healthy': result.is_healthy,
                'critical_path_available': result.critical_path_available,
                'issues': result.issues,
                'concurrent_success_rate': concurrent_results['success_rate'],
                'concurrent_requests_per_second': concurrent_results['requests_per_second']
            }
            results.append(iteration_result)
            continue
            
        elif scenario == 'stress_test':
            fitness_functions.services['payment_service'].base_response_time = 3.0
            fitness_functions.services['logistics_service'].base_response_time = 2.5
            fitness_functions.services['order_service'].base_response_time = 2.0
            fitness_functions.simulate_service_failure('cache', False)
        
        # Run availability tests
        result = fitness_functions.run_availability_tests()
        
        iteration_result = {
            'iteration': i+1,
            'timestamp': time.time(),
            'overall_score': result.overall_score,
            'is_healthy': result.is_healthy,
            'critical_path_available': result.critical_path_available,
            'issues': result.issues
        }
        results.append(iteration_result)
    
    # Calculate summary statistics
    scores = [r['overall_score'] for r in results]
    healthy_count = sum(1 for r in results if r['is_healthy'])
    critical_path_count = sum(1 for r in results if r['critical_path_available'])
    
    summary = {
        'scenario': scenario,
        'iterations': iterations,
        'timestamp': time.time(),
        'summary': {
            'average_score': sum(scores) / len(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'healthy_rate': healthy_count / len(results),
            'critical_path_rate': critical_path_count / len(results),
            'total_issues': sum(len(r['issues']) for r in results)
        },
        'results': results
    }
    
    # Save results
    with open(f'scenario-results/{scenario}_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    avg_score = summary['summary']['average_score']
    healthy_rate = summary['summary']['healthy_rate']
    
    print(f"\n📊 Scenario Summary:")
    print(f"   Average Score: {avg_score:.1f}/100")
    print(f"   Healthy Rate: {healthy_rate:.1%}")
    print(f"   Critical Path Rate: {summary['summary']['critical_path_rate']:.1%}")
    
    return healthy_rate >= 0.6  # More lenient for local testing


def run_monitoring(alert_threshold=70):
    """Simulate the monitoring.yml workflow"""
    print_header("SIMULATING: Continuous Monitoring")
    
    # Create monitoring directory
    os.makedirs("monitoring-results", exist_ok=True)
    
    print("🏥 Running health check...")
    
    # Run fitness functions
    result = fitness_functions.run_availability_tests()
    
    # Create health report
    health_report = {
        'timestamp': time.time(),
        'datetime': datetime.now().isoformat(),
        'overall_score': result.overall_score,
        'is_healthy': result.is_healthy,
        'critical_path_available': result.critical_path_available,
        'issues': result.issues,
        'services': {
            name: {
                'is_healthy': health.is_healthy,
                'response_time': health.response_time,
                'error_message': health.error_message
            }
            for name, health in result.services.items()
        }
    }
    
    # Save report
    with open('monitoring-results/health_report.json', 'w') as f:
        json.dump(health_report, f, indent=2)
    
    print(f"📊 Health Check Results:")
    print(f"   Overall Score: {result.overall_score}/100")
    print(f"   System Healthy: {'✅' if result.is_healthy else '❌'}")
    print(f"   Critical Path: {'✅' if result.critical_path_available else '❌'}")
    print(f"   Issues Found: {len(result.issues)}")
    
    # Check against alert threshold
    if result.overall_score < alert_threshold:
        print(f"🚨 ALERT: System score ({result.overall_score}) below threshold ({alert_threshold})")
        return False
    else:
        print(f"✅ System health is within acceptable range")
        return True


def run_deployment_validation(environment="production"):
    """Simulate the deployment.yml workflow"""
    print_header(f"SIMULATING: Deployment Validation - {environment}")
    
    # Create validation directory
    os.makedirs("deployment-validation", exist_ok=True)
    
    print("🔍 Running pre-deployment validation...")
    
    # Run comprehensive fitness tests
    scenarios = ['healthy_system', 'degraded_system', 'high_load']
    results = {}
    
    for scenario in scenarios:
        print(f"\n--- Testing {scenario} ---")
        
        # Reset services and set deterministic behavior
        for service_name in fitness_functions.services:
            fitness_functions.simulate_service_failure(service_name, True)
            fitness_functions.services[service_name].failure_rate = 0.001
        
        # Apply scenario conditions
        if scenario == 'degraded_system':
            fitness_functions.services['payment_service'].base_response_time = 2.0
            fitness_functions.services['logistics_service'].base_response_time = 1.5
        elif scenario == 'high_load':
            result = fitness_functions.run_availability_tests()
            concurrent_results = fitness_functions.test_concurrent_availability(100)
            
            results[scenario] = {
                'overall_score': result.overall_score,
                'is_healthy': result.is_healthy,
                'critical_path_available': result.critical_path_available,
                'concurrent_success_rate': concurrent_results['success_rate'],
                'concurrent_requests_per_second': concurrent_results['requests_per_second']
            }
            continue
        
        # Run availability tests
        result = fitness_functions.run_availability_tests()
        results[scenario] = {
            'overall_score': result.overall_score,
            'is_healthy': result.is_healthy,
            'critical_path_available': result.critical_path_available,
            'issues': result.issues
        }
    
    # Calculate validation score
    scores = [r['overall_score'] for r in results.values()]
    avg_score = sum(scores) / len(scores)
    all_healthy = all(r['is_healthy'] for r in results.values())
    critical_path_ok = all(r['critical_path_available'] for r in results.values())
    
    validation_result = {
        'timestamp': time.time(),
        'scenarios_tested': list(results.keys()),
        'average_score': avg_score,
        'all_scenarios_healthy': all_healthy,
        'critical_path_available': critical_path_ok,
        'validation_passed': avg_score >= 80 and all_healthy and critical_path_ok,
        'detailed_results': results
    }
    
    # Save validation results
    with open('deployment-validation/pre_deployment_validation.json', 'w') as f:
        json.dump(validation_result, f, indent=2)
    
    print(f"\n📊 Pre-deployment validation results:")
    print(f"   Average Score: {avg_score:.1f}/100")
    print(f"   All Scenarios Healthy: {all_healthy}")
    print(f"   Critical Path Available: {critical_path_ok}")
    print(f"   Validation Passed: {validation_result['validation_passed']}")
    
    if validation_result['validation_passed']:
        print("✅ Pre-deployment validation passed")
        
        # Simulate deployment
        print("\n🚀 Deploying to environment...")
        time.sleep(2)
        print("✅ Deployment completed successfully")
        
        # Post-deployment validation
        print("\n🔍 Running post-deployment validation...")
        time.sleep(1)
        
        test_results = []
        for i in range(3):  # Reduced for local testing
            print(f"\n--- Post-deployment test {i+1}/3 ---")
            result = fitness_functions.run_availability_tests()
            test_results.append({
                'test_number': i+1,
                'overall_score': result.overall_score,
                'is_healthy': result.is_healthy,
                'critical_path_available': result.critical_path_available,
                'issues': result.issues
            })
        
        # Calculate post-deployment metrics
        scores = [r['overall_score'] for r in test_results]
        avg_score = sum(scores) / len(scores)
        all_healthy = all(r['is_healthy'] for r in test_results)
        critical_path_ok = all(r['critical_path_available'] for r in test_results)
        
        post_deployment_result = {
            'timestamp': time.time(),
            'deployment_environment': environment,
            'tests_run': len(test_results),
            'average_score': avg_score,
            'all_tests_healthy': all_healthy,
            'critical_path_available': critical_path_ok,
            'validation_passed': avg_score >= 85 and all_healthy and critical_path_ok,
            'test_results': test_results
        }
        
        # Save post-deployment results
        with open('deployment-validation/post_deployment_validation.json', 'w') as f:
            json.dump(post_deployment_result, f, indent=2)
        
        print(f"\n📊 Post-deployment validation results:")
        print(f"   Average Score: {avg_score:.1f}/100")
        print(f"   All Tests Healthy: {all_healthy}")
        print(f"   Critical Path Available: {critical_path_ok}")
        print(f"   Validation Passed: {post_deployment_result['validation_passed']}")
        
        if post_deployment_result['validation_passed']:
            print("✅ Post-deployment validation passed")
            return True
        else:
            print("❌ Post-deployment validation failed")
            return False
    else:
        print("❌ Pre-deployment validation failed")
        return False


def main():
    """Main function to run local GitHub Actions simulation"""
    parser = argparse.ArgumentParser(description='Test GitHub Actions workflows locally')
    parser.add_argument('--workflow', choices=['fitness-functions', 'scenario', 'monitoring', 'deployment', 'all'],
                       default='all', help='Workflow to simulate')
    parser.add_argument('--scenario', choices=['healthy_system', 'degraded_system', 'critical_failure', 
                                             'partial_failure', 'high_load', 'stress_test'],
                       default='healthy_system', help='Scenario to test (for scenario workflow)')
    parser.add_argument('--iterations', type=int, default=3, help='Number of iterations (for scenario workflow)')
    parser.add_argument('--alert-threshold', type=int, default=70, help='Alert threshold (for monitoring workflow)')
    parser.add_argument('--environment', choices=['staging', 'production'], default='production',
                       help='Deployment environment (for deployment workflow)')
    
    args = parser.parse_args()
    
    print("🚀 GitHub Actions Local Testing")
    print("=" * 60)
    print("This script simulates GitHub Actions workflows locally.")
    print("Use this to test your fitness functions before pushing to GitHub.")
    print("=" * 60)
    
    results = {}
    
    if args.workflow in ['fitness-functions', 'all']:
        results['fitness-functions'] = run_availability_testing()
    
    if args.workflow in ['scenario', 'all']:
        results['scenario'] = run_scenario_testing(args.scenario, args.iterations)
    
    if args.workflow in ['monitoring', 'all']:
        results['monitoring'] = run_monitoring(args.alert_threshold)
    
    if args.workflow in ['deployment', 'all']:
        results['deployment'] = run_deployment_validation(args.environment)
    
    # Summary
    print_header("TESTING SUMMARY")
    for workflow, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {workflow}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All workflows would pass on GitHub Actions!")
        return 0
    else:
        print("\n⚠️ Some workflows would fail on GitHub Actions.")
        print("Please fix the issues before pushing to GitHub.")
        return 1


if __name__ == "__main__":
    exit(main()) 