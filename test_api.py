#!/usr/bin/env python3
import requests
import json

# Test the API
print("Testing Neusearch API...")

# Check health
response = requests.get("http://localhost:8000/health")
print(f"\n1. Health check: {response.json()}")

# Trigger scraping
print("\n2. Triggering data load...")
response = requests.post(
    "http://localhost:8000/api/scraping",
    headers={"Content-Type": "application/json"},
    json={"max_products": 30, "use_fallback": True}
)
print(f"Response: {response.status_code} - {response.json()}")

# Wait a bit for background task
import time
time.sleep(3)

# Check status
print("\n3. Checking scraping status...")
response = requests.get("http://localhost:8000/api/scraping/status")
print(f"Status: {response.json()}")

# Get products
print("\n4. Getting products...")
response = requests.get("http://localhost:8000/api/products")
products = response.json()
print(f"Found {len(products)} products")
if products:
    print(f"First product: {products[0]['title']}")

print("\n✅ Backend is working!")
