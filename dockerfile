# Basic setup
FROM python:3.10

# Update system packages
RUN apt-get update && apt-get install -y \
    sudo \
    git \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Setup user to not run as root
RUN adduser --disabled-password --gecos '' autogen-dev
RUN adduser autogen-dev sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER autogen-dev
WORKDIR /home/autogen-dev

# Clone repo
RUN git clone https://github.com/microsoft/autogen.git
WORKDIR /home/autogen-dev/autogen

# Install Python packages
# Add your requirements.txt file to the same directory as Dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install autogen from GitHub
RUN pip install git+https://github.com/microsoft/autogen.git

# Install precommit hooks
RUN pre-commit install

# For docs
RUN sudo npm install --global yarn
RUN pip install pydoc-markdown
WORKDIR /home/autogen-dev/autogen/website
RUN yarn install --frozen-lockfile --ignore-engines

# Override default image starting point
CMD ["/bin/bash"]
ENTRYPOINT []