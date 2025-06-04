def find_ssok_prefixed_value(labels: dict) -> str | None:
    # 딕셔너리 안에서 ssok-로 시작하는 값을 찾아서 반환
    field_order = ["container", "job", "deployment", "service"]

    for field in field_order:
        value = labels.get(field)
        if isinstance(value, str) and value.startswith("ssok-"):
            return value
    return None

def parse_alert_webhook(data: dict) -> dict:
    alerts = data.get("alerts", [])
    results = []
    for alert in alerts:
        labels = alert.get("labels", {})
        alertname = labels.get("alertname")

        # 지정 필드 순서대로 ssok- prefix 값을 찾음
        ssok_value = find_ssok_prefixed_value(labels)
        # ssok_value가 없으면 alertname으로 대체
        app_value = ssok_value if ssok_value else alertname

        severity = labels.get("severity")
        description = alert.get("annotations").get("description", "")

        results.append({
            "app": app_value,
            "level": severity,
            "message": (alertname or "") + " - " + (description or ""),
            "timestamp": alert.get("startsAt"),
            "id": alert.get("fingerprint")
        })

    payload = {
        "alerts": results
    }
    return payload
