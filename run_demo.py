#!/usr/bin/env python3
"""
Demo script for Availability Fitness Functions
==============================================

Shows different scenarios and their impact on system availability.
"""

from fitness_functions import fitness_functions
import time


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


def demo_healthy_system():
    """Demo 1: Healthy system"""
    print_header("SCENARIO 1: Healthy System")
    print("All services are working normally with good response times.")
    
    result = fitness_functions.run_availability_tests()
    print_result(result)


def demo_degraded_system():
    """Demo 2: Degraded system"""
    print_header("SCENARIO 2: Degraded System")
    print("Some services are slow, affecting overall performance.")
    
    # Make some services slow
    fitness_functions.services['payment_service'].base_response_time = 2.5
    fitness_functions.services['logistics_service'].base_response_time = 2.0
    
    result = fitness_functions.run_availability_tests()
    print_result(result)
    
    # Reset for next demo
    fitness_functions.services['payment_service'].base_response_time = 0.3
    fitness_functions.services['logistics_service'].base_response_time = 0.25


def demo_critical_failure():
    """Demo 3: Critical service failure"""
    print_header("SCENARIO 3: Critical Service Failure")
    print("The group buying service is completely down - critical path fails.")
    
    # Make critical service unavailable
    fitness_functions.simulate_service_failure('group_buying_service', False)
    
    result = fitness_functions.run_availability_tests()
    print_result(result)
    
    # Reset for next demo
    fitness_functions.simulate_service_failure('group_buying_service', True)


def demo_partial_failure():
    """Demo 4: Partial failure"""
    print_header("SCENARIO 4: Partial Failure")
    print("Payment service is down, but other services work.")
    
    # Make payment service unavailable
    fitness_functions.simulate_service_failure('payment_service', False)
    
    result = fitness_functions.run_availability_tests()
    print_result(result)
    
    # Reset for next demo
    fitness_functions.simulate_service_failure('payment_service', True)


def demo_high_load():
    """Demo 5: High load scenario"""
    print_header("SCENARIO 5: High Load")
    print("Testing system under high concurrent load.")
    
    print("\n🔍 Testing with 20 concurrent requests...")
    concurrent_results = fitness_functions.test_concurrent_availability(num_requests=20)
    
    print(f"\n📊 Load Test Results:")
    print(f"   Success Rate: {concurrent_results['success_rate']:.1%}")
    print(f"   Total Time: {concurrent_results['total_time']:.3f}s")
    print(f"   Requests/Second: {concurrent_results['requests_per_second']:.1f}")
    
    if concurrent_results['success_rate'] >= 0.95:
        print("   ✅ System handles high load well")
    else:
        print("   ❌ System struggles under high load")


def interactive_demo():
    """Interactive demo where user can control service states"""
    print_header("INTERACTIVE DEMO")
    print("You can control service availability and see the impact.")
    print("Available services:", list(fitness_functions.services.keys()))
    
    while True:
        print("\nOptions:")
        print("1. Test current system state")
        print("2. Toggle service availability")
        print("3. Reset all services to healthy")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            result = fitness_functions.run_availability_tests()
            print_result(result)
        
        elif choice == "2":
            service_name = input("Enter service name: ").strip()
            if service_name in fitness_functions.services:
                current_state = fitness_functions.services[service_name].is_available
                new_state = not current_state
                fitness_functions.simulate_service_failure(service_name, new_state)
                print(f"✅ {service_name} set to {'available' if new_state else 'unavailable'}")
            else:
                print(f"❌ Service '{service_name}' not found")
        
        elif choice == "3":
            for service_name in fitness_functions.services:
                fitness_functions.simulate_service_failure(service_name, True)
            print("✅ All services reset to healthy")
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


def main():
    """Main demo function"""
    print("🚀 Group Buying Platform - Availability Fitness Functions Demo")
    print("This demo shows how availability testing works with different scenarios.")
    
    # Run all demos
    demo_healthy_system()
    time.sleep(2)
    
    demo_degraded_system()
    time.sleep(2)
    
    demo_critical_failure()
    time.sleep(2)
    
    demo_partial_failure()
    time.sleep(2)
    
    demo_high_load()
    time.sleep(2)
    
    # Interactive demo
    interactive_demo()


if __name__ == "__main__":
    main() 