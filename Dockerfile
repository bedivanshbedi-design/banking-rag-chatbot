from python:3.10

# Set working directory
WORKDIR /app

#Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy backend file
COPY  .  .

#Expose port
EXPOSE 8000

#RUN fastapi

CMD ["uvicorn" , "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


