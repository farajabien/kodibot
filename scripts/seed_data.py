#!/usr/bin/env python3
"""
Script de peuplement de la base de données avec des données de test réalistes pour la RDC
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from src.database import get_db, Citizens, Taxes, Procedures, Parcels, LinkedUsers, create_tables
import json

def seed_database():
    """Populate database with sample data"""
    # 1. Create all tables
    create_tables()
    db = next(get_db())

    try:
        # 2. Seed Citizens
        citizen = Citizens(
            phone_number     = "+243123456789",
            citizen_id       = "CIT123456789",
            first_name       = "Jean",
            last_name        = "Kabila",
            email            = "jean.kabila@example.com",
            address          = "Avenue de la Liberté, Kinshasa, RDC",
            date_of_birth    = datetime(1980, 5, 15),
            is_verified      = True
        )
        db.add(citizen)

        # 3. Seed LinkedUsers
        linked = LinkedUsers(
            phone_number = citizen.phone_number,
            citizen_id   = citizen.citizen_id,
            is_linked    = True,
            linked_at    = datetime.utcnow()
        )
        db.add(linked)

        # 4. Seed Taxes
        taxes = [
            Taxes(
                citizen_id = citizen.citizen_id,
                tax_type   = "Taxe foncière",
                amount_due = 250000.0,
                amount_paid= 150000.0,
                due_date   = datetime(2024, 12, 31),
                status     = "pending",
                tax_year   = 2024
            ),
            Taxes(
                citizen_id = citizen.citizen_id,
                tax_type   = "Taxe professionnelle",
                amount_due = 180000.0,
                amount_paid= 180000.0,
                due_date   = datetime(2024, 6, 30),
                status     = "paid",
                tax_year   = 2024
            )
        ]
        db.add_all(taxes)

        # 5. Seed Procedures
        procedures = [
            Procedures(
                name                = "Renouvellement de permis de conduire",
                description         = "Procédure pour renouveler votre permis de conduire",
                steps               = json.dumps([
                    "1. Rassembler les documents requis",
                    "2. Se rendre au bureau des transports",
                    "3. Payer les frais de renouvellement",
                    "4. Passer l'examen médical",
                    "5. Récupérer le nouveau permis"
                ]),
                required_documents  = json.dumps([
                    "Ancien permis de conduire",
                    "Certificat médical",
                    "2 photos passeport",
                    "Reçu de paiement"
                ]),
                estimated_duration  = "2-3 semaines",
                cost                = 25000.0,
                department          = "Ministère des Transports"
            ),
            Procedures(
                name                = "Demande de passeport",
                description         = "Procédure pour obtenir un nouveau passeport",
                steps               = json.dumps([
                    "1. Remplir le formulaire de demande",
                    "2. Fournir les documents requis",
                    "3. Payer les frais consulaires",
                    "4. Attendre la production",
                    "5. Récupérer le passeport"
                ]),
                required_documents  = json.dumps([
                    "Acte de naissance",
                    "Carte d'identité",
                    "4 photos biométriques",
                    "Justificatif de domicile"
                ]),
                estimated_duration  = "4-6 semaines",
                cost                = 150000.0,
                department          = "Ministère des Affaires Étrangères"
            )
        ]
        db.add_all(procedures)

        # 6. Seed Parcels
        parcels = [
            Parcels(
                citizen_id     = citizen.citizen_id,
                parcel_number  = "P001-KIN-2024",
                property_type  = "Maison",
                address        = "Parcelle 123, Commune de Gombe, Kinshasa",
                area_sqm       = 500.0,
                estimated_value= 85_000_000.0,
                status         = "active"
            ),
            Parcels(
                citizen_id     = citizen.citizen_id,
                parcel_number  = "P002-KIN-2024",
                property_type  = "Terrain",
                address        = "Parcelle 456, Commune de Limete, Kinshasa",
                area_sqm       = 800.0,
                estimated_value= 45_000_000.0,
                status         = "active"
            )
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
