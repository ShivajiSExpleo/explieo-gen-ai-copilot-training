"""
Enterprise Prompt Engineering Agent
====================================
Give it what you want → get back a production-ready enterprise prompt.

Usage:
    python enterprise_prompt_agent.py
"""

import os
import sys
import textwrap

# ── Optional: use OpenAI if API key is present ──────────────────────────────
try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

# ── ANSI colour helpers ──────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
RED    = "\033[91m"

def c(text, colour): return f"{colour}{text}{RESET}"
def hr(char="─", width=70): return char * width

# ── Master meta-prompt that turns a user request into enterprise prompts ─────
ENTERPRISE_SYSTEM_PROMPT = """\
You are an elite Prompt Engineering Architect with 10+ years of experience \
building enterprise AI systems for Fortune 500 companies.

Your job is to convert a user's raw requirement into a complete, \
production-ready prompt package that a developer can drop directly into a \
business application.

## OUTPUT STRUCTURE — always produce ALL 7 sections

### 1. SYSTEM PROMPT
A detailed system/persona prompt that sets role, expertise, tone, boundaries, \
and compliance constraints (e.g., GDPR, SOC-2 awareness).

### 2. USER PROMPT TEMPLATE
A parameterised template with clearly labelled placeholders in {{DOUBLE_BRACES}}. \
Include every variable a developer needs to fill in.

### 3. FEW-SHOT EXAMPLES (2–3)
Concrete input → output pairs that teach the model the expected behaviour, \
format, and quality level.

### 4. CHAIN-OF-THOUGHT INSTRUCTION
An explicit reasoning directive telling the model HOW to think through the \
problem step-by-step before producing its final answer.

### 5. OUTPUT FORMAT SPECIFICATION
Strict schema for the response: JSON / Markdown / table / plain text. \
Include field names, types, and validation rules where relevant.

### 6. GUARDRAILS & SAFETY CONSTRAINTS
Edge-case handling, refusal conditions, hallucination-prevention tactics, \
PII/sensitive-data rules, and graceful degradation instructions.

### 7. PRODUCTION INTEGRATION NOTES
Recommended model (GPT-4o / Claude 3.5 / Gemini Pro etc.), temperature, \
max_tokens, retry strategy, logging hooks, and caching advice.

## QUALITY BAR
- Be specific and actionable — no vague instructions.
- Use professional, domain-appropriate language.
- Anticipate edge cases a developer would face in production.
- Output must be immediately usable without further editing.
"""

ENTERPRISE_USER_TEMPLATE = """\
Convert the following requirement into a complete enterprise production-ready \
prompt package following the 7-section structure above.

REQUIREMENT:
{requirement}

ADDITIONAL CONTEXT (if any):
{context}

Deliver the full prompt package now.
"""

# ── Core logic ───────────────────────────────────────────────────────────────

def build_with_openai(requirement: str, context: str) -> str:
    """Generate the prompt package via OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    user_message = ENTERPRISE_USER_TEMPLATE.format(
        requirement=requirement,
        context=context or "None provided."
    )

    print(c("\n⏳  Generating via OpenAI GPT-4o …", GREY))
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=3000,
        messages=[
            {"role": "system", "content": ENTERPRISE_SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ]
    )
    return response.choices[0].message.content


def build_offline(requirement: str, context: str) -> str:
    """
    Offline mode: produces a richly pre-filled template the user can
    copy-paste and adapt.  No API key required.
    """
    domain = requirement[:60].strip()
    ctx_line = context if context else "No additional context provided."

    package = f"""
╔══════════════════════════════════════════════════════════════════════╗
║         ENTERPRISE PROMPT PACKAGE  [OFFLINE TEMPLATE MODE]          ║
╚══════════════════════════════════════════════════════════════════════╝

REQUIREMENT  : {requirement}
CONTEXT      : {ctx_line}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. SYSTEM PROMPT
────────────────
You are a highly experienced, senior-level AI assistant specialising in
{domain}.  You operate within enterprise-grade systems where accuracy,
compliance, and reliability are non-negotiable.

Core directives:
- Adhere strictly to the task scope; do not speculate beyond available data.
- Follow data-privacy standards (GDPR / CCPA / HIPAA as applicable).
- Refuse requests that involve PII disclosure, illegal activity, or
  content that violates company policy.
- When uncertain, state your confidence level and recommend human review.
- Maintain a professional, concise, and neutral tone at all times.

### 2. USER PROMPT TEMPLATE
──────────────────────────
You are helping a {{DEPARTMENT}} team at {{COMPANY_NAME}}.

Task:
{{TASK_DESCRIPTION}}

Input data:
{{INPUT_DATA}}

Constraints:
- Output language: {{LANGUAGE | default: "English"}}
- Maximum response length: {{MAX_LENGTH | default: "500 words"}}
- Audience expertise level: {{AUDIENCE_LEVEL | default: "intermediate"}}
- Format required: {{OUTPUT_FORMAT | default: "structured Markdown"}}

Produce the output now.

### 3. FEW-SHOT EXAMPLES
───────────────────────
EXAMPLE 1
  Input : [Provide a realistic sample input for {domain}]
  Output: [Provide the ideal, fully-formatted output]

EXAMPLE 2
  Input : [Provide a second realistic sample — edge case or harder variant]
  Output: [Ideal output demonstrating graceful handling]

EXAMPLE 3
  Input : [Provide a borderline / ambiguous input]
  Output: [Output showing the model flagging uncertainty and asking for
            clarification rather than guessing]

### 4. CHAIN-OF-THOUGHT INSTRUCTION
────────────────────────────────────
Before writing your final response, reason through the following steps
inside <thinking> tags (these will not appear in the final output):

  <thinking>
  Step 1 – Understand the request: restate what is being asked in one
            sentence.
  Step 2 – Identify constraints: list every explicit and implicit
            constraint from the prompt.
  Step 3 – Gather evidence: cite any relevant facts, data points, or
            policies that apply.
  Step 4 – Draft an approach: outline how you will structure the answer.
  Step 5 – Validate: check your draft against the constraints and
            guardrails.  If it violates any, revise.
  </thinking>

Only then write the final user-facing answer.

### 5. OUTPUT FORMAT SPECIFICATION
───────────────────────────────────
Return a JSON object with the following schema:

{{
  "status"     : "success" | "partial" | "error",
  "confidence" : 0.0–1.0,   // model's self-assessed confidence
  "result"     : {{
    "summary"  : "string",   // ≤ 2 sentence executive summary
    "details"  : "string",   // full Markdown body
    "sources"  : ["string"], // citations or "INTERNAL_KNOWLEDGE"
    "caveats"  : ["string"]  // known limitations / assumptions
  }},
  "metadata"   : {{
    "model"    : "string",
    "tokens_used": integer,
    "latency_ms" : integer
  }}
}}

Validation rules:
- `confidence` must be a float in [0, 1].
- If `status` is "error", `result.details` must explain the failure.
- All string fields must be non-null; use "" if empty.

### 6. GUARDRAILS & SAFETY CONSTRAINTS
───────────────────────────────────────
REFUSE and return {{"status":"error","result":{{"summary":"Request declined",
"details":"<reason>"}}}} if:
  • The request asks for PII, credentials, or proprietary data.
  • The output could cause physical, financial, or reputational harm.
  • The task is outside the defined domain scope.

HALLUCINATION PREVENTION:
  • Never invent statistics, citations, or named individuals.
  • If factual accuracy cannot be verified, add a caveat.
  • Prefer "I do not have enough information" over guessing.

DATA HANDLING:
  • Strip or mask any PII detected in the input before processing.
  • Log a compliance event if sensitive data is encountered.

GRACEFUL DEGRADATION:
  • On ambiguous input, ask one clarifying question instead of assuming.
  • On partial data, produce a partial result with confidence < 0.6.

### 7. PRODUCTION INTEGRATION NOTES
─────────────────────────────────────
Recommended model   : GPT-4o  (fallback: Claude 3.5 Sonnet)
Temperature         : 0.2  (deterministic; raise to 0.5 for creative tasks)
Max tokens          : 1 500 – 2 000
Top-p               : 0.9
Retry strategy      : Exponential back-off, 3 attempts, base delay 1 s
Timeout             : 30 s per request
Caching             : Cache identical requests for 15 min (Redis / CDN)
Logging hooks       : Log prompt hash, latency, token count, status code
Cost guard          : Alert if monthly spend exceeds configured threshold
Rate limiting       : 60 req/min per user; 1 000 req/min globally
Monitoring          : Track avg confidence score; alert if < 0.6 for > 5 %
                      of requests over a 1-hour window.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[OFFLINE MODE] — Set OPENAI_API_KEY to get a fully customised package.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return textwrap.dedent(package)


def save_output(content: str, requirement: str) -> str:
    """Save the generated prompt package to a file."""
    safe_name = "".join(
        c for c in requirement[:40] if c.isalnum() or c in (" ", "-", "_")
    ).strip().replace(" ", "_")
    filename = f"prompt_package_{safe_name}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Enterprise Prompt Package\n\n")
        f.write(f"**Requirement:** {requirement}\n\n---\n\n")
        f.write(content)
    return filename


# ── Interactive REPL ─────────────────────────────────────────────────────────

def run_agent():
    print()
    print(c(hr("═"), CYAN))
    print(c("  🏢  ENTERPRISE PROMPT ENGINEERING AGENT", BOLD + CYAN))
    print(c("  Give me what you want → I'll generate a production-ready prompt", GREY))
    print(c(hr("═"), CYAN))

    api_mode = _OPENAI_AVAILABLE and bool(os.getenv("OPENAI_API_KEY"))
    mode_label = (
        c("  ✅  OpenAI GPT-4o mode active", GREEN)
        if api_mode
        else c("  ⚡  Offline template mode  (set OPENAI_API_KEY for AI generation)", YELLOW)
    )
    print(mode_label)
    print(c("  Type 'quit' or 'exit' to stop | 'save' after generation to export\n", GREY))

    while True:
        print(c(hr(), CYAN))
        requirement = input(c("📝  What do you want the prompt to do?\n    > ", BOLD)).strip()

        if requirement.lower() in ("quit", "exit", "q"):
            print(c("\n👋  Goodbye!\n", CYAN))
            break

        if not requirement:
            print(c("    ⚠️  Please enter a requirement.", YELLOW))
            continue

        context = input(c("\n🔍  Any additional context / constraints? (press Enter to skip)\n    > ", GREY)).strip()

        # ── Generate ──
        try:
            if api_mode:
                result = build_with_openai(requirement, context)
            else:
                result = build_offline(requirement, context)
        except Exception as e:
            print(c(f"\n❌  Error: {e}", RED))
            continue

        # ── Display ──
        print()
        print(c(hr("─"), GREEN))
        print(c("  ✨  ENTERPRISE PROMPT PACKAGE", BOLD + GREEN))
        print(c(hr("─"), GREEN))
        print(result)
        print(c(hr("─"), GREEN))

        # ── Save? ──
        save_choice = input(c("\n💾  Save to file? [y/N]: ", GREY)).strip().lower()
        if save_choice == "y":
            fname = save_output(result, requirement)
            print(c(f"    ✅  Saved → {fname}", GREEN))

        print()


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_agent()
