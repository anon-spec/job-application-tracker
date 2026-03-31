#Database connection functions
import mysql.connector


def get_db():
	return mysql.connector.connect(
		host='localhost',
		user='root',
		port='3307',
		password='bopfod-coWhe4-boqzyz',
		database='job_application_tracker'
	)
