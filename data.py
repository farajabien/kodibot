user_tax_data = {
    "user_id": "USR123456",
    "personal_info": {
        "first_name": "Alex",
        "last_name": "Johnson",
        "ssn": "123-45-6789",
        "dob": "1985-06-12",
        "email": "alex.johnson@example.com",
        "phone": "254729054607",
        "address": {
            "street": "789 Main Street",
            "city": "Springfield",
            "state": "CA",
            "zip": "90210",
            "country": "USA"
        },
        "filing_status": "Married Filing Jointly",
        "dependents": [
            {"name": "Emma Johnson", "dob": "2012-05-16", "relationship": "Daughter"},
            {"name": "Liam Johnson", "dob": "2015-09-20", "relationship": "Son"}
        ]
    },

    "employment_info": {
        "employer": "TechNova Inc.",
        "employer_id": "EID876543",
        "occupation": "Software Engineer",
        "wages": 112500.00,
        "withholding_tax": 18200.00,
        "bonus": 10000.00,
        "other_income": [
            {"type": "freelance", "amount": 7000.00},
            {"type": "stock dividends", "amount": 1500.00}
        ]
    },

    "deductions_and_credits": {
        "standard_deduction": True,
        "itemized_deductions": {
            "mortgage_interest": 8500.00,
            "charitable_donations": 1200.00,
            "medical_expenses": 2300.00,
            "property_taxes": 3500.00
        },
        "education_credits": {
            "lifetime_learning_credit": 2000.00
        },
        "child_tax_credit": 4000.00,
        "retirement_contributions": {
            "401k": 18000.00,
            "ira": 6000.00
        }
    },

    "property_info": {
        "primary_residence": {
            "purchase_price": 450000.00,
            "current_value": 525000.00,
            "mortgage_balance": 325000.00,
            "property_tax_paid": 3600.00
        },
        "rental_properties": [
            {
                "address": "123 Rental St, Los Angeles, CA",
                "annual_rental_income": 24000.00,
                "expenses": {
                    "maintenance": 3000.00,
                    "insurance": 900.00,
                    "property_tax": 2400.00
                }
            }
        ]
    },

    "investments": {
        "capital_gains": [
            {"asset": "TSLA stock", "gain": 3500.00, "long_term": True},
            {"asset": "Bitcoin", "gain": 1200.00, "long_term": False}
        ],
        "loss_carryforward": 500.00,
        "dividends": 1500.00,
        "interest_income": 800.00
    },

    "tax_filing_history": [
        {
            "year": 2023,
            "status": "Filed",
            "refund": 1200.00,
            "tax_paid": 15800.00,
            "filing_date": "2024-04-10"
        },
        {
            "year": 2022,
            "status": "Filed",
            "refund": 950.00,
            "tax_paid": 14500.00,
            "filing_date": "2023-04-12"
        }
    ],

    "current_year_estimate": {
        "estimated_tax_liability": 16700.00,
        "payments_made": 14000.00,
        "estimated_refund_or_due": -2700.00  # Negative means due
    },

    "notices_and_audits": {
        "irs_notices": [
            {"date": "2024-08-15", "type": "Underpayment Notice", "amount": 800.00}
        ],
        "audit_history": []
    },

    "compliance_flags": {
        "missing_forms": ["1099-K", "1098-E"],
        "late_filing": False,
        "underpayment_penalty": True
    }
}
