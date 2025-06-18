#!/usr/bin/env python3
"""
Simple test script for Kodibot API
Run this after starting the server with: uvicorn main:app --reload
"""

import requests
import json
from config import TestConfig

def test_chat(phone_number, message):
    """Test the chat endpoint with a message"""
    url = TestConfig.get_api_url("/chat")
    payload = {"phone_number": phone_number, "message": message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def test_linking(phone_number, citizen_id):
    """Test account linking"""
    url = TestConfig.get_api_url("/link-account")
    payload = {"phone_number": phone_number, "citizen_id": citizen_id}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def test_otp(phone_number, otp_code):
    """Test OTP verification"""
    url = TestConfig.get_api_url("/verify-otp")
    payload = {"phone_number": phone_number, "otp_code": otp_code}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def main():
    """Run some test conversations including linking process"""
    print("🤖 Testing KodiBOT API - Complete Flow")
    print("=" * 60)
    
    # Test data from centralized config
    test_phone = TestConfig.TEST_PHONE_UNLINKED
    linked_phone = TestConfig.TEST_PHONE_LINKED
    citizen_id = TestConfig.TEST_CITIZEN_ID
    
    print("\n=== TEST 1: Unlinked User (should prompt for linking) ===")
    result = test_chat(test_phone, "Bonjour")
    print(f"👤 User: Bonjour")
    if "response" in result:
        print(f"🤖 KodiBOT: {result['response']}")
        if result.get("requires_linking"):
            print("🔗 Linking required!")
    
    print("\n=== TEST 2: Account Linking Process ===")
    print(f"👤 User: Linking with citizen ID {citizen_id}")
    link_result = test_linking(test_phone, citizen_id)
    print(f"🔗 Linking result: {link_result}")
    
    if link_result.get("success") and "otp" in link_result:
        otp = link_result["otp"]
        print(f"\n👤 User: OTP verification with {otp}")
        otp_result = test_otp(test_phone, otp)
        print(f"✅ OTP result: {otp_result}")
    
    print("\n=== TEST 3: Linked User Conversation ===")
    test_messages = [
        "Bonjour",
        "Quel est mon solde de taxe foncière?",
        "Quelle est mon adresse?",
        "Mes parcelles",
        "Comment renouveler mon permis?",
        "Merci beaucoup"
    ]
    
    for message in test_messages:
        print(f"\n👤 User ({linked_phone}): {message}")
        result = test_chat(linked_phone, message)
        
        if "response" in result:
            print(f"🤖 KodiBOT: {result['response']}")
        elif "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"🔍 Raw response: {result}")
    
    print("\n=== TEST 4: Analytics ===")
    try:
        analytics_response = requests.get(TestConfig.get_api_url("/analytics/popular-intents"))
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print("📊 Popular Intents:")
            for intent_data in analytics.get("popular_intents", []):
                print(f"   • {intent_data['intent']}: {intent_data['count']} fois")
    except:
        print("❌ Could not fetch analytics")

if __name__ == "__main__":
    main() 