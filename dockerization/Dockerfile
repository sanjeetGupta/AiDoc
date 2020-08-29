## Base Image
FROM python:3.7.3

# Install packages
RUN pip install tensorflow-cpu==2.1.0
RUN pip install Flask==1.1.1
RUN pip install tensorflow-text==2.1.1

# transfer the required files
ADD ./app.py /ai-doc/
RUN mkdir ai-doc/model
ADD ./model/3/ /ai-doc/model/3/

# set working directory
WORKDIR /ai-doc

## Expose the port flask is using
EXPOSE 8501
# run the app.py when the image is started
CMD ["python", "app.py"]



