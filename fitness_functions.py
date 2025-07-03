"""
Group Buying Platform - Availability Fitness Functions
====================================================

Simple, self-contained fitness functions focused on availability testing.
All services are mocked to demonstrate the concept without external dependencies.
"""

import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional
import json


@dataclass
class ServiceHealth:
    """Represents the health status of a service"""
    name: str
    is_healthy: bool
    response_time: float
    error_message: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class AvailabilityResult:
    """Results of availability fitness function tests"""
    overall_score: int
    is_healthy: bool
    services: Dict[str, ServiceHealth]
    critical_path_available: bool
    issues: List[str]
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class MockService:
    """Mock service that simulates real service behavior"""
    
    def __init__(self, name: str, base_response_time: float = 0.1, failure_rate: float = 0.05):
        self.name = name
        self.base_response_time = base_response_time
        self.failure_rate = failure_rate
        self.is_available = True
    
    def simulate_request(self) -> ServiceHealth:
        """Simulate a service request with realistic behavior"""
        start_time = time.time()
        
        # Simulate network delay
        time.sleep(self.base_response_time + random.uniform(0, 0.2))
        
        response_time = time.time() - start_time
        
        # Simulate occasional failures
        if not self.is_available or random.random() < self.failure_rate:
            return ServiceHealth(
                name=self.name,
                is_healthy=False,
                response_time=response_time,
                error_message=f"Service {self.name} is unavailable"
            )
        
        return ServiceHealth(
            name=self.name,
            is_healthy=True,
            response_time=response_time
        )
    
    def set_availability(self, available: bool):
        """Set service availability for testing"""
        self.is_available = available


class AvailabilityFitnessFunctions:
    """
    Availability-focused fitness functions for the Group Buying Platform.
    
    Tests the critical path availability:
    1. User creates a group cart
    2. Other users join and add products
    3. Minimum threshold reached → cart closes
    4. Consolidated order generated
    5. Group payment initiated and completed
    6. Logistics and distribution managed
    7. Users notified for pickup/delivery
    """
    
    def __init__(self):
        # Initialize mock services for the critical path
        self.services = {
            'group_buying_service': MockService('group_buying_service', 0.15, 0.02),
            'order_service': MockService('order_service', 0.2, 0.03),
            'payment_service': MockService('payment_service', 0.3, 0.05),
            'logistics_service': MockService('logistics_service', 0.25, 0.04),
            'notification_service': MockService('notification_service', 0.1, 0.01),
            'database': MockService('database', 0.05, 0.01),
            'cache': MockService('cache', 0.02, 0.005)
        }
        
        # Availability thresholds
        self.thresholds = {
            'max_response_time': 5.0,  # 5 seconds (more realistic for degraded scenarios)
            'max_failure_rate': 0.10,  # 10% (more lenient)
            'min_availability_score': 70  # 70/100 (more realistic)
        }
    
    def test_service_health(self, service_name: str) -> ServiceHealth:
        """Test individual service health"""
        if service_name not in self.services:
            return ServiceHealth(
                name=service_name,
                is_healthy=False,
                response_time=0,
                error_message=f"Service {service_name} not found"
            )
        
        return self.services[service_name].simulate_request()
    
    def test_critical_path_availability(self) -> bool:
        """
        Test the complete critical path availability.
        This is the most important test for business success.
        """
        print("🔍 Testing critical path availability...")
        
        # Simulate the critical path
        steps = [
            ("Create group cart", "group_buying_service"),
            ("Add products to cart", "group_buying_service"),
            ("Check minimum participants", "database"),
            ("Generate consolidated order", "order_service"),
            ("Process group payment", "payment_service"),
            ("Coordinate logistics", "logistics_service"),
            ("Send notifications", "notification_service")
        ]
        
        path_successful = True
        total_response_time = 0
        
        for step_name, service_name in steps:
            health = self.test_service_health(service_name)
            total_response_time += health.response_time
            
            if not health.is_healthy:
                print(f"❌ {step_name} failed: {health.error_message}")
                path_successful = False
            else:
                print(f"✅ {step_name} successful ({health.response_time:.3f}s)")
        
        print(f"📊 Critical path total time: {total_response_time:.3f}s")
        return path_successful and total_response_time < self.thresholds['max_response_time']
    
    def test_all_services_health(self) -> Dict[str, ServiceHealth]:
        """Test health of all services"""
        print("🏥 Testing all services health...")
        
        results = {}
        for service_name in self.services:
            health = self.test_service_health(service_name)
            results[service_name] = health
            
            status = "✅" if health.is_healthy else "❌"
            print(f"{status} {service_name}: {health.response_time:.3f}s")
        
        return results
    
    def test_concurrent_availability(self, num_requests: int = 10) -> Dict[str, float]:
        """Test availability under concurrent load"""
        print(f"👥 Testing concurrent availability ({num_requests} requests)...")
        
        async def make_concurrent_requests():
            tasks = []
            for i in range(num_requests):
                # Simulate concurrent users hitting different services
                service_name = random.choice(list(self.services.keys()))
                task = asyncio.create_task(self._async_service_request(service_name))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        start_time = time.time()
        results = asyncio.run(make_concurrent_requests())
        total_time = time.time() - start_time
        
        successful_requests = sum(1 for r in results if isinstance(r, ServiceHealth) and r.is_healthy)
        success_rate = successful_requests / num_requests
        
        print(f"📊 Concurrent test results:")
        print(f"   Success rate: {success_rate:.1%}")
        print(f"   Total time: {total_time:.3f}s")
        print(f"   Requests/second: {num_requests/total_time:.1f}")
        
        return {
            'success_rate': success_rate,
            'total_time': total_time,
            'requests_per_second': num_requests / total_time
        }
    
    async def _async_service_request(self, service_name: str) -> ServiceHealth:
        """Async wrapper for service requests"""
        # Simulate async behavior
        await asyncio.sleep(0.01)
        return self.test_service_health(service_name)
    
    def calculate_availability_score(self, service_healths: Dict[str, ServiceHealth]) -> int:
        """Calculate overall availability score (0-100)"""
        if not service_healths:
            return 0
        
        total_services = len(service_healths)
        healthy_services = sum(1 for health in service_healths.values() if health.is_healthy)
        
        # Base score from healthy services
        base_score = (healthy_services / total_services) * 100
        
        # Penalty for slow responses
        slow_services = sum(1 for health in service_healths.values() 
                          if health.response_time > self.thresholds['max_response_time'])
        penalty = (slow_services / total_services) * 20
        
        return max(0, int(base_score - penalty))
    
    def run_availability_tests(self) -> AvailabilityResult:
        """Run all availability fitness function tests"""
        print("🚀 Running Availability Fitness Functions")
        print("=" * 50)
        
        issues = []
        
        # Test 1: Individual service health
        service_healths = self.test_all_services_health()
        
        # Test 2: Critical path availability
        critical_path_available = self.test_critical_path_availability()
        
        # Test 3: Concurrent availability
        concurrent_results = self.test_concurrent_availability()
        
        # Calculate overall score
        availability_score = self.calculate_availability_score(service_healths)
        
        # Check critical path
        if not critical_path_available:
            issues.append("Critical path is not available")
            availability_score -= 30
        
        # Check concurrent performance
        if concurrent_results['success_rate'] < (1 - self.thresholds['max_failure_rate']):
            issues.append(f"Concurrent success rate too low: {concurrent_results['success_rate']:.1%}")
            availability_score -= 20
        
        # Check individual services
        for service_name, health in service_healths.items():
            if not health.is_healthy:
                issues.append(f"Service {service_name} is unhealthy: {health.error_message}")
            elif health.response_time > self.thresholds['max_response_time']:
                issues.append(f"Service {service_name} is too slow: {health.response_time:.3f}s")
        
        is_healthy = availability_score >= self.thresholds['min_availability_score']
        
        print("\n📊 Final Results:")
        print(f"   Overall Score: {availability_score}/100")
        print(f"   Healthy: {'✅' if is_healthy else '❌'}")
        print(f"   Critical Path: {'✅' if critical_path_available else '❌'}")
        
        if issues:
            print(f"   Issues: {len(issues)}")
            for issue in issues:
                print(f"     - {issue}")
        
        return AvailabilityResult(
            overall_score=availability_score,
            is_healthy=is_healthy,
            services=service_healths,
            critical_path_available=critical_path_available,
            issues=issues
        )
    
    def simulate_service_failure(self, service_name: str, available: bool):
        """Simulate service failure for testing"""
        if service_name in self.services:
            self.services[service_name].set_availability(available)
            status = "available" if available else "unavailable"
            print(f"🔧 Set {service_name} to {status}")


# Global instance for easy access
fitness_functions = AvailabilityFitnessFunctions()


def run_fitness_functions() -> AvailabilityResult:
    """Convenience function to run all fitness functions"""
    return fitness_functions.run_availability_tests()


if __name__ == "__main__":
    # Run fitness functions when executed directly
    result = run_fitness_functions()
    
    # Exit with appropriate code
    exit(0 if result.is_healthy else 1) 