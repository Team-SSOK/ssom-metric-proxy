# SSOM-METRIC-PROXY

**SSOM-METRIC-PROXY**는 SSOM 프로젝트의 모니터링 시스템에서 Prometheus Alertmanager의 웹훅을 받아, 필요한 정보를 가공해 메인 서버로 전달하는 프록시 서버입니다.

- Prometheus Alertmanager에서 전달받은 JSON 웹훅을 수신합니다.
- 메인 서버에서 활용할 수 있도록 필요한 정보만 추출 및 가공합니다.
- 가공한 정보를 메인 서버에 다시 웹훅 형태로 전달합니다.

---

## 기술 스택

- **Python** 3.13
- **FastAPI** 0.115.12

---

## 실행 방법

### 1. 사전 준비

- Docker 및 Docker Compose가 설치된 환경이 필요합니다.

### 2. 서비스 실행

```bash
docker-compose up -d
```

### 3. 서비스 중지

```bash
docker-compose down
```
