# Delivery Platform Lab

Projeto educacional que simula uma plataforma de deploy de serviços.

## Tecnologias

- FastAPI
- Docker
- Prometheus
- Grafana
- GitHub Actions
- Pytest
- Ruff

## Fluxo de release

1. Build
2. Test
3. Deploy

Cada release gera métricas Prometheus e logs estruturados.

## Executar

docker compose up --build

## Endpoints

/health
/live
/ready
/release
/releases
/metrics

## Dashboards automáticos

Foi criado Dashboards automaticamente usando Grafana provisioning, cada gráfico coletado o JSON na interface gráfica.


[![CI](https://github.com/GuiReisSilva/delivery-platform-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/GuiReisSilva/delivery-platform-lab/actions)