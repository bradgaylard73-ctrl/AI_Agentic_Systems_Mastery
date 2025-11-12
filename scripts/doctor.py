import shutil, sys, os
ok = True
for tool in ("python","ffmpeg"):
    if not shutil.which(tool):
        print("missing:", tool)
        ok = False
print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
sys.exit(0 if ok else 1)
