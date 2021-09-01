from typing import Callable

from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info


def error_metric() -> Callable[[Info], None]:
    """Basic error counter metric.

    Refer to prometheus_fastapi_instrumentator documentation for details.
    """
    metric = Counter(
        "errors_total",
        "Errors counter by http method and error type",
        labelnames=(
            "method",
            "error_type",
        ),
    )

    def instrumentation(info: Info) -> None:
        if info.response.status_code == 422:
            metric.labels(info.request.method, "validation error").inc()
        if info.response.status_code == 409:
            metric.labels(info.request.method, "duplicate").inc()
        if info.response.status_code == 404:
            metric.labels(info.request.method, "not found").inc()

    return instrumentation


metrics_instrumentator = Instrumentator(excluded_handlers=["/docs", "/openapi.json", "/metrics"])
metrics_instrumentator.add(error_metric())
metrics.requests()
