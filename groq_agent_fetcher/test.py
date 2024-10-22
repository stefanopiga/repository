# import requests
#
# url = "http://telemetry.crewai.com:4318/v1/traces"
# timeout = 30  # Aumenta il timeout a 30 secondi
#
# try:
#    response = requests.post(url, timeout=timeout)
#    response.raise_for_status()  # Solleva un'eccezione per codici di stato HTTP 4xx/5xx
#    print("Connessione riuscita:", response.status_code)
# except requests.exceptions.RequestException as e:
#    print("Errore di connessione:", e)
#

import logging
import requests

# Configura il logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CustomTelemetryTool:
    """Strumento telemetria personalizzata"""

    name: str = "CustomTelemetryTool"
    description: str = "Strumento per la telemetria personalizzata."

    def _run(self, data: dict) -> str:
        try:
            url = "http://telemetry.crewai.com:4318/v1/traces"
            headers = {'Content-Type': 'application/json'}
            logger.debug(f"Sending data to {url}: {data}")
            response = requests.post(
                url, json=data, headers=headers, timeout=30)
            logger.debug(
                f"Response status: {response.status_code}, response body: {response.text}")
            response.raise_for_status()
            return "Telemetria inviata con successo"
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"HTTP error: {e.response.status_code} {e.response.text}")
            return f"Errore HTTP: {e.response.status_code} {e.response.text}"
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante l'invio della telemetria: {e}")
            return f"Errore durante l'invio della telemetria: {e}"


# Utilizzo del nuovo strumento di telemetria
telemetry_tool = CustomTelemetryTool()

# Esempio di dati di telemetria
example_data = {
    "traceId": "abcd1234",
    "spans": [
        {
            "spanId": "efgh5678",
            "name": "example-span",
            "startTime": "2023-06-15T12:00:00Z",
            "endTime": "2023-06-15T12:01:00Z",
            "attributes": {
                "service.name": "example-service",
                "host.name": "example-host",
                "http.method": "GET",
                "http.url": "http://example.com/api"
            }
        }
    ]
}

result = telemetry_tool._run(example_data)
print(result)
