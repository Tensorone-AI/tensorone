# Use Node.js 18 Alpine as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Copy and set permissions for scripts
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
COPY docker/docker-healthcheck.sh /docker-healthcheck.sh
RUN chmod +x /docker-entrypoint.sh /docker-healthcheck.sh

# Expose port
EXPOSE 3000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /docker-healthcheck.sh

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start the application
CMD ["node", "build"]