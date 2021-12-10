# Standard Library
import logging
import tempfile
from pathlib import Path

# Third-Party
import pytest

# First-Party
from diff_tools import pdf_diff, view_pdf
from sender import pdflatex

# PROG_LOCATION = os.path.dirname(__file__)
PROG_LOCATION = Path(__file__).parent.absolute()
# TEMPLATE_LOCATION = os.path.dirname(pdflatex.__file__)
TEMPLATE_LOCATION = Path(pdflatex.__file__).parent.absolute()
LOGGER = logging.getLogger(__name__)
LOGGER


@pytest.mark.incremental
class TestTools:
    def test_pdf_diff_file_not_exist(self):
        pdf = PROG_LOCATION.joinpath("test_expectation.pdf")
        with pytest.raises(FileNotFoundError):
            pdf_diff(pdf)

    def test_pdf_diff_no_diff(self):
        pdf = PROG_LOCATION.joinpath("test_simple_expectation.pdf")
        pdf_diff(pdf, pdf)

    def test_pdf_diff_big_diff(self):
        pdf = PROG_LOCATION.joinpath("test_simple_expectation.pdf")
        pdf2 = PROG_LOCATION.joinpath("test_normal_expectation.pdf")
        pdf_diff(pdf, pdf2)


@pytest.mark.incremental
class TestPdflatexModule:
    def test_pdflatex_installed(self):
        """Check whether pdflatex tool is on PATH and marked as executable."""
        assert pdflatex.PDFLaTeX.verify_install()
        # assert which("pdflatex") is not None

    def test_tmp_dir(self):
        with tempfile.TemporaryDirectory() as td:
            # create a file "myfile" in "mydir" in temp directory
            f = Path(td, "file")
            f.write_text("Hwllo")
            assert f.read_text() == "Hwllo"

    @pytest.mark.parametrize("filename", ["test_simple", "test_normal"])
    def test_make_pdf_from_tex(self, filename):
        """.tex file must not contain comments"""
        dir = PROG_LOCATION
        output_dir = dir

        texfile = dir.joinpath(filename).with_suffix(".tex")
        LOGGER.debug(texfile)
        pdfl = pdflatex.PDFLaTeX.from_texfile(texfile)
        pdf, log, cp = pdfl.create_pdf(keep_pdf_file=True, dst=output_dir.absolute())
        cp.check_returncode()

        # for item in output_dir.iterdir():
        #     LOGGER.debug(item)

        output_file_pdf = texfile.with_suffix(".pdf")
        assert output_file_pdf.exists()

        pdf_diff(output_file_pdf)

    def test_jinja2_template(self):
        # Third-Party
        import jinja2
        import pandas

        env = pdflatex.JINJA2_ENV
        env["loader"] = jinja2.FileSystemLoader(TEMPLATE_LOCATION)  # ! ( + subfolder)
        env = jinja2.Environment(**env)
        template = env.get_template("template.tex")

        username = "user"

        pdfl = pdflatex.PDFLaTeX.from_jinja2_template(
            template,
            username,  # fails if commented out :'C
            distance="50m",
            animal="Älg",
            data_frame_values=pandas.DataFrame(),
            leader_name="L-O Nilsson",
            shooter_name="Marcus Börne",
            date=r"\DTMnow",
        )
        pdf, log, cp = pdfl.create_pdf(keep_pdf_file=True, dst=PROG_LOCATION)
        cp.check_returncode()

        for item in PROG_LOCATION.iterdir():
            LOGGER.debug(item)

        output_file_pdf = PROG_LOCATION.joinpath(f"{username}.pdf")
        # output_file_pdf = PROG_LOCATION.joinpath(f"template.pdf")
        assert output_file_pdf.exists()

        view_pdf(output_file_pdf)
