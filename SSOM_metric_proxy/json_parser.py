from datetime import datetime
import pytz

def find_ssok_prefixed_value(labels: dict) -> str | None:
    # 딕셔너리 안에서 ssok-로 시작하는 값을 찾아서 반환
    field_order = ["container", "job", "deployment", "service"]

    for field in field_order:
        value = labels.get(field)
        if isinstance(value, str) and value.startswith("ssok-"):
            return value
    return None

def convert_utc_to_kst_formatted(utc_ts: str) -> str | None:
    # UTC ISO8601 타임스탬프 문자열을 KST로 변환하고 "%Y-%m-%dT%H:%M:%S" 포맷으로 반환
    kst = pytz.timezone('Asia/Seoul')
    if not utc_ts:
        return None
    try:
        dt_utc = datetime.strptime(utc_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        dt_utc = datetime.strptime(utc_ts, "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt_utc.replace(tzinfo=pytz.utc)
    dt_kst = dt_utc.astimezone(kst)
    return dt_kst.strftime("%Y-%m-%dT%H:%M:%S")

def parse_alert_webhook(data: dict) -> dict:
    alerts = data.get("alerts", [])
    results = []
    for alert in alerts:
        labels = alert.get("labels", {})
        alertname = labels.get("alertname")
        description = alert.get("annotations").get("description", "")

        # 지정 필드 순서대로 ssok- prefix 값을 찾음
        ssok_value = find_ssok_prefixed_value(labels)

        # ssok_value가 없으면 alertname으로 대체
        app_value = ssok_value if ssok_value else alertname

        level_value = labels.get("severity")
        message_value = (alertname or "") + " - " + (description or "")
        timestamp_value = convert_utc_to_kst_formatted(alert.get("startsAt"))
        id_value = alert.get("fingerprint")

        results.append({
            "app": app_value,
            "level": level_value,
            "message": message_value,
            "timestamp": timestamp_value,
            "id": id_value
        })

    payload = {
        "alerts": results
    }
    return payload
