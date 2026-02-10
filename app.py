from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from utils.math_utils import generate_fibonacci, filter_primes, calculate_lcm, calculate_hcf
from utils.ai_utils import get_ai_response

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Your official Chitkara email
OFFICIAL_EMAIL = "naman0580.be23@chitkara.edu.in"

# Max integer limit constraint
MAX_INT = 2**51 - 1


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route('/bfhl', methods=['POST'])
def bfhl():
    try:
        if not request.is_json:
            return jsonify({
                "is_success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        valid_keys = ['fibonacci', 'prime', 'lcm', 'hcf', 'AI']
        present_keys = [key for key in valid_keys if key in data]
        
        if len(present_keys) == 0:
            return jsonify({
                "is_success": False,
                "error": "Request must contain exactly one of: fibonacci, prime, lcm, hcf, AI"
            }), 400
        
        if len(present_keys) > 1:
            return jsonify({
                "is_success": False,
                "error": "Request must contain exactly one operation key"
            }), 400
        
        operation = present_keys[0]
        
        # Fibonacci
        if operation == 'fibonacci':
            n = data['fibonacci']
            if not isinstance(n, int):
                return jsonify({"is_success": False,"error": "Fibonacci input must be an integer"}), 400
            
            if n < 0:
                return jsonify({"is_success": False,"error": "Fibonacci input must be non-negative"}), 400
            
            if n > 1000000:
                return jsonify({"is_success": False,"error": "Fibonacci input too large (max 50)"}), 400
            
            result = generate_fibonacci(n)
        
        # PRIME
        elif operation == 'prime':
            numbers = data['prime']
            if not isinstance(numbers, list):
                return jsonify({"is_success": False,"error": "Prime input must be an array"}), 400
            
            if not numbers:
                return jsonify({"is_success": False,"error": "Prime input array cannot be empty"}), 400
            
            if not all(isinstance(x, int) for x in numbers):
                return jsonify({"is_success": False,"error": "All elements in prime array must be integers"}), 400
            
            # NEW constraint
            if any(x > MAX_INT for x in numbers):
                return jsonify({
                    "is_success": False,
                    "error": "Prime input exceeds maximum integer limit"
                }), 400
            
            result = filter_primes(numbers)
        
        # LCM
        elif operation == 'lcm':
            numbers = data['lcm']

            if not isinstance(numbers, list):
                return jsonify({"is_success": False,"error": "LCM input must be an array"}), 400
            
            if not numbers:
                return jsonify({"is_success": False,"error": "LCM input array cannot be empty"}), 400
            
            if not all(isinstance(x, int) for x in numbers):
                return jsonify({"is_success": False,"error": "All elements in LCM array must be integers"}), 400
            
            if any(x <= 0 for x in numbers):
                return jsonify({"is_success": False,"error": "All elements in LCM array must be positive"}), 400

            if any(x > MAX_INT for x in numbers):
                return jsonify({
                    "is_success": False,
                    "error": "LCM input exceeds maximum integer limit"
                }), 400

            result = calculate_lcm(numbers)

            if result > MAX_INT:
                return jsonify({
                    "is_success": False,
                    "error": "LCM exceeds maximum integer limit"
                }), 400
        
        # HCF
        elif operation == 'hcf':
            numbers = data['hcf']
            if not isinstance(numbers, list):
                return jsonify({"is_success": False,"error": "HCF input must be an array"}), 400
            
            if not numbers:
                return jsonify({"is_success": False,"error": "HCF input array cannot be empty"}), 400
            
            if not all(isinstance(x, int) for x in numbers):
                return jsonify({"is_success": False,"error": "All elements in HCF array must be integers"}), 400
            
            if any(x <= 0 for x in numbers):
                return jsonify({"is_success": False,"error": "All elements in HCF array must be positive"}), 400
            
            # NEW constraint
            if any(x > MAX_INT for x in numbers):
                return jsonify({
                    "is_success": False,
                    "error": "HCF input exceeds maximum integer limit"
                }), 400
            
            
            result = calculate_hcf(numbers)

#a
            if result > MAX_INT:
                return jsonify({

                    "is_success": False,
                    "error": "HCF exceeds maximum integer limit"
                }), 400
        
        # AI
        elif operation == 'AI':
            # Validate input
            question = data['AI']
            if not isinstance(question, str):
                return jsonify({
                    "is_success": False,
                    "error": "AI input must be a string"
                }), 400
            
            if not question.strip():
                return jsonify({
                    "is_success": False,
                    "error": "AI input cannot be empty"
                }), 400
            
            result = get_ai_response(question)
        
        # Return successful response
        return jsonify({
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": result
        }), 200
        
    except KeyError as e:
        return jsonify({
            "is_success": False,
            "error": f"Missing required field: {str(e)}"
        }), 400
    
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": "Internal server error"
        }), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"is_success": False,"error": "Endpoint not found"}), 404




@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"is_success": False,"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"is_success": False,"error": "Internal server error"}), 500
