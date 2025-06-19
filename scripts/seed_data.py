#!/usr/bin/env python3
"""
Script de peuplement de la base de données avec des données de test réalistes pour la RDC
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from src.database import get_db, Citizens, Taxes, Procedures, Parcels, LinkedUsers, create_tables
from src.test_data import PRIMARY_CITIZEN, TEST_TAXES, TEST_PROCEDURES, TEST_PARCELS
import json

def seed_database():
    """Populate database with sample data"""
    # 1. Create all tables
    create_tables()
    db = next(get_db())

    try:
        # 2. Seed Citizens (using centralized test data)
        citizen = Citizens(**PRIMARY_CITIZEN)
        db.add(citizen)

        # 3. Seed LinkedUsers
        linked = LinkedUsers(
            phone_number = citizen.phone_number,
            citizen_id   = citizen.citizen_id,
            is_linked    = True,
            linked_at    = datetime.utcnow()
        )
        db.add(linked)

        # 4. Seed Taxes (using centralized test data)
        taxes = [
            Taxes(citizen_id=citizen.citizen_id, **tax_data) 
            for tax_data in TEST_TAXES
        ]
        db.add_all(taxes)

        # 5. Seed Procedures (using centralized test data)
        procedures = [
            Procedures(
                **{**proc_data, 
                   "steps": json.dumps(proc_data["steps"]),
                   "required_documents": json.dumps(proc_data["required_documents"])
                }
            )
            for proc_data in TEST_PROCEDURES
        ]
        db.add_all(procedures)

        # 6. Seed Parcels (using centralized test data)
        parcels = [
            Parcels(citizen_id=citizen.citizen_id, **parcel_data)
            for parcel_data in TEST_PARCELS
        ]
        db.add_all(parcels)

        # 7. (Optional) Seed Buildings
        if hasattr(PreparedLocals(), 'Buildings'):
            buildings = [
                Buildings(
                    citizen_id         = citizen.citizen_id,
                    building_id        = "B001-KIN-2024",
                    type               = "Appartement",
                    address            = "Immeuble XYZ, Kinshasa",
                    number_of_units    = 4,
                    estimated_value    = 60_000_000.0,
                    status             = "active"
                )
            ]
            db.add_all(buildings)

        # 8. Commit
        db.commit()
        print("✅ Base de données peuplée avec succès !")
        print(f"👤 Citoyen : {citizen.first_name} {citizen.last_name} (ID : {citizen.citizen_id})")
        print(f"💰 Taxes créées : {len(taxes)}")
        print(f"📋 Procédures créées : {len(procedures)}")
        print(f"🏠 Parcelles créées : {len(parcels)}")
        if 'buildings' in locals():
            print(f"🏢 Bâtiments créés : {len(buildings)}")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors du peuplement : {e}")
        raise

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
