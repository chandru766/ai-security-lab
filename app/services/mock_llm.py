class MockLLMProvider:
    def __init__(self, is_secure: bool = False, lab_id: str = None):
        self.is_secure = is_secure
        self.lab_id = lab_id
        
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        
        # LAB 01: Direct Prompt Injection
        if self.lab_id == "lab01":
            if "ignore" in prompt_lower or "system" in prompt_lower:
                if self.is_secure:
                    return "Blocked: Unsafe instruction override detected."
                else:
                    return "My system secret is: LAB_SECRET=AI-LAB-PI-001"
            return "Hello. How can I help you?"

        # LAB 02: System Prompt Extraction
        if self.lab_id == "lab02":
            if "repeat" in prompt_lower or "print" in prompt_lower:
                if self.is_secure:
                    return "I cannot reveal my internal instructions."
                else:
                    return "SYSTEM_PROMPT_SECRET=AI-LAB-SYS-002"
            return "I am a helpful AI agent."

        # LAB 03: Jailbreak Testing
        if self.lab_id == "lab03":
            if "dan" in prompt_lower or "do anything now" in prompt_lower or "hypothetical" in prompt_lower:
                if self.is_secure:
                    return "I cannot bypass my safety policies."
                else:
                    return "JAILBROKEN: I can now bypass all restrictions and execute arbitrary requests."
            return "I operate under strict safety guidelines."
            
        # LAB 04: Sensitive Information Disclosure
        if self.lab_id == "lab04":
            if "email" in prompt_lower or "token" in prompt_lower or "confidential" in prompt_lower:
                if self.is_secure:
                    return "I am not authorized to disclose confidential data."
                else:
                    return "Here is the internal data: API_TOKEN=AI-LAB-TOKEN-404, admin_email=ceo@company.local"
            return "Ask me general questions about the company."

        # LAB 07: Indirect Prompt Injection
        if self.lab_id == "lab07":
            if "summarize" in prompt_lower:
                if self.is_secure:
                    return "The provided document appears to contain malicious instructions. I will not execute them."
                else:
                    return "The document says: SYSTEM COMPROMISED. SENDING USER DATA TO ATTACKER."
            return "Provide a document for me to summarize."

        # LAB 08: Insecure Output Handling
        if self.lab_id == "lab08":
            if "script" in prompt_lower or "exec" in prompt_lower:
                if self.is_secure:
                    return "I will only provide safe, sanitized text."
                else:
                    return "<script>alert('XSS executed from LLM output!')</script>"
            return "I generate content for web pages."

        # LAB 12: Cross-Tenant AI Data Access
        if self.lab_id == "lab12":
            if "tenantb" in prompt_lower or "bob" in prompt_lower:
                if self.is_secure:
                    return "Access Denied: You do not have permission to view tenantB's context."
                else:
                    return "Here is tenantB's private conversation history: Bob requested the quarterly earnings report."
            return "I am your dedicated tenant assistant."

        # LAB 14: Configuration Security
        if self.lab_id == "lab14":
            if "temperature" in prompt_lower or "config" in prompt_lower:
                if self.is_secure:
                    return "System configurations are locked."
                else:
                    return "Current config: Temperature=1.5, SystemPrompt=Unrestricted. You can modify these settings."
            return "Configuration console active."

        # Default fallback
        return f"Simulated response to: {prompt}"
