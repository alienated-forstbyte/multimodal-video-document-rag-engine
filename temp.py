import subprocess

scripts = [
    "frames-generator.py",
    "audio_transcribe.py",
    "index.py",
]

for script in scripts:
    print(f"\nRunning {script}...")

    result = subprocess.run(
        ["python", script],
        check=True
    )

    print(f"{script} completed successfully.")

print("\nPipeline completed!")