from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ChatRequest(BaseModel):
    phone_number: str
    message: str

class ChatResponse(BaseModel):
    response: Optional[str] = None
    error: Optional[str] = None
    requires_linking: bool = False
    linking_in_progress: bool = False
    user_linked: bool = False
    intent: Optional[str] = None
    confidence: Optional[float] = None

class LinkingRequest(BaseModel):
    phone_number: str
    citizen_id: str

class OTPVerificationRequest(BaseModel):
    phone_number: str
    otp_code: str

class LinkingResponse(BaseModel):
    success: bool
    message: str
    otp: Optional[str] = None

# K-CAF Models
class KCAF_Apartment(BaseModel):
    occupant_actuel: str # propriétaire, locataire, vacant
    nom_occupant: Optional[str] = None
    telephone_occupant: Optional[str] = None
    montant_loyer: Optional[float] = None
    devise_loyer: Optional[str] = None # USD, CDF
    date_debut_contrat: Optional[str] = None
    date_fin_contrat: Optional[str] = None

class KCAF_RecordCreate(BaseModel):
    parcel_number: str
    nature_propriete: str
    usage_principal: str
    nom_proprietaire: str
    nationalite_proprietaire: str
    type_possession: str
    telephone_proprietaire: Optional[str] = None
    etat_civil_proprietaire: Optional[str] = None
    sexe_proprietaire: Optional[str] = None
    adresse_commune: str
    adresse_quartier: str
    adresse_avenue: str
    adresse_numero: str
    type_personne: str
    type_batiment: str
    nombre_etages: str
    nombre_appartements: int
    nombre_appartements_vides: int
    appartements_details: Optional[List[KCAF_Apartment]] = None
    plaque_identification: bool
    raccordements: Dict[str, bool]
    distance_sante: str
    distance_education: str
    acces_eau_potable: Dict[str, bool]
    gestion_dechets: Dict[str, bool]
    photo_url: Optional[str] = None
    montant_a_payer: float
    etat: str
    numero_collecteur: str

class KCAF_RecordResponse(KCAF_RecordCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True