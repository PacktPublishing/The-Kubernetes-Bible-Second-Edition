# Base image
FROM ubuntu:20.04

# Install curl, jq, and any other dependencies
RUN apt-get update && apt-get install -y curl jq

# Copy the hamster script into the container
COPY hamster.sh /usr/local/bin/hamster.sh

# Make the script executable
RUN chmod +x /usr/local/bin/hamster.sh

# Set environment variable
ENV TOTAL_HAMSTER_USAGE="1.0"

# Set the entrypoint to the hamster script
ENTRYPOINT ["/usr/local/bin/hamster.sh"]
