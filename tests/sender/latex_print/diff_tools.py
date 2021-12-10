# Standard Library
import subprocess
import sys
from pathlib import Path
from subprocess import PIPE


def view_pdf(filepath: Path):
    if sys.platform == "linux":
        subprocess.run(["okular", filepath])


def pdf_diff(pdf: Path, compare_to_file: Path = None):
    if compare_to_file:
        pdf_expected = compare_to_file
    else:
        pdf_expected = pdf.with_name(f"{pdf.stem}_expectation.pdf")

    for filepath in [pdf, pdf_expected]:
        if not filepath.exists():
            raise FileNotFoundError(str(filepath))

    cp = subprocess.run(
        ["pdf-diff", pdf, pdf_expected],
        stdout=PIPE,
        stderr=PIPE,
    )

    FAILURE_CODE = -1
    if cp.stderr.find(bytes("Exception: There are no text differences.", "utf8")) != FAILURE_CODE:
        assert True
    else:
        output_file = Path(f"{pdf.stem} vs {pdf_expected.stem}.png")
        output_file.write_bytes(cp.stdout)
        view_pdf(output_file)
