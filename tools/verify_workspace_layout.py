"""Check application relocation without making model requests."""

import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    require((ROOT / "frontend/src/App.vue").is_file(), "Frontend entry missing")
    require((ROOT / "backend/main.py").is_file(), "Backend entry missing")
    require((ROOT / "backend/static/index.html").is_file(), "Static page missing")
    require(not (ROOT / "week3/frontend/package.json").exists(), "Old frontend entry remains")
    require(not (ROOT / "week2/api/main.py").exists(), "Old backend entry remains")

    sys.path.insert(0, str(ROOT))
    previous_directory = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="ai-workstation-layout-") as temporary:
        try:
            os.chdir(temporary)
            from backend import main as service
            from backend import prompts
            from fastapi.testclient import TestClient

            require(service.ENV_FILE == ROOT / ".env", "Backend configuration path changed")
            require(prompts.ROOT_DIR == ROOT, "Prompt project root changed")
            require(prompts.SAMPLE == ROOT / "week2/attention_extracted.txt", "Sample path changed")
            require(prompts.SAMPLE.is_file(), "Prompt sample missing")
            require(prompts.OUTPUT_DIR == ROOT / "week4", "Prompt output path changed")
            require(prompts.OUTPUT_DIR.is_dir(), "Prompt output directory missing")

            with TestClient(service.app) as client:
                health = client.get("/health")
                require(health.status_code == 200, "Health endpoint failed")
                require(health.json().get("status") == "ok", "Health response changed")
                static = client.get("/")
                require(static.status_code == 200, "Static page endpoint failed")
                require(
                    static.content == (ROOT / "backend/static/index.html").read_bytes(),
                    "Static endpoint serves different content",
                )
                missing = client.post("/summarize")
                require(missing.status_code == 422, "Missing-file validation changed")
                invalid = client.post(
                    "/summarize", files={"file": ("probe.txt", b"not a PDF", "text/plain")}
                )
                require(invalid.status_code == 400, "Invalid-file validation changed")
                require(
                    invalid.json().get("detail") == "上传的文件不是 PDF",
                    "Invalid-file response changed",
                )
            print("PASS: application entries and retired paths")
            print("PASS: root configuration and Prompt paths from an unrelated working directory")
            print("PASS: health, static page, missing-file and invalid-file routes")
            print("No model requests were made.")
        finally:
            os.chdir(previous_directory)


if __name__ == "__main__":
    main()
