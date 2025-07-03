"""
Simple test for minimal architecture fitness function
"""

import pytest
from fitness_functions import fitness_functions, AvailabilityResult


def test_architecture():
    """Test the minimal architecture fitness function"""
    result = fitness_functions.run_architecture_test()
    
    # Check result type
    assert isinstance(result, AvailabilityResult)
    
    # Check that system is healthy
    assert result.is_healthy
    assert result.critical_path_available
    assert result.overall_score == 100
    
    # Check that all critical services are present and healthy
    assert len(result.services) == 7  # 7 critical services
    assert all(s.is_healthy for s in result.services.values())
    
    # Check that no issues are detected
    assert result.issues == []
    
    # Verify all expected services are present
    expected_services = [
        'group_buying_service',
        'order_service', 
        'payment_service',
        'logistics_service',
        'notification_service',
        'database',
        'cache'
    ]
    for service_name in expected_services:
        assert service_name in result.services
        assert result.services[service_name].is_healthy


if __name__ == "__main__":
    pytest.main([__file__]) 