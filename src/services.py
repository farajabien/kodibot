"""
Services for KodiBOT - Authentication, Data, and Logging
"""

import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import Citizens, LinkedUsers, Taxes, Parcels, Procedures, ChatLogs, KCAF_Records
from .models import KCAF_RecordCreate
import json
import uuid
from typing import Optional

class AuthService:
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def is_user_linked(phone_number: str, db: Session) -> bool:
        """Check if user is already linked"""
        linked_user = db.query(LinkedUsers).filter(
            LinkedUsers.phone_number == phone_number,
            LinkedUsers.is_linked == True
        ).first()
        return linked_user is not None
    
    @staticmethod
    def get_citizen_by_phone(phone_number: str, db: Session):
        """Get citizen data by phone number"""
        linked_user = db.query(LinkedUsers).filter(
            LinkedUsers.phone_number == phone_number,
            LinkedUsers.is_linked == True
        ).first()
        
        if not linked_user:
            return None
            
        citizen = db.query(Citizens).filter(
            Citizens.citizen_id == linked_user.citizen_id
        ).first()
        
        return citizen
    
    @staticmethod
    def initiate_linking(phone_number: str, citizen_id: str, db: Session):
        """Start the linking process with OTP"""
        # Check if citizen exists
        citizen = db.query(Citizens).filter(Citizens.citizen_id == citizen_id).first()
        if not citizen:
            return {"success": False, "message": "Numéro de citoyen non trouvé"}
        
        # Generate OTP
        otp = AuthService.generate_otp()
        otp_expires = datetime.utcnow() + timedelta(minutes=10)
        
        # Save/update linking record
        existing_link = db.query(LinkedUsers).filter(
            LinkedUsers.phone_number == phone_number
        ).first()
        
        if existing_link:
            existing_link.citizen_id = citizen_id  # type: ignore
            existing_link.otp_code = otp  # type: ignore
            existing_link.otp_expires_at = otp_expires  # type: ignore
            existing_link.is_linked = False  # type: ignore
        else:
            new_link = LinkedUsers(
                phone_number=phone_number,
                citizen_id=citizen_id,
                otp_code=otp,
                otp_expires_at=otp_expires
            )
            db.add(new_link)
        
        db.commit()
        
        # For testing: return OTP in response (will be sent via SMS in production)
        return {
            "success": True, 
            "otp": otp, 
            "message": f"Code OTP généré: {otp}. (En production, ce code sera envoyé par SMS)"
        }
    
    @staticmethod
    def verify_otp(phone_number: str, otp_code: str, db: Session):
        """Verify OTP and complete linking"""
        linked_user = db.query(LinkedUsers).filter(
            LinkedUsers.phone_number == phone_number
        ).first()
        
        if not linked_user:
            return {"success": False, "message": "Aucune demande de liaison trouvée"}
        
        if linked_user.otp_expires_at < datetime.utcnow():  # type: ignore
            return {"success": False, "message": "Code OTP expiré"}
        
        if linked_user.otp_code != otp_code:  # type: ignore
            return {"success": False, "message": "Code OTP incorrect"}
        
        # Complete linking
        linked_user.is_linked = True  # type: ignore
        linked_user.linked_at = datetime.utcnow()  # type: ignore
        linked_user.otp_code = None  # type: ignore
        linked_user.otp_expires_at = None  # type: ignore
        
        db.commit()
        
        return {"success": True, "message": "Liaison réussie!"}

class DataService:
    @staticmethod
    def get_profile_data(citizen_id: str, db: Session):
        """Fetch citizen profile data"""
        citizen = db.query(Citizens).filter(Citizens.citizen_id == citizen_id).first()
        if not citizen:
            return None
        
        return {
            "nom": f"{citizen.first_name} {citizen.last_name}",
            "date_naissance": citizen.date_of_birth.strftime("%d/%m/%Y") if citizen.date_of_birth else "Non définie",  # type: ignore
            "adresse": citizen.address or "Non définie",
            "email": citizen.email or "Non définie"
        }
    
    @staticmethod
    def get_tax_data(citizen_id: str, db: Session):
        """Fetch tax information"""
        taxes = db.query(Taxes).filter(Taxes.citizen_id == citizen_id).all()
        
        tax_summary = []
        total_due = 0
        total_paid = 0
        
        for tax in taxes:
            tax_summary.append({
                "type": tax.tax_type,
                "montant_du": tax.amount_due,
                "montant_paye": tax.amount_paid,
                "statut": tax.status,
                "annee": tax.tax_year,
                "echeance": tax.due_date.strftime("%d/%m/%Y") if tax.due_date else "Non définie"  # type: ignore
            })
            total_due += tax.amount_due
            total_paid += tax.amount_paid
        
        return {
            "taxes": tax_summary,
            "total_du": total_due,
            "total_paye": total_paid,
            "solde": total_due - total_paid
        }
    
    @staticmethod
    def get_parcels_data(citizen_id: str, db: Session):
        """Fetch parcel/property information"""
        parcels = db.query(Parcels).filter(Parcels.citizen_id == citizen_id).all()
        
        parcels_list = []
        for parcel in parcels:
            parcels_list.append({
                "numero_parcelle": parcel.parcel_number,
                "type": parcel.property_type,
                "adresse": parcel.address,
                "superficie": f"{parcel.area_sqm} m²" if parcel.area_sqm else "Non définie",  # type: ignore
                "valeur_estimee": parcel.estimated_value,
                "statut": parcel.status
            })
        
        return {"parcelles": parcels_list, "nombre_total": len(parcels_list)}
    
    @staticmethod
    def get_procedures_data(procedure_name: str, db: Session):
        """Fetch procedure information"""
        if procedure_name:
            procedure = db.query(Procedures).filter(
                Procedures.name.ilike(f"%{procedure_name}%")
            ).first()
        else:
            # Return most common procedures
            procedures = db.query(Procedures).limit(5).all()
            return {"procedures": [{"nom": p.name, "description": p.description} for p in procedures]}
        
        if not procedure:
            return None
        
        return {
            "nom": procedure.name,
            "description": procedure.description,
            "etapes": json.loads(procedure.steps) if procedure.steps else [],  # type: ignore
            "documents_requis": json.loads(procedure.required_documents) if procedure.required_documents else [],  # type: ignore
            "duree_estimee": procedure.estimated_duration,
            "cout": procedure.cost,
            "departement": procedure.department
        }

    @staticmethod
    def create_kcaf_record(record_data: KCAF_RecordCreate, db: Session):
        """Create a new K-CAF record for a parcel."""
        existing_record = db.query(KCAF_Records).filter(KCAF_Records.parcel_number == record_data.parcel_number).first()
        if existing_record:
            return None

        record_dict = record_data.dict()
        if record_data.appartements_details:
            record_dict['appartements_details'] = [apt.dict() for apt in record_data.appartements_details]

        new_record = KCAF_Records(**record_dict)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record

    @staticmethod
    def get_kcaf_record_by_parcel(parcel_number: str, db: Session):
        """Fetch K-CAF record by parcel number."""
        return db.query(KCAF_Records).filter(KCAF_Records.parcel_number == parcel_number).first()

    @staticmethod
    def get_etax_status(citizen_id: str, db: Session):
        """Fetch E-Tax status and account information"""
        from .test_data import get_etax_record_by_citizen_id
        
        etax_record = get_etax_record_by_citizen_id(citizen_id)
        if not etax_record:
            return None
        
        # Format the response for better readability
        status_emoji = "✅" if etax_record["etax_status"] == "active" else "⚠️"
        verification_emoji = "✅" if etax_record["verification_level"] == "verified" else "⏳"
        
        return {
            "status": etax_record["etax_status"],
            "status_display": f"{status_emoji} {etax_record['etax_status'].title()}",
            "account_type": etax_record["account_type"],
            "verification_level": f"{verification_emoji} {etax_record['verification_level'].title()}",
            "registration_date": etax_record["registration_date"].strftime("%d/%m/%Y"),
            "last_login": etax_record["last_login"].strftime("%d/%m/%Y"),
            "payment_methods": etax_record["payment_methods"],
            "notifications_enabled": etax_record["notifications_enabled"],
            "auto_payment_setup": etax_record["auto_payment_setup"],
            "tax_returns_filed": etax_record["tax_returns_filed"],
            "last_filing_date": etax_record["last_filing_date"].strftime("%d/%m/%Y"),
            "compliance_score": etax_record["compliance_score"],
            "compliance_level": "Excellent" if etax_record["compliance_score"] >= 90 else 
                               "Bon" if etax_record["compliance_score"] >= 80 else
                               "Moyen" if etax_record["compliance_score"] >= 70 else "À améliorer"
        }

class LoggingService:
    @staticmethod
    def log_message(phone_number: str, message_text: str, direction: str, db: Session,
                   intent: Optional[str] = None, confidence: Optional[float] = None, 
                   citizen_id: Optional[str] = None):
        """Log chat message"""
        chat_log = ChatLogs(
            phone_number=phone_number,
            citizen_id=citizen_id,
            message_text=message_text,
            direction=direction,
            intent=intent,
            confidence=confidence
        )
        db.add(chat_log)  # type: ignore
        db.commit()
        return chat_log
    
    @staticmethod
    def update_response_accuracy(log_id: int, accuracy: float, db: Session):
        """Update response accuracy score"""
        chat_log = db.query(ChatLogs).filter(ChatLogs.id == log_id).first()
        if chat_log:
            chat_log.response_accuracy = accuracy  # type: ignore
            db.commit()

class IntentHandlers:
    @staticmethod
    def handle_get_profile(citizen_id: str, db: Session, slots: Optional[dict] = None):
        """Handle profile information requests"""
        return DataService.get_profile_data(citizen_id, db)
    
    @staticmethod
    def handle_get_tax_info(citizen_id: str, db: Session, slots: Optional[dict] = None):
        """Handle tax information requests"""
        return DataService.get_tax_data(citizen_id, db)
    
    @staticmethod
    def handle_get_parcels(citizen_id: str, db: Session, slots: Optional[dict] = None):
        """Handle parcel information requests"""
        return DataService.get_parcels_data(citizen_id, db)
    
    @staticmethod
    def handle_get_procedures(citizen_id: str, db: Session, slots: Optional[dict] = None):
        """Handle procedure information requests"""
        procedure_name = slots.get("procedure_name") if slots else None
        return DataService.get_procedures_data(procedure_name, db)  # type: ignore

    @staticmethod
    def handle_get_etax_status(citizen_id: str, db: Session, slots: Optional[dict] = None):
        """Handle E-Tax status information requests"""
        return DataService.get_etax_status(citizen_id, db)

# Intent mapping
INTENT_HANDLERS = {
    "profile": IntentHandlers.handle_get_profile,
    "tax_info": IntentHandlers.handle_get_tax_info,
    "parcels": IntentHandlers.handle_get_parcels,
    "procedures": IntentHandlers.handle_get_procedures,
    "etax_status": IntentHandlers.handle_get_etax_status,
} 