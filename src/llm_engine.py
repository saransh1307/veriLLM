import logging
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger("SecureLogger")

class PIIAnonymizer:
    def __init__(self, model_name="llama3", base_url="http://ollama:11434"):
        # We point to our internal isolated Ollama container
        self.llm = Ollama(model=model_name, base_url=base_url, temperature=0.1)
        
        # We need a strict prompt to ensure AI focuses ONLY on redaction and avoids talking to the user.
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""You are a strict Data Privacy Compliance Officer. Your ONLY job is to find Personally Identifiable Information (PII) in the following text and replace it with highly realistic synthetic data.

Rules:
1. Identify all Names, Email Addresses, Phone Numbers, SSNs, and Physical Addresses.
2. Replace each identified entity with a UNIQUE, completely randomized fake equivalent. Do NOT use generic names like "John Doe" or obvious fakes like "000-00-0000". Invent a distinct sounding realistic name (e.g., "Marcus Vance" or "Elena Rostova"), a distinct 9-digit SSN, and a distinct email for every single person you find.
3. Preserve the exact meaning and structure of the original text.
4. Output ONLY the raw mutated text. Do NOT include phrases like "Here is the anonymized text:" or "Note: I replaced...". Your first word must be the first word of the anonymized sentence. Your last word must be the last word. Do not explain your changes.

Original Text:
{text}

Anonymized Text:"""
        )

    def anonymize_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return text
            
        try:
            chain = self.prompt | self.llm
            result = chain.invoke({"text": text})
            return result.strip()
        except Exception as e:
            # [CYBERSEC] Error Handling without PII Leakage
            # We explicitly do not log the text that caused the crash.
            logger.error("Error during LLM anonymization. Fallback triggered to prevent leakage.")
            return "[REDACTED_DUE_TO_PROCESSING_ERROR]"
