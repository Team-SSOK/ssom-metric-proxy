def find_ssok_prefixed_value(labels: dict) -> str:
    # 딕셔너리 안에서 ssok-로 시작하는 값을 찾아서 반환
    field_order = ["container", "job", "deployment", "service"]

    for field in field_order:
        value = labels.get(field)
        if isinstance(value, str) and value.startswith("ssok-"):
            return value
    return "Not Found"

def parse_alert_webhook(data: dict) -> dict:
    alerts = data.get("alerts", [])
    results = []
    for alert in alerts:
        labels = alert.get("labels", {})

        # 지정 필드 순서대로 ssok- prefix 값을 찾음
        ssok_value = find_ssok_prefixed_value(labels)

        severity = labels.get("severity")
        description = alert.get("annotations").get("description")

        results.append({
            "app": ssok_value,
            "level": severity,
            "message": labels.get("alertname") + " - " + description,
            "timestamp": alert.get("startsAt"),
            "id": alert.get("fingerprint")
        })

    payload = {
        "alerts": results,
    }
    return payload
