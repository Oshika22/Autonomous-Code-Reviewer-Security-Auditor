# Lightweight Nginx image
FROM nginx:alpine

# Copy the frontend landing page
COPY docker/frontend/index.html /usr/share/nginx/html/index.html

# Copy the Tableau dashboard for static download 
# The build context is the project root
COPY visualization/security_dashboard.twbx /usr/share/nginx/html/security_dashboard.twbx

# Nginx serves on port 80 by default
EXPOSE 80
