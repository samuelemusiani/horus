# Use Node.js as base image
FROM node:20 as frontend-build

# Set working directory for frontend
WORKDIR /app/client

# Copy frontend source code
COPY client/ .
RUN npm install

# Build frontend
RUN npm run build

# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Node.js and npm for serving frontend
RUN apt-get update && \
    apt-get install -y nodejs npm curl nmap iproute2 iputils-ping

# Copy frontend build from previous stage
COPY --from=frontend-build /app/client/dist /app/client/dist

# Install serve to host frontend
RUN npm install -g serve

# Copy backend requirements and install dependencies
COPY server/requirements.txt /app/server/
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy backend source code
COPY server/ /app/server/

# Create startup script
RUN echo '#!/bin/bash\n\
python /app/server/main.py & \n\
serve -s /app/client/dist -l 3000' > /app/start.sh && \
chmod +x /app/start.sh

# Expose ports
EXPOSE 3000 8000

# Start both services
CMD ["/app/start.sh"]
