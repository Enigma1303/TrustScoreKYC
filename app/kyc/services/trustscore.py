from kyc.models import DocumentUpload

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


def compute_trust_score(application):
    document_score = compute_document_completion_score(application)
    resubmission_penalty = calculate_resubmission_score(application)

    # Ensure score doesn't go below 0
    final_ratio_score = max(document_score - resubmission_penalty, 0)

    # Convert to 0–100 scale
    trust_score = int(final_ratio_score * 100)

    # Determine risk level
    if trust_score >= 80:
        risk_level = "LOW"
    elif trust_score >= 50:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return trust_score, risk_level


