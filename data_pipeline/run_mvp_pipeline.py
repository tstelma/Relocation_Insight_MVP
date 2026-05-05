import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def run_command(command: list[str], description: str) -> None:
    """Run a command and print status."""
    print(f"{description}...")
    try:
        result = subprocess.run(
            command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        # Print the last few lines of output for confirmation
        output_lines = result.stdout.strip().split('\n')
        if output_lines and output_lines[-1]:
            print(f"✓ {output_lines[-1]}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def main():
    """Run the complete MVP pipeline."""
    print("Starting MVP pipeline...\n")

    # Step 1: Run HICP pipeline
    run_command(
        [sys.executable, "data_pipeline/run_hicp_pipeline.py"],
        "Running HICP pipeline"
    )

    # Step 2: Run housing burden pipeline
    run_command(
        [sys.executable, "data_pipeline/run_indicator_export.py", "housing_overburden"],
        "Running housing burden pipeline"
    )

    # Step 3: Run poverty risk pipeline
    run_command(
        [sys.executable, "data_pipeline/run_indicator_export.py", "poverty_risk"],
        "Running poverty risk pipeline"
    )

    # Step 4: Run income capacity pipeline
    run_command(
        [sys.executable, "data_pipeline/run_indicator_export.py", "income_capacity"],
        "Running income capacity pipeline"
    )

    # Step 5: Run net earnings capacity pipeline
    run_command(
        [sys.executable, "data_pipeline/run_indicator_export.py", "net_earnings_capacity"],
        "Running net earnings capacity pipeline"
    )

    # Step 6: Export standardized historical time-series
    run_command(
        [sys.executable, "data_pipeline/transform/export_timeseries.py"],
        "Exporting standardized MVP time-series"
    )

    # Step 7: Combine MVP insights
    run_command(
        [sys.executable, "data_pipeline/insights/combine_insights.py"],
        "Combining MVP insights"
    )

    print("\n✓ MVP pipeline complete.")


if __name__ == "__main__":
    main()
