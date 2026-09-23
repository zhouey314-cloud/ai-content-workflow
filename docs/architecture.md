# Architecture

The core is a small pure function. The input contains source documents and claims linked by IDs. Output includes the persona, intent, channel, draft, citation IDs, checks and state. Unsourced or unsupported claims fail before review; only a named human can approve. The built-in channel adaptation is intentionally basic. It is a tested workflow skeleton, not an AI writing quality benchmark.
