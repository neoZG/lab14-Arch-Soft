"""
Pytest tests for Availability Fitness Functions
==============================================

Simple tests to demonstrate how to test the fitness functions.
"""

import pytest
import time
from fitness_functions import (
    AvailabilityFitnessFunctions, 
    ServiceHealth, 
    AvailabilityResult,
    MockService
)


class TestMockService:
    """Test the MockService class"""
    
    def test_mock_service_creation(self):
        """Test creating a mock service"""
        service = MockService("test_service", 0.1, 0.05)
        assert service.name == "test_service"
        assert service.base_response_time == 0.1
        assert service.failure_rate == 0.05
        assert service.is_available is True
    
    def test_mock_service_simulation(self):
        """Test service simulation"""
        service = MockService("test_service", 0.1, 0.0)  # No failures
        health = service.simulate_request()
        
        assert isinstance(health, ServiceHealth)
        assert health.name == "test_service"
        assert health.is_healthy is True
        assert health.response_time > 0
        assert health.error_message is None
    
    def test_mock_service_failure_simulation(self):
        """Test service failure simulation"""
        service = MockService("test_service", 0.1, 1.0)  # Always fail
        health = service.simulate_request()
        
        assert health.is_healthy is False
        assert health.error_message is not None
    
    def test_mock_service_availability_control(self):
        """Test controlling service availability"""
        service = MockService("test_service")
        service.set_availability(False)
        
        health = service.simulate_request()
        assert health.is_healthy is False


class TestAvailabilityFitnessFunctions:
    """Test the main fitness functions class"""
    
    @pytest.fixture
    def fitness_functions(self):
        """Create a fresh fitness functions instance for each test"""
        return AvailabilityFitnessFunctions()
    
    def test_fitness_functions_initialization(self, fitness_functions):
        """Test fitness functions initialization"""
        assert len(fitness_functions.services) == 7  # 7 mock services
        assert 'group_buying_service' in fitness_functions.services
        assert 'payment_service' in fitness_functions.services
        assert fitness_functions.thresholds['max_response_time'] == 3.0
    
    def test_service_health_test(self, fitness_functions):
        """Test individual service health testing"""
        health = fitness_functions.test_service_health('group_buying_service')
        
        assert isinstance(health, ServiceHealth)
        assert health.name == 'group_buying_service'
        assert health.response_time > 0
    
    def test_nonexistent_service_health(self, fitness_functions):
        """Test health check for non-existent service"""
        health = fitness_functions.test_service_health('nonexistent_service')
        
        assert health.is_healthy is False
        assert health.error_message == "Service nonexistent_service not found"
    
    def test_all_services_health(self, fitness_functions):
        """Test all services health check"""
        results = fitness_functions.test_all_services_health()
        
        assert len(results) == 7
        for service_name, health in results.items():
            assert isinstance(health, ServiceHealth)
            assert health.name == service_name
    
    def test_critical_path_availability(self, fitness_functions):
        """Test critical path availability"""
        result = fitness_functions.test_critical_path_availability()
        
        assert isinstance(result, bool)
        # Should be True with default mock settings
    
    def test_critical_path_with_failure(self, fitness_functions):
        """Test critical path when a service fails"""
        # Make payment service unavailable
        fitness_functions.services['payment_service'].set_availability(False)
        
        result = fitness_functions.test_critical_path_availability()
        assert result is False
    
    def test_concurrent_availability(self, fitness_functions):
        """Test concurrent availability"""
        results = fitness_functions.test_concurrent_availability(num_requests=5)
        
        assert 'success_rate' in results
        assert 'total_time' in results
        assert 'requests_per_second' in results
        assert 0 <= results['success_rate'] <= 1
        assert results['total_time'] > 0
    
    def test_availability_score_calculation(self, fitness_functions):
        """Test availability score calculation"""
        # Create mock service health results
        service_healths = {
            'service1': ServiceHealth('service1', True, 0.1),
            'service2': ServiceHealth('service2', True, 0.2),
            'service3': ServiceHealth('service3', False, 0.1, "Error")
        }
        
        score = fitness_functions.calculate_availability_score(service_healths)
        
        assert 0 <= score <= 100
        # With 2/3 healthy services, should be around 67 (minus penalties)
        assert score < 100
    
    def test_full_availability_test_run(self, fitness_functions):
        """Test the complete availability test run"""
        result = fitness_functions.run_availability_tests()
        
        assert isinstance(result, AvailabilityResult)
        assert hasattr(result, 'overall_score')
        assert hasattr(result, 'is_healthy')
        assert hasattr(result, 'services')
        assert hasattr(result, 'critical_path_available')
        assert hasattr(result, 'issues')
        assert 0 <= result.overall_score <= 100
    
    def test_service_failure_simulation(self, fitness_functions):
        """Test simulating service failures"""
        fitness_functions.simulate_service_failure('payment_service', False)
        
        # Test that the service is now unavailable
        health = fitness_functions.test_service_health('payment_service')
        assert health.is_healthy is False


class TestServiceHealth:
    """Test the ServiceHealth dataclass"""
    
    def test_service_health_creation(self):
        """Test creating a ServiceHealth instance"""
        health = ServiceHealth(
            name="test_service",
            is_healthy=True,
            response_time=0.5
        )
        
        assert health.name == "test_service"
        assert health.is_healthy is True
        assert health.response_time == 0.5
        assert health.error_message is None
        assert health.timestamp is not None
    
    def test_service_health_with_error(self):
        """Test ServiceHealth with error message"""
        health = ServiceHealth(
            name="test_service",
            is_healthy=False,
            response_time=0.1,
            error_message="Connection timeout"
        )
        
        assert health.is_healthy is False
        assert health.error_message == "Connection timeout"


class TestAvailabilityResult:
    """Test the AvailabilityResult dataclass"""
    
    def test_availability_result_creation(self):
        """Test creating an AvailabilityResult instance"""
        services = {
            'service1': ServiceHealth('service1', True, 0.1)
        }
        
        result = AvailabilityResult(
            overall_score=85,
            is_healthy=True,
            services=services,
            critical_path_available=True,
            issues=[]
        )
        
        assert result.overall_score == 85
        assert result.is_healthy is True
        assert result.critical_path_available is True
        assert len(result.issues) == 0
        assert result.timestamp is not None


# Integration tests
class TestFitnessFunctionsIntegration:
    """Integration tests for fitness functions"""
    
    def test_healthy_system_scenario(self):
        """Test a completely healthy system"""
        fitness_functions = AvailabilityFitnessFunctions()
        result = fitness_functions.run_availability_tests()
        
        # With default settings, should be healthy
        assert result.is_healthy is True
        assert result.critical_path_available is True
        assert result.overall_score >= 80
    
    def test_degraded_system_scenario(self):
        """Test a system with some degraded services"""
        fitness_functions = AvailabilityFitnessFunctions()
        
        # Make some services slow
        fitness_functions.services['payment_service'].base_response_time = 3.0
        fitness_functions.services['logistics_service'].base_response_time = 2.5
        
        result = fitness_functions.run_availability_tests()
        
        # Should have issues due to slow services
        assert len(result.issues) > 0
        assert result.overall_score < 100
    
    def test_critical_failure_scenario(self):
        """Test a system with critical service failure"""
        fitness_functions = AvailabilityFitnessFunctions()
        
        # Make critical service unavailable
        fitness_functions.services['group_buying_service'].set_availability(False)
        
        result = fitness_functions.run_availability_tests()
        
        # Should fail critical path
        assert result.critical_path_available is False
        assert result.is_healthy is False
        assert result.overall_score < 80


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"]) 