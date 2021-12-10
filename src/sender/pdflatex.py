# Standard Library
import logging  # Dev-tool
import shutil
import subprocess
import tempfile
from pathlib import Path
from subprocess import PIPE

# Third-Party
from jinja2 import Template

LOGGER = logging.getLogger(__name__)  # Dev-tool

MODE_BATCH = 0
MODE_NON_STOP = 1
MODE_SCROLL = 2
MODE_ERROR_STOP = 3
INTERACTION_MODES = ["batchmode", "nonstopmode", "scrollmode", "errorstopmode"]

JINJA2_ENV = {
    "block_start_string": "\BLOCK{",
    "block_end_string": "}",
    "variable_start_string": "\VAR{",
    "variable_end_string": "}",
    "comment_start_string": "\#{",
    "comment_end_string": "}",
    "line_statement_prefix": "%%",
    "line_comment_prefix": "%#",
    "trim_blocks": True,
    "autoescape": False,
}


class PDFLaTeX:
    """
    Modified by Antarktis 2021-07-01
    """

    def __init__(self, tex_src_bin, job_name: str):
        self.verify_install()
        self.tex_src_bin = tex_src_bin
        self.job_name = job_name
        self.interaction_mode = INTERACTION_MODES[MODE_NON_STOP]
        self.dst = None
        self.pdf_filename = None
        self.params = dict()
        self.pdf = None
        self.log = None

    @staticmethod
    def verify_install():
        """Check whether pdflatex tool is on PATH and marked as executable.

        Raises:
            FileNotFoundError: pdflatex could not be found on PATH

        Returns:
            bool: True if it is installed
        """
        if shutil.which("pdflatex") is None:  # pragma: no cover
            raise shutil.ExecError("Aborting! pdflatex could not be found on PATH")
        else:
            return True

    @classmethod
    def from_texfile(cls, file: Path):
        formated_src = file.read_text().replace("\n", " ")
        return cls.from_binarystring(formated_src.encode(), file.stem)

    @classmethod
    def from_binarystring(cls, binstr: str, jobname: str):
        return cls(binstr, jobname)

    @classmethod
    def from_jinja2_template(cls, jinja2_template: Template, jobname: str = None, **render_kwargs):
        tex_src = jinja2_template.render(**render_kwargs)
        tex_src_bin = tex_src.replace("\n", " ").encode()
        fn = jobname

        if fn is None:
            fn = jinja2_template.filename
            if not fn:
                raise ValueError(
                    "PDFLaTeX: if jinja template does not have attribute 'filename' set, 'jobname' must be provided"
                )
        return cls(tex_src_bin, fn)

    def create_pdf(self, keep_pdf_file: bool = False, keep_log_file: bool = False, env: dict = None, dst: Path = None):
        if self.interaction_mode is not None:
            self.add_args({"-interaction": self.interaction_mode})

        self.add_args({"--file-line-error": None})  # output c style errors

        # dst = self.params.get('-output-directory')
        filename = self.params.get("-jobname")

        if filename is None:
            filename = self.job_name
        if dst is None:
            dst = Path("")

        with tempfile.TemporaryDirectory() as td:
            self.set_output_directory(td)
            self.set_jobname("file")

            args = self.get_run_args()
            fp = subprocess.run(args, input=self.tex_src_bin, env=env, timeout=300, stdout=PIPE, stderr=PIPE)

            if fp.returncode != 0:  # pragma: no cover
                LOGGER.warning(fp.args)
                LOGGER.warning(fp.stdout.decode())
            LOGGER.debug(subprocess.run(["ls", "-R", "/tmp"]))
            LOGGER.debug(subprocess.run(["tail", f"{td}/file.log"]))
            LOGGER.debug(subprocess.run(["tail", f"{td}/file.aux"]))

            temp_pdf = Path(td, "file.pdf")
            self.pdf = temp_pdf.read_bytes()

            temp_log = Path(td, "file.log")
            self.log = temp_log.read_bytes()

            if keep_pdf_file:
                target_pdf = dst.joinpath(filename).with_suffix(".pdf")
                shutil.move(temp_pdf, target_pdf)

            if keep_log_file:
                target_log = dst.joinpath(filename).with_suffix(".log")
                shutil.move(temp_log, target_log)

        return self.pdf, self.log, fp

    def get_run_args(self):
        a = [k + ("=" + v if v is not None else "") for k, v in self.params.items()]
        a.insert(0, "pdflatex")
        return a

    def add_args(self, params: dict):
        for k in params:
            self.params[k] = params[k]

    def set_output_directory(self, dst: str = None):
        self.generic_param_set("-output-directory", dst)

    def set_jobname(self, jobname: str = None):
        self.generic_param_set("-jobname", jobname)

    def generic_param_set(self, param_name, value):
        if value is None:
            if param_name in self.params.keys():
                del self.params[param_name]
        else:
            self.params[param_name] = value
