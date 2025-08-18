import requests
import sys
import json
from datetime import datetime

class OtimizaVendaAPITester:
    def __init__(self, base_url="https://otimizavenda.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details
        })

    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Status: {data.get('status', 'unknown')}, Message: {data.get('message', 'no message')}"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, str(e))
            return False

    def test_sales_calculation(self):
        """Test sales calculation endpoint"""
        test_data = {
            "produto": "Fone Bluetooth",
            "preco_custo": 50.00,
            "impostos": 5.00,
            "frete": 10.00,
            "margem_desejada": 20.0
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/calcular-vendas", 
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Verify calculation logic
                expected_custo_total = 50.00 + 5.00 + 10.00  # 65.00
                expected_preco_venda = expected_custo_total / (1 - 0.20)  # 65 / 0.8 = 81.25
                expected_lucro_bruto = expected_preco_venda - 50.00  # 81.25 - 50 = 31.25
                expected_lucro_liquido = expected_preco_venda - expected_custo_total  # 81.25 - 65 = 16.25
                
                actual_preco_venda = data.get('preco_venda', 0)
                actual_lucro_bruto = data.get('lucro_bruto', 0)
                actual_lucro_liquido = data.get('lucro_liquido', 0)
                
                calculation_correct = (
                    abs(actual_preco_venda - expected_preco_venda) < 0.01 and
                    abs(actual_lucro_bruto - expected_lucro_bruto) < 0.01 and
                    abs(actual_lucro_liquido - expected_lucro_liquido) < 0.01
                )
                
                if calculation_correct:
                    details = f"Calculation correct - Preço: R${actual_preco_venda}, Lucro Bruto: R${actual_lucro_bruto}, Lucro Líquido: R${actual_lucro_liquido}"
                else:
                    details = f"Calculation incorrect - Expected: R${expected_preco_venda:.2f}, Got: R${actual_preco_venda}"
                    success = False
            else:
                details = f"Status code: {response.status_code}, Response: {response.text[:200]}"
                
            self.log_test("Sales Calculation", success, details)
            return success
        except Exception as e:
            self.log_test("Sales Calculation", False, str(e))
            return False

    def test_calculation_history(self):
        """Test calculation history endpoint"""
        try:
            response = requests.get(f"{self.api_url}/historico-calculos", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Retrieved {len(data)} calculation records"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Calculation History", success, details)
            return success
        except Exception as e:
            self.log_test("Calculation History", False, str(e))
            return False

    def test_niches_endpoint(self):
        """Test niches endpoint"""
        try:
            response = requests.get(f"{self.api_url}/nichos", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                expected_niches = ["Produtos para Pets", "Fitness em Casa", "Produtos Sustentáveis", "Tech Gadgets"]
                found_niches = [niche.get('nome', '') for niche in data]
                
                all_found = all(niche in found_niches for niche in expected_niches)
                details = f"Found {len(data)} niches: {', '.join(found_niches[:3])}..."
                
                if not all_found:
                    success = False
                    details += " - Missing expected niches"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Niches Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Niches Endpoint", False, str(e))
            return False

    def test_suppliers_endpoint(self):
        """Test suppliers endpoint"""
        try:
            response = requests.get(f"{self.api_url}/fornecedores", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                expected_suppliers = ["TechSupply Brasil", "PetWorld Fornecedor", "EcoVerde Distribuidora"]
                found_suppliers = [supplier.get('nome', '') for supplier in data]
                
                all_found = all(supplier in found_suppliers for supplier in expected_suppliers)
                details = f"Found {len(data)} suppliers: {', '.join(found_suppliers)}"
                
                if not all_found:
                    success = False
                    details += " - Missing expected suppliers"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Suppliers Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Suppliers Endpoint", False, str(e))
            return False

    def test_trends_endpoint(self):
        """Test trends endpoint"""
        try:
            response = requests.get(f"{self.api_url}/tendencias", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                expected_trends = ["Air Fryer", "Plantas Artificiais", "Produtos para Home Office"]
                found_trends = [trend.get('produto', '') for trend in data]
                
                all_found = all(trend in found_trends for trend in expected_trends)
                details = f"Found {len(data)} trends: {', '.join(found_trends)}"
                
                if not all_found:
                    success = False
                    details += " - Missing expected trends"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Trends Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Trends Endpoint", False, str(e))
            return False

    def test_filter_functionality(self):
        """Test filter functionality for endpoints"""
        try:
            # Test niche filtering
            response = requests.get(f"{self.api_url}/nichos?categoria=Animais", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Should return only "Produtos para Pets" which has categoria "Animais"
                filtered_correctly = len(data) == 1 and data[0].get('nome') == 'Produtos para Pets'
                details = f"Niche filter test - Found {len(data)} items"
                
                if not filtered_correctly:
                    success = False
                    details += " - Filter not working correctly"
            else:
                details = f"Status code: {response.status_code}"
                
            self.log_test("Filter Functionality", success, details)
            return success
        except Exception as e:
            self.log_test("Filter Functionality", False, str(e))
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting OtimizaVenda Backend API Tests")
        print("=" * 50)
        
        # Test in order of importance
        tests = [
            self.test_health_check,
            self.test_sales_calculation,
            self.test_calculation_history,
            self.test_niches_endpoint,
            self.test_suppliers_endpoint,
            self.test_trends_endpoint,
            self.test_filter_functionality
        ]
        
        for test in tests:
            test()
            print()
        
        # Print summary
        print("=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All backend tests passed! Backend is working correctly.")
            return True
        else:
            print("⚠️  Some backend tests failed. Issues found:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['name']}: {result['details']}")
            return False

def main():
    tester = OtimizaVendaAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())