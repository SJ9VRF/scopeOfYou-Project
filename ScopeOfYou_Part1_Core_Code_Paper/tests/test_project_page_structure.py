from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"

REQUIRED_SECTIONS = [
    "problem", "idea", "architecture", "contribution", "experiments", "results",
    "failures", "demo", "scaling", "safety", "deep", "artifacts", "citation",
]
REQUIRED_COPY = [
    "Scope of You", "Aura Yavary", "Paper", "Code", "Demo", "Benchmark", "Video",
    "Why this problem matters", "Core idea", "My contribution", "Experiments", "Results",
    "Failure analysis", "Interactive demo", "Scaling", "Safety / limitations",
    "Technical deep dive", "Artifacts", "Citation", "APPLY", "SUPPRESS", "MUST-NOT-AFFECT",
    "ContractBench-Implicit", "+10.46 pp", "20 / 20", "Data / tasks", "Baselines",
    "Ablations", "Setup", "Success rate / reliability", "Recovery", "Latency", "Cost",
    "Model size", "Task horizon", "Tool count", "Cost / latency", "Robustness",
    "Irreversible actions", "Human escalation", "Experiment ledger", "year = {2026}",
    "not an LLM capability result", "7–8B", "human validation",
]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if "id" in d: self.ids.add(d["id"])
        if tag == "a" and "href" in d: self.hrefs.append(d["href"])

def test_project_page_structure_and_claim_hygiene():
    text = PAGE.read_text(encoding="utf-8")
    for token in REQUIRED_COPY:
        assert token.lower() in text.lower(), token
    parser=Parser(); parser.feed(text)
    assert set(REQUIRED_SECTIONS).issubset(parser.ids)
    prohibited = ["we achieve sota", "state-of-the-art performance", "sota result"]
    for phrase in prohibited:
        assert phrase not in text.lower(), phrase
    assert "no frontier-model SOTA" in text
    assert "not an LLM capability result" in text

def test_project_page_internal_links_resolve():
    parser=Parser(); parser.feed(PAGE.read_text(encoding="utf-8"))
    for href in parser.hrefs:
        if href.startswith(("#","http://","https://","mailto:","javascript:")):
            continue
        assert (PAGE.parent / href).resolve().exists(), href
