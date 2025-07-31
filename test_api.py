import requests
import sys

def test_api(base_url="http://localhost:8000"):
    """
    Test the GuessIt API with various scenarios.
    
    Args:
        base_url: The base URL of the API
    """
    print("Testing GuessIt API...")
    
    # Test 1: Valid filename
    print("\nTest 1: Valid filename")
    filename = "The.Big.Bang.Theory.S05E17.720p.HDTV.X264-DIMENSION.mkv"
    response = requests.get(f"{base_url}/api/guess", params={"it": filename})
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response:")
        for key, value in response.json().items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: No filename (should return 400)
    print("\nTest 2: No filename (should return 400)")
    response = requests.get(f"{base_url}/api/guess")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test 3: Invalid input that might cause an error (should return 500)
    # Note: This is a contrived example; actual errors would depend on guessit's behavior
    print("\nTest 3: Input that might cause an error (should return 500)")
    try:
        # Sending a very large string that might cause memory issues
        large_filename = "x" * 10000000  # 10 million characters
        response = requests.get(f"{base_url}/api/guess", params={"it": large_filename})
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    # Use command line argument as base URL if provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(base_url)