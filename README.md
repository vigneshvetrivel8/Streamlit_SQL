# Project Setup Instructions

## Setup postgres database  
### Follow these steps to install and configure PostgreSQL:  

Update Package List:    
sudo apt update  

Install PostgreSQL and Contrib Packages:    
sudo apt install postgresql postgresql-contrib  

Check PostgreSQL Service Status:    
sudo systemctl status postgresql  

Enable PostgreSQL to Start on Boot:     
sudo systemctl enable postgresql  

Access PostgreSQL Command Line Interface:    
sudo -u postgres psql  

Execute the following SQL commands within the PostgreSQL CLI:  
Create User and Database:  
1)CREATE USER username WITH PASSWORD 'password';  
CREATE DATABASE database_name;  
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;  
2)\q  

## Setup Environment variables:  
Fill up the .env file with their respective values

##  Run the app:  

Install Required Python Packages:  
pip install -r requirements.txt  

Create the Database and Tables:    
python3 create_db.py  

Run the Application with Streamlit:    
streamlit run app.py  

## Note:  
If you encounter issues with protobuf, you may need to upgrade it:  
pip install --upgrade protobuf  