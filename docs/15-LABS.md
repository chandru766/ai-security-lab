# 15 AI Security Labs

*Documenting the 15 labs currently implemented in the database.*

## Lab 01 — Direct Prompt Injection
**Objective**: Force the LLM to ignore instructions and print a secret.
**Vulnerable Behavior**: The LLM blindly concatenates user input with system prompts.
**Secure Behavior**: The LLM sanitizes input or strictly separates user context from system context.

## Lab 02 — System Prompt Extraction
**Objective**: Extract the hidden system prompt guidelines.
**Vulnerable Behavior**: The LLM regurgitates its initial programming when requested.

## Lab 03 — Jailbreak Testing
**Objective**: Bypass safety filters to generate disallowed content.
**Vulnerable Behavior**: The LLM fails to recognize adversarial framing (e.g., "DAN" mode).

## Lab 04 — Sensitive Information Disclosure
**Objective**: Trick the LLM into revealing PII or API keys embedded in its context.
**Vulnerable Behavior**: The LLM lacks output filtering for sensitive tokens.

## Lab 05 — RAG Security
**Objective**: Access documents outside the intended scope of the user.
**Vulnerable Behavior**: The retriever uses unsanitized input to fetch cross-tenant data.

## Lab 06 — RAG Poisoning
**Objective**: Inject a document into the knowledge base that manipulates future answers.
**Vulnerable Behavior**: The system ingests untrusted text without validation.

## Lab 07 — Indirect Prompt Injection
**Objective**: Embed an injection payload on a webpage that the LLM reads.
**Vulnerable Behavior**: The LLM executes instructions found in retrieved web text.

## Lab 08 — Insecure Output Handling
**Objective**: Achieve XSS by making the LLM generate unescaped HTML/JS.
**Vulnerable Behavior**: The frontend renders LLM output as raw HTML.

## Lab 09 — Excessive Agency
**Objective**: Make an AI agent execute a destructive action (e.g., drop database).
**Vulnerable Behavior**: The agent has overly broad permissions without human-in-the-loop.

## Lab 10 — AI Agent Tool Abuse
**Objective**: Exploit a vulnerability in a tool the AI uses (e.g., SSRF via a fetch tool).
**Vulnerable Behavior**: The agent blindly passes user-controlled parameters to backend APIs.

## Lab 11 — Broken Access Control
**Objective**: Exploit flawed RBAC in the LLM's authorization layer.
**Vulnerable Behavior**: The LLM serves responses based on user claims rather than backend validation.

## Lab 12 — Cross-Tenant AI Data Access
**Objective**: View data belonging to another tenant in a multi-tenant LLM deployment.
**Vulnerable Behavior**: Vector search lacks tenant isolation.

## Lab 13 — AI Supply Chain Security
**Objective**: Identify a vulnerability in an imported third-party AI library/model.
**Vulnerable Behavior**: The application uses a known-vulnerable dependency.

## Lab 14 — Model/Prompt Configuration Security
**Objective**: Abuse insecure generation parameters (e.g., high temperature leading to leakage).
**Vulnerable Behavior**: The model configuration is optimized for creativity over security.

## Lab 15 — AI Security Assessment
**Objective**: Comprehensive capstone combining multiple vulnerabilities.
**Vulnerable Behavior**: The system exhibits chained vulnerabilities.\n