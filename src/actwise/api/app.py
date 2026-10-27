"""The API wired to the real pipelines: `make serve`, or uvicorn actwise.api.app:app.

Reads .env: the LLM providers (serving profile: fast failover), ACTWISE_API_KEY and
MAX_DAILY_REQUESTS. Only the local profile exists so far: the cloud one needs the
ONNX embedder of step 9 and the Qdrant index of step 13.
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

from actwise.agent.classifier import ai_act_articles, classify
from actwise.api.main import DAILY_CAP, create_app
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import RagPipeline
from actwise.llm.factory import SERVING, build_llm
from actwise.retrieval.passages import paragraph_passages
from actwise.retrieval.systems import SERVED, SYSTEMS

ANSWER_PROMPT = "answer.v2"  # the best prompt of step 6 (docs/generation.md)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
logging.getLogger("actwise").setLevel(logging.INFO)
load_dotenv()  # .env fills in what the environment doesn't set
if (profile := os.environ.get("PROFILE") or "local") != "local":
    raise RuntimeError(f"PROFILE={profile} is not wired yet: use local (cloud: steps 9 and 13)")

llm = build_llm(os.environ, SERVING)
retriever = SYSTEMS[SERVED].build()
retriever.search("warm-up", 1)  # load the embedder now, not during the first request
pipeline = RagPipeline(llm, retriever.search, load_prompt(ANSWER_PROMPT))
articles = ai_act_articles(paragraph_passages())

app = create_app(
    ask=pipeline.ask,
    classify=lambda description, deadline: classify(
        llm, retriever.search, articles, description, deadline=deadline
    ),
    search=retriever.search,
    api_key=os.environ.get("ACTWISE_API_KEY") or None,
    daily_cap=int(os.environ.get("MAX_DAILY_REQUESTS") or DAILY_CAP),
)
