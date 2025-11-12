# Avatar Assistant — Architecture (M1)
Components: CLI, transcription provider, summarizer, storage.
Data flow: audio -> transcribe -> summarize -> write outputs to data/runs/<ts>/
