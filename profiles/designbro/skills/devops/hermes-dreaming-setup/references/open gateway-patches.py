# Provider patches for OpenGateway compatibility
# Apply these to providers.py after each plugin install/update

## 1. chat.completions instead of responses.create + gzip fix
OLD:
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        prompt = self._build_prompt(sources, context)
        response = client.responses.create(model=self.model, input=prompt, temperature=0)
        text = getattr(response, "output_text", "").strip()

NEW:
        import httpx as _httpx
        client = OpenAI(api_key=self.api_key, base_url=self.base_url, http_client=_httpx.Client(headers={"Accept-Encoding": "identity"}))
        prompt = self._build_prompt(sources, context)
        response = client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": prompt}], temperature=0, max_tokens=16384)
        msg = response.choices[0].message if response.choices else None
        text = (msg.content or "").strip()
        if not text and msg and hasattr(msg, 'reasoning') and msg.reasoning:
            text = msg.reasoning.strip()

## 2. Line numbers in source block (helps model generate correct provenance)
OLD:
        source_block = "\n\n".join(f"### {source.path}\n{source.content}" for source in sources)

NEW:
        def _numbered(content, path):
            lines = content.splitlines()
            numbered = [f"{i+1}: {line}" for i, line in enumerate(lines)]
            return '\n'.join(numbered)
        source_block = "\n\n".join(f"### {source.path}\n{_numbered(source.content, source.path)}" for source in sources)

## 3. Prompt constraints (add before "Set approved to false" line)
- "IMPORTANT: target_path must be RELATIVE to live_root (e.g. user.md, memory.md). NEVER absolute paths.\n"
- "CRITICAL: Generate at most ONE proposal per target_path. Combine changes.\n"
- "STRICT SIZE LIMITS: memory max 240 chars/4 lines, user max 220 chars/4 lines, fact max 320 chars/12 lines. Each entry must start with -. Max 3 proposals total.\n"
- "Policy_flags must be non-empty list like ['auto-generated'].\n"
