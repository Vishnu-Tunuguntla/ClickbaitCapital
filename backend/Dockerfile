FROM python:3.11.4

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

COPY python_files /app/backend/
WORKDIR /app/backend

RUN pip install -r requirements.txt

EXPOSE 5000

#For Local Docker Testing
CMD ["python", "app.py"]

#For Production Deployment
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "wsgi:app"]






#Environment Variables to be set:
#GPT_API_KEY
#FRONTEND_HOST --> http://localhost:3000 
#REACT_APP_BACKEND_HOST --> http://localhost:5000

#Docker Commands:
#docker build -t kit-backend:tag .
#docker run -p 5000:5000 -e GPT_API_KEY=your-api-key -e FRONTEND_HOST=http://localhost:3000 -v C:/Users/15715/Desktop/KITProj/KIT/backend/Python_Files/Main_Scripts/best.pt:/app/backend/best.pt kit-backend 
#docker run -p 5000:5000 -e GPT_API_KEY=your-api-key -e FRONTEND_HOST="*" vishnut04/kit-backend:deploymentv1 --> for deployment, -v file mounting not required!
#docker kill $(docker ps -q) --> kills all containers
#docker rm container:id --> removes container