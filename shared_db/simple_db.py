"""
Módulo simples de acesso ao banco de dados compartilhado
Funções: consultar, agendar, liberar, buscar por documento, add_payment e refund
"""
import json
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "appointments.json")
PAYMENTS_FILE = os.path.join(os.path.dirname(__file__), "payments.json")

def consultar_slots():
    """Retorna todos os slots do banco"""
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["available_slots"]

def agendar_slot(slot_id, patient_cpf):
    """Marca um slot como ocupado por um paciente"""
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Procura o slot e marca como ocupado
    for date, slots in data["available_slots"].items():
        for slot in slots:
            if slot["slot_id"] == slot_id:
                slot["available"] = False
                slot["patient"] = patient_cpf
                
                # Salva as mudanças
                with open(DB_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return {"success": True, "message": "Slot agendado"}
    
    return {"success": False, "error": "Slot não encontrado"}

def buscar_por_documento(documento):
    """Busca slot ocupado por um documento específico"""
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Procura o paciente em todas as datas
    for date, slots in data["available_slots"].items():
        for slot in slots:
            if slot.get("patient") == documento:
                return {
                    "success": True,
                    "found": True,
                    "data": {
                        "date": date,
                        "slot_id": slot["slot_id"],
                        "time": slot["time"],
                        "doctor_name": slot["doctor_name"],
                        "specialties": slot["specialties"]
                    }
                }
    
    return {
        "success": True,
        "found": False,
        "message": f"Nenhum agendamento encontrado para o documento {documento}"
    }

def liberar_slot(slot_id):
    """Libera um slot ocupado"""
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Procura o slot e libera
    for date, slots in data["available_slots"].items():
        for slot in slots:
            if slot["slot_id"] == slot_id:
                slot["available"] = True
                slot["patient"] = None
                
                # Salva as mudanças
                with open(DB_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return {"success": True, "message": "Slot liberado"}
    
    return {"success": False, "error": "Slot não encontrado"}

def add_payment(patient_name, document, date, specialty):
    """Adiciona um pagamento simples ao banco de dados"""
    with open(PAYMENTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Cria novo pagamento simples
    new_payment = {
        "patient_name": patient_name,
        "document": document,
        "date": date,
        "specialty": specialty
    }
    
    # Adiciona ao array
    data["payments"].append(new_payment)
    
    # Salva as mudanças
    with open(PAYMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {"success": True, "message": f"Pagamento de {patient_name} processado"}

def refund(document):
    """Remove pagamento do banco (reembolso)"""
    with open(PAYMENTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Busca e remove pagamento por documento
    for i, payment in enumerate(data["payments"]):
        if payment["document"] == document:
            removed_payment = data["payments"].pop(i)
            
            # Salva as mudanças
            with open(PAYMENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {"success": True, "message": f"Reembolso processado para {removed_payment['patient_name']}"}
    
    return {"success": False, "error": f"Nenhum pagamento encontrado para o documento {document}"}