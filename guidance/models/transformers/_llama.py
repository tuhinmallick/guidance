from ._transformers import Transformers, TransformersChat

class Llama(Transformers):
    pass

class LlamaChat(TransformersChat, Llama):

    def system(self):
        """Patch up the system command to convert normal system role structure into Llama structure (nested in the first user message)."""
        self._system_prefex = "[INST] " if not str(self) else ""
        out = super().system()
        delattr(self, "_system_prefex")
        return out
    
    def get_role_start(self, role_name, **kwargs):
        if role_name == "system":
            return self._system_prefex + "<<SYS>>\n"
        elif role_name == "user":
            return "" if str(self).endswith("\n<</SYS>>\n\n") else "[INST] "
        else:
            return " "
    
    def get_role_end(self, role_name=None):
        if role_name == "system":
            return "\n<</SYS>>\n\n"
        elif role_name == "user":
            return " [/INST]"
        else:
            return " "