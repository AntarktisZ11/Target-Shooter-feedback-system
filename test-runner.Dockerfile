# Image from which to build onto from
FROM balenalib/amd64:build

# Update Ubuntu and install 'tkinter' and 'pip'
RUN sudo apt update
RUN sudo apt-get install python3-tk && sudo apt-get -y install python3-pip


# Install Kile - LaTeX compiler & required package
RUN sudo apt-get install kile texlive-xetex texlive-plain-generic

# Install Okular - PDF viewer
RUN sudo apt-get install okular

# Pre-Install requirements
RUN pip3 install numpy matplotlib pandas jinja2 pytest pytest-cov coverage-conditional-plugin
RUN sudo apt-get install python3-lxml poppler-utils
RUN sudo apt-get install python3-dev
RUN pip3 install pdf-diff
RUN pip3 install pdbpp

WORKDIR /home
COPY . L-O

WORKDIR /home/L-O
RUN pip3 install -r requirements-dev.txt
CMD bash -c "pytest && cd htmlcov && python3 -m http.server"
# CMD bash -c "tail -f /dev/null"
# CMD bash -c "pdf-diff 'tests/sender/latex-print/Bortans_Jaktskyttebana.pdf' 'tests/sender/latex-print/Bortans_Jaktskyttebana (1).pdf' > comparison_output.png && okular comparison_output.png"
