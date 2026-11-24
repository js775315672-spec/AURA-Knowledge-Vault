import re
PROJECTS = {"QuizNote", "Octopus", "Ouroboros", "Cerberus", "Fenrir", "SteadyTrade"}
STATES = {"UNVERIFIED", "INFERRED", "CONFLICT", "REJECTED", "DEPRECATED"}
def validate(record):
    if not isinstance(record, dict) or set(record) != {"id","project","status","sha256","synthetic"}:
        raise ValueError("invalid fields")
    if record["project"] not in PROJECTS or record["status"] not in STATES:
        raise ValueError("invalid project or status")
    if record["synthetic"] is not True:
        raise ValueError("public fixture must be synthetic")
    for key, pattern in (("id", r"KNOW-[A-Z0-9-]{1,64}"), ("sha256", r"[0-9a-f]{64}")):
        if not isinstance(record[key], str) or not re.fullmatch(pattern, record[key]):
            raise ValueError("invalid " + key)
    return True
