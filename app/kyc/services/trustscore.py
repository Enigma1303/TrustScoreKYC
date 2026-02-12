from kyc.models import DocumentUpload
from django.utils import timezone

def compute_document_completion_score(application):
    required_documents=[
        doc.value for doc in DocumentUpload.DocumentType
    ]
    
    uploaded_docs_types=application.documents.values("document_type")
    unique_doc_type_count=uploaded_docs_types.distinct().count()

    totaldoctypes=len(required_documents)
    document_completion_score=unique_doc_type_count/totaldoctypes

    return document_completion_score

def calculate_resubmission_score(application):

    resubmissions=application.statushistory.filter(old_status="REJECTED",new_status="SUBMITTED").count()

    return resubmissions*0.1


def caclulate_profileconsistency_score(user):

    account_age_days=(timezone.now()-user.created_at).days 
    score=0
    if account_age_days > 365:
        score += 0.3
    elif account_age_days > 180:
        score += 0.2
    elif account_age_days > 30:
        score += 0.1
    
    return score


def compute_trust_score(application):
    user=application.user
    document_score = compute_document_completion_score(application)
    resubmission_penalty = calculate_resubmission_score(application)
    profile_consistency=caclulate_profileconsistency_score(user)
   

    final_ratio_score = max(document_score - resubmission_penalty + profile_consistency, 0)

    
    trust_score = int(final_ratio_score * 100)
    if trust_score >= 80:
        risk_level = "LOW"
    elif trust_score >= 50:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return trust_score, risk_level


