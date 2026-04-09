from vastai import BenchmarkConfig, HandlerConfig, LogActionConfig, Worker, WorkerConfig


MODEL_SERVER_URL = "http://127.0.0.1"
MODEL_SERVER_PORT = 18000
MODEL_LOG_FILE = "/var/log/omnivoice/server.log"
MODEL_HEALTHCHECK_ENDPOINT = "/health"

MODEL_LOAD_LOG_MSG = [
    "Model loaded successfully.",
    "[PIPELINE] Model ready",
]

MODEL_ERROR_LOG_MSGS = [
    "Traceback (most recent call last):",
    "[PIPELINE] Model load FAILED",
    "[TTS] Generation failed",
]

MODEL_INFO_LOG_MSGS = [
    "[PIPELINE]",
    "[TTS]",
]


def request_parser(request: dict) -> dict:
    if isinstance(request, dict) and "payload" in request and isinstance(request["payload"], dict):
        return request["payload"]
    return request


def benchmark_generator() -> dict:
    return {
        "text": "Bonjour, test de benchmark OmniVoice sur Vast.ai.",
        "mode": "auto",
        "language": "fr",
        "num_step": 8,
        "speed": 1.0,
    }


worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url=MODEL_HEALTHCHECK_ENDPOINT,
    handlers=[
        HandlerConfig(
            route="/tts",
            request_parser=request_parser,
            allow_parallel_requests=False,
            max_queue_time=120.0,
            workload_calculator=lambda payload: 100.0,
            benchmark_config=BenchmarkConfig(
                generator=benchmark_generator,
                concurrency=1,
                runs=3,
            ),
        )
    ],
    log_action_config=LogActionConfig(
        on_load=MODEL_LOAD_LOG_MSG,
        on_error=MODEL_ERROR_LOG_MSGS,
        on_info=MODEL_INFO_LOG_MSGS,
    ),
)


if __name__ == "__main__":
    Worker(worker_config).run()
