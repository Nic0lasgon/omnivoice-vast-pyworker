# OmniVoice Vast.ai PyWorker

Dedicated `worker.py` repository for OmniVoice serverless routing on Vast.ai.

## Purpose

This repository is used via `PYWORKER_REPO` in Vast.ai serverless templates.

It defines the PyWorker route configuration (`/tts`) that forwards requests to a local model server running on:

- URL: `http://127.0.0.1`
- Port: `18000`

## Files

- `worker.py`: PyWorker configuration (`WorkerConfig`, `HandlerConfig`, `LogActionConfig`, `BenchmarkConfig`)
- `requirements.txt`: worker dependencies installed at worker startup

## Expected model server contract

The local model server should expose:

- `POST /tts`
- `GET /health`

And log to:

- `/var/log/omnivoice/server.log`

## Recommended template env

- `PYWORKER_REPO=https://github.com/Nic0lasgon/omnivoice-vast-pyworker`

## Current Vast notes

The worker image has been validated with the current OmniVoice flow and the current deployment uses a small writable disk footprint on Vast.

For the current setup, the workergroup has been updated with:

- `launch_args=--disk 15`

That value is enough for the current image and runtime state.

## Recommended workergroup search filters

Use datacenter-only, one-GPU workers, with your validated GPU targets:

- `gpu_name in [RTX_A4000, RTX_4060_Ti, RTX_3060]`
- `num_gpus=1`
- `datacenter=True`
- `verified=True`
- `rentable=True`
- `rented=False`
