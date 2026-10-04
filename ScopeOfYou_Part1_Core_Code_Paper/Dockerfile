FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e . --no-build-isolation
COPY . .
EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/health', timeout=2)" || exit 1
CMD ["personal-agi-serve", "--checkpoint", "checkpoints/sft_behavior_v31.pt", "--host", "0.0.0.0", "--port", "8765"]
