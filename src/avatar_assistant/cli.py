import os, sys
def main():
    print("avatar-assistant 0.1.0")
    print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
    sys.exit(0)
if __name__ == "__main__":
    main()
