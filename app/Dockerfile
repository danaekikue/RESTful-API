FROM ubuntu:18.04 
RUN apt-get update
RUN apt-get install -y python3 python3-pip 
RUN pip3 install --upgrade pip 
RUN pip3 install flask pymongo 
RUN mkdir /app
RUN mkdir -p /app/data
COPY app.py /app/app.py  
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "app.py" ]