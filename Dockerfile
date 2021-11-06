## remeber to put this in the project folder
## here is the dockerfile for the techtrends project 01

FROM python:2.7
LABEL maintainer="Mordern Geek"
EXPOSE 3111
WORKDIR /techtrends
COPY ./ .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]