FROM python:3.11.4


RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*


COPY python_files /app/backend/
WORKDIR /app/backend


RUN pip install -r requirements.txt


EXPOSE 5000


# #For Local Docker Testing
# CMD ["python", "app.py"]


#For Production Deployment
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "wsgi:app"]












