FROM python:3.11.2

# Set the working directory in the container
WORKDIR /app
# Copy the entrypoint script into the container
# COPY ./open_cam.sh /usr/local/bin/entrypoint.sh
COPY ./open_browser.sh /usr/local/bin/open_browser.sh
# Make the entrypoint script executable
# RUN chmod +x /usr/local/bin/entrypoint.sh
ADD . .
# Install Python packages
RUN pip install mediapipe
RUN pip install streamlit
RUN pip install keyboard
RUN pip install psutil
RUN pip install opencv-python-headless

# Set execute permissions for the script
RUN chmod +x /usr/local/bin/open_browser.sh
# RUN device=/dev/video0
# Set the entrypoint script
EXPOSE 8501
ENTRYPOINT [ "streamlit","run","app.py"]
