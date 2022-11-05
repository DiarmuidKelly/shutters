FROM python:3

#Set the working directory
WORKDIR /usr/src/app

#copy all the files
COPY requirements.txt .
COPY src/ .

#Install the dependencies
RUN apt-get -y update
RUN pip3 install --no-cache-dir -r requirements.txt

#Expose the required port
EXPOSE 5000

#Run the command
CMD ["python3", "main.py"]
