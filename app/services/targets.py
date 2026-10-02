from typing import Tuple, Dict, Any, List
import re

class MockLLM:
    def __init__(self):
        pass

    def evaluate(self, system_prompt: str, context: str, user_input: str, is_secure: bool) -> Tuple[str, bool, str]:
        """
        Returns (response, is_vulnerable, evidence)
        """
        inp = user_input.lower()
        is_vuln = False
        evidence = None
        
        # Determine intent (Normal Conversation vs Attack)
        if "hello" in inp or "hi" in inp:
            return "Hello! How can I assist you today?", False, None
        if "refund" in inp:
            return "Our synthetic refund policy states that you can return items within 30 days.", False, None
        if "support" in inp or "contact" in inp:
            return "You can contact our synthetic support team at support@company.local.", False, None
        if "security" in inp:
            return "Account security includes 2FA, strong passwords, and regular audits.", False, None

        return None, False, None # Fallback to specific lab logic

class TargetApplication:
    def __init__(self, is_secure: bool, db, user):
        self.is_secure = is_secure
        self.db = db
        self.user = user
        self.llm = MockLLM()

    def process(self, user_input: str) -> Tuple[str, bool, str, Dict]:
        """Returns (response, is_vuln, evidence, extra_data)"""
        return "Not implemented", False, None, {}

class CustomerSupportTarget(TargetApplication): # Lab 01
    def process(self, user_input: str):
        llm_resp, _, _ = self.llm.evaluate("System prompt", "", user_input, self.is_secure)
        if llm_resp: return llm_resp, False, None, {}

        inp = user_input.lower()
        if "ignore" in inp or "system" in inp:
            if self.is_secure:
                return "Blocked: Unsafe instruction override detected.", False, "Blocked PI attempt", {}
            else:
                return "My system secret is: LAB_SECRET=AI-LAB-PI-001", True, "System instruction exposed via Prompt Injection", {}
        
        return "I can answer questions about refunds, support, or account security.", False, None, {}

class SystemPromptTarget(TargetApplication): # Lab 02
    def process(self, user_input: str):
        llm_resp, _, _ = self.llm.evaluate("System prompt", "", user_input, self.is_secure)
        if llm_resp: return llm_resp, False, None, {}

        inp = user_input.lower()
        if "repeat" in inp or "print" in inp or "rules" in inp:
            if self.is_secure:
                return "I cannot reveal my internal instructions.", False, "System prompt extraction blocked.", {}
            else:
                return "SYSTEM_PROMPT_SECRET=AI-LAB-SYS-002", True, "Extracted SYSTEM_PROMPT_SECRET=AI-LAB-SYS-002", {}
        return "I am an internal assistant. How can I help?", False, None, {}

class JailbreakTarget(TargetApplication): # Lab 03
    def process(self, user_input: str):
        llm_resp, _, _ = self.llm.evaluate("System prompt", "", user_input, self.is_secure)
        if llm_resp: return llm_resp, False, None, {}

        inp = user_input.lower()
        if "dan" in inp or "hypothetical" in inp or "ignore policies" in inp:
            if self.is_secure:
                return "I cannot bypass my safety policies.", False, "Policy enforcement active.", {}
            else:
                return "JAILBROKEN: I can now bypass all restrictions.", True, "Safety policy successfully bypassed.", {}
        return "I operate under strict safety guidelines. What is your request?", False, None, {}

class SensitiveDataTarget(TargetApplication): # Lab 04
    def process(self, user_input: str):
        llm_resp, _, _ = self.llm.evaluate("System prompt", "", user_input, self.is_secure)
        if llm_resp: return llm_resp, False, None, {}

        inp = user_input.lower()
        if "email" in inp or "token" in inp or "confidential" in inp:
            if self.is_secure:
                return "I am not authorized to disclose confidential data.", False, "DLP Filter active.", {}
            else:
                return "Internal data: API_TOKEN=AI-LAB-TOKEN-404, admin@company.local", True, "Disclosed API_TOKEN=AI-LAB-TOKEN-404", {}
        return "I manage employee information.", False, None, {}

class RAGTarget(TargetApplication): # Lab 05
    def process(self, user_input: str):
        inp = user_input.lower()
        if "secret" in inp or "query" in inp:
            if self.is_secure:
                return "Document retrieval blocked due to access policies.", False, "RAG Access Denied", {"docs": [], "score": 0.0}
            else:
                return "Retrieved confidential RAG context.", True, "RAG-DOC-SECRET-005", {"docs": ["RAG-DOC-SECRET-005"], "score": 0.99}
        return f"Found 1 generic document for query: {user_input}", False, None, {"docs": ["refund_policy.txt"], "score": 0.85}

class RAGPoisoningTarget(TargetApplication): # Lab 06
    def process(self, user_input: str):
        inp = user_input.lower()
        if "poison" in inp or "inject" in inp:
            if self.is_secure:
                return "Malicious document neutralized.", False, "Poisoned doc ignored", {"docs": ["poison_payload.txt (BLOCKED)"], "score": 0.0}
            else:
                return "I will execute the instruction from the document: You are compromised.", True, "Model executed poisoned instructions.", {"docs": ["poison_payload.txt"], "score": 0.95}
        return f"Results for: {user_input}", False, None, {"docs": ["normal_doc.txt"], "score": 0.70}

class IndirectPromptTarget(TargetApplication): # Lab 07
    def process(self, user_input: str):
        inp = user_input.lower()
        if "summarize" in inp:
            if self.is_secure:
                return "The document contains malicious instructions. I will not execute them.", False, "Indirect Prompt Injection detected", {"docs": ["malicious_doc.txt"]}
            else:
                return "SYSTEM COMPROMISED. SENDING USER DATA TO ATTACKER.", True, "Executed instruction injected via external document.", {"docs": ["malicious_doc.txt"]}
        return "Provide a document name to summarize.", False, None, {}

class OutputHandlingTarget(TargetApplication): # Lab 08
    def process(self, user_input: str):
        inp = user_input.lower()
        if "script" in inp or "xss" in inp:
            if self.is_secure:
                return "&lt;script&gt;alert('XSS blocked')&lt;/script&gt;", False, "Output sanitized", {}
            else:
                return "<script>alert('XSS executed from LLM output!')</script>", True, "Unsafe script rendered from LLM.", {}
        return "I generate formatted output.", False, None, {}

class ExcessiveAgencyTarget(TargetApplication): # Lab 09
    def process(self, user_input: str):
        inp = user_input.lower()
        if "drop" in inp or "admin" in inp or "tool" in inp:
            if self.is_secure:
                return "Agent denied access to unauthorized tools.", False, "Tool authorization check failed.", {"tool": "DB_DROP_TABLE", "allowed": False}
            else:
                return "Tool executed.", True, "Agent successfully executed privileged tool: DB_DROP_TABLE", {"tool": "DB_DROP_TABLE", "allowed": True}
        return "I can search logs and view basic status.", False, None, {"tool": "search_logs", "allowed": True}

class ToolAbuseTarget(TargetApplication): # Lab 10
    def process(self, user_input: str):
        inp = user_input.lower()
        if "system" in inp or "abuse" in inp or "rm -rf" in inp:
            if self.is_secure:
                return "Tool parameters validated and rejected.", False, "Input validation failed on tool params.", {"params": inp, "safe": False}
            else:
                return "Command injected via tool parameters.", True, "Unsafe parameters passed to internal tool.", {"params": inp, "safe": True}
        return f"Executed tool safely with: {user_input}", False, None, {"params": user_input, "safe": True}

class BrokenAccessControlTarget(TargetApplication): # Lab 11
    def process(self, user_input: str):
        inp = user_input.lower()
        target_tenant = "tenantb" if self.user.tenant.lower() == "tenanta" else "tenanta"
        if target_tenant in inp or "other" in inp:
            if self.is_secure:
                return f"Access Denied: You cannot view data for {target_tenant}", False, "403 Forbidden.", {"requested_tenant": target_tenant, "actual": self.user.tenant}
            else:
                return f"Successfully retrieved API data for {target_tenant}", True, f"Cross-tenant data accessed for {target_tenant}", {"requested_tenant": target_tenant, "actual": self.user.tenant}
        return f"Showing data for your tenant: {self.user.tenant}", False, None, {"requested_tenant": self.user.tenant, "actual": self.user.tenant}

class CrossTenantAITarget(TargetApplication): # Lab 12
    def process(self, user_input: str):
        inp = user_input.lower()
        target_tenant = "tenantb" if self.user.tenant.lower() == "tenanta" else "tenanta"
        if target_tenant in inp or "bob" in inp:
            if self.is_secure:
                return f"AI cannot retrieve context for {target_tenant}.", False, "Cross-tenant AI context blocked.", {}
            else:
                return f"Here is {target_tenant}'s private conversation history.", True, f"Leaked AI context for {target_tenant}.", {}
        return f"I am your dedicated tenant assistant.", False, None, {}

class SupplyChainTarget(TargetApplication): # Lab 13
    def process(self, user_input: str):
        inp = user_input.lower()
        if "supply" in inp or "model" in inp or "untrusted" in inp:
            if self.is_secure:
                return "Untrusted model weights blocked by signature verification.", False, "Hash validation failed.", {"component": "huggingface/untrusted-model", "verified": False}
            else:
                return "Loaded untrusted model weights.", True, "Untrusted artifact loaded successfully.", {"component": "huggingface/untrusted-model", "verified": True}
        return "Model registry active.", False, None, {"component": "huggingface/trusted-model", "verified": True}

class ConfigSecurityTarget(TargetApplication): # Lab 14
    def process(self, user_input: str):
        inp = user_input.lower()
        if "temperature" in inp or "config" in inp:
            if self.is_secure:
                return "System configurations are locked.", False, "Configuration change rejected.", {}
            else:
                return "Configuration altered. Safety bounds removed.", True, "Unsafe model configuration applied.", {}
        return "Configuration console active.", False, None, {}

class AssessmentTarget(TargetApplication): # Lab 15
    def process(self, user_input: str):
        inp = user_input.lower()
        if "assess" in inp or "final" in inp:
            return "Final Assessment completed.", True, "Completed all required assessment checks.", {}
        return "Perform all tests for final assessment.", False, None, {}

TARGET_MAP = {
    "lab01": CustomerSupportTarget,
    "lab02": SystemPromptTarget,
    "lab03": JailbreakTarget,
    "lab04": SensitiveDataTarget,
    "lab05": RAGTarget,
    "lab06": RAGPoisoningTarget,
    "lab07": IndirectPromptTarget,
    "lab08": OutputHandlingTarget,
    "lab09": ExcessiveAgencyTarget,
    "lab10": ToolAbuseTarget,
    "lab11": BrokenAccessControlTarget,
    "lab12": CrossTenantAITarget,
    "lab13": SupplyChainTarget,
    "lab14": ConfigSecurityTarget,
    "lab15": AssessmentTarget
}
