ALLOWED_TRANSITIONS = {
    "SUBMITTED": ["IN_REVIEW"],
    "IN_REVIEW": ["APPROVED", "REJECTED"],
    "APPROVED": [],
    "REJECTED": ["SUBMITTED"],
}


def validate_status_transition(old_status, new_status):
    allowed = ALLOWED_TRANSITIONS.get(old_status, [])

    if new_status not in allowed:
        raise ValueError(
            f"Cannot change status from {old_status} to {new_status}."
        )