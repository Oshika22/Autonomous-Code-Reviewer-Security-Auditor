# Use a lightweight official Python image
FROM python:3.11-slim
#uses an official pthon image as the base image for the container
#slim variant is used to reduce the image size by excluding unnecessary components.... fewer OS packages= smaller attack surface and faster downloads
#fixes python version to 3.11==> ensures consistency across different environments (reproducibility)



# Create a non-root user for isolation
RUN useradd -m appuser
#creates a non-root linux user named appuser with a home directory
#enhances security by limiting permissions and access within the container; containers run as root by default, which can pose security risks if vulnerabilities are exploited. By creating and using a non-root user, we reduce the potential impact of any security breaches.
#improves basic sandboxing 



# Set working directory inside the container
WORKDIR /app
#set /app as the working directory for all subsequent instructions in the Dockerfile
#all commands now run inside /app



# Install minimal system dependencies; some python packages may require compilation (gcc needed fot that)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
#remove package cache to keep image small



# Copy dependency list first (Docker layer caching)
COPY requirements.txt .
#docker builds images in layers; if requirements.txt doesnot change, dependencies are not reinstalled
#Dependencies are copied separately to leverage Docker layer caching



# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
#Installs all Python dependencies; Uses --no-cache-dir to reduce image size; Guarantees same library versions everywhere



# Copy the entire project into the container (rag, knowledgebase, visualization, readme, etc.)
COPY . .



# Fix ownership so non-root user can access files
RUN chown -R appuser:appuser /app
#Gives file ownership to non-root user; Prevents permission errors; Required when switching users

# Switch to non-root user
USER appuser

# Expose backend port (for future API/frontend use)
EXPOSE 8000

# Start the backend application
CMD ["python", "rag/main.py"]
#This is what runs when container starts; Executes your existing backend logic