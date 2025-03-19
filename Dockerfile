#FROM gg-summer.registry.jetbrains.space/p/p7/jajapy/base:latest
FROM ubuntu:jammy 

ARG number_of_threads=2

WORKDIR /base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    cmake \
    clang \
    libboost-all-dev \
    build-essential \
    git \
    libcln-dev \
    libgmp-dev \
    libginac-dev \
    automake \
    libglpk-dev \
    libhwloc-dev \
    libz3-dev \
    libxerces-c-dev \
    libeigen3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install setuptools==68.2.2

RUN git clone --branch 14.25 --single-branch --depth 1 https://github.com/moves-rwth/carl-storm.git /base/carl-storm && \
    git clone --branch 2.2.0 --single-branch --depth 1 https://github.com/moves-rwth/pycarl.git /base/pycarl && \
    git clone --branch 1.8.1 --single-branch --depth 1 https://github.com/moves-rwth/storm.git /base/storm && \
    git clone --branch 1.8.0 --single-branch --depth 1 https://github.com/moves-rwth/stormpy.git /base/stormpy && \
    git clone https://github.com/Rapfff/jajapy.git /base/jajapy


# Build CArL-storm
WORKDIR /base/carl-storm/build
RUN cmake .. && \
    make -j$number_of_threads lib_carl

# Install Pycarl
WORKDIR /base/pycarl
RUN python3 setup.py build_ext --jobs $number_of_threads develop

# Build Storm
WORKDIR /base/storm/build
RUN cmake .. && \
    make -j$number_of_threads binaries

# Install Stormpy
WORKDIR /base/stormpy
RUN python3 setup.py build_ext --jobs $number_of_threads develop

WORKDIR /base/jajapy
RUN pip install numpy==1.26.0 && \
    pip install scipy==1.11.2 && \
    pip install alive-progress==3.1.4 && \
    pip install sympy==1.12 && \
    pip install matplotlib==3.8.1 && \
    pip install pandas==2.2.3 && \
    apt-get update && \ 
    apt-get install check -y && \
    apt-get install gdb -y && \
    rm -rf /var/lib/apt/lists/*

# GO BACK
RUN pip install jajapy
COPY . .
RUN git config --list
# Configure Git user identity
RUN git config --global user.email "saahol20@student.aau.dk"
RUN git config --global user.name "test"
RUN git remote set-url origin git@github.com:AAU-Dat/P10-Thesis.git
#RUN git config branch.test.remote origin
#RUN git config branch.test.merge refs/heads/test

#RUN chmod +x command_script.sh
ENTRYPOINT python3 experiments/models.py && git checkout -b initial-models && git add experiments/initial-models/ experiments/observations/ && git commit -m"made observations and initial probabilities" && git push --set-upstream origin initial-models
#ENTRYPOINT python3 experiments/models.py && tail -f /dev/null