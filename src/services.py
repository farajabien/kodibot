"""
Services for KodiBOT - Authentication, Data, and Logging
"""

import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import Citizens, LinkedUsers, Taxes, Parcels, Procedures, ChatLogs
import json
import uuid

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
            existing_link.citizen_id = citizen_id
            existing_link.otp_code = otp
            existing_link.otp_expires_at = otp_expires
            existing_link.is_linked = False
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
        
        if linked_user.otp_expires_at < datetime.utcnow():
            return {"success": False, "message": "Code OTP expiré"}
        
        if linked_user.otp_code != otp_code:
            return {"success": False, "message": "Code OTP incorrect"}
        
        # Complete linking
        linked_user.is_linked = True
        linked_user.linked_at = datetime.utcnow()
        linked_user.otp_code = None
        linked_user.otp_expires_at = None
        
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
            "date_naissance": citizen.date_of_birth.strftime("%d/%m/%Y") if citizen.date_of_birth else "Non définie",
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
                "echeance": tax.due_date.strftime("%d/%m/%Y") if tax.due_date else "Non définie"
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
                "superficie": f"{parcel.area_sqm} m²" if parcel.area_sqm else "Non définie",
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
            "etapes": json.loads(procedure.steps) if procedure.steps else [],
            "documents_requis": json.loads(procedure.required_documents) if procedure.required_documents else [],
            "duree_estimee": procedure.estimated_duration,
            "cout": procedure.cost,
            "departement": procedure.department
        }

class LoggingService:
    @staticmethod
    def log_message(phone_number: str, message_text: str, direction: str, 
                   intent: str = None, confidence: float = None, 
                   citizen_id: str = None, db: Session = None):
        """Log chat message"""
        chat_log = ChatLogs(
            phone_number=phone_number,
            citizen_id=citizen_id,
            message_text=message_text,
            direction=direction,
            intent=intent,
            confidence=confidence
        )
        db.add(chat_log)
        db.commit()
        return chat_log
    
    @staticmethod
    def update_response_accuracy(log_id: int, accuracy: float, db: Session):
        """Update response accuracy score"""
        chat_log = db.query(ChatLogs).filter(ChatLogs.id == log_id).first()
        if chat_log:
            chat_log.response_accuracy = accuracy
            db.commit()

class IntentHandlers:
    @staticmethod
    def handle_get_profile(citizen_id: str, db: Session, slots: dict = None):
        """Handle profile information requests"""
        return DataService.get_profile_data(citizen_id, db)
    
    @staticmethod
    def handle_get_tax_info(citizen_id: str, db: Session, slots: dict = None):
        """Handle tax information requests"""
        return DataService.get_tax_data(citizen_id, db)
    
    @staticmethod
    def handle_get_parcels(citizen_id: str, db: Session, slots: dict = None):
        """Handle parcel information requests"""
        return DataService.get_parcels_data(citizen_id, db)
    
    @staticmethod
    def handle_get_procedures(citizen_id: str, db: Session, slots: dict = None):
        """Handle procedure information requests"""
        procedure_name = slots.get("procedure_name") if slots else None
        return DataService.get_procedures_data(procedure_name, db)

# Intent mapping
INTENT_HANDLERS = {
    "profile": IntentHandlers.handle_get_profile,
    "tax_info": IntentHandlers.handle_get_tax_info,
    "parcels": IntentHandlers.handle_get_parcels,
    "procedures": IntentHandlers.handle_get_procedures,
} 