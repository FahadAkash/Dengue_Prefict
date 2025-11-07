import sys
import os

# Add the parent directories to the path to import from other modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from api.BaseAPI import get_recommendation

def test_enhanced_recommendations():
    """Test the enhanced recommendation system"""
    
    print("Testing Enhanced Dengue Risk Recommendations\n")
    
    # Test high risk recommendation
    print("1. High Risk Recommendation (75%):")
    high_risk_rec = get_recommendation(0.75, "Badda")
    print(high_risk_rec)
    print("\n" + "="*60 + "\n")
    
    # Test medium risk recommendation
    print("2. Medium Risk Recommendation (55%):")
    med_risk_rec = get_recommendation(0.55, "Mirpur")
    print(med_risk_rec)
    print("\n" + "="*60 + "\n")
    
    # Test low risk recommendation
    print("3. Low Risk Recommendation (25%):")
    low_risk_rec = get_recommendation(0.25, "Gulshan")
    print(low_risk_rec)
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_enhanced_recommendations()