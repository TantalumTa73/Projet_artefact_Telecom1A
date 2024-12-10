import requests
import time

url = "http://proj103.r2.enst.fr"

def send_request(api,data=None):
	print("\n"+"-"*10)
	full_url = url+api
	print(f"Sending request {full_url}")
	if data is not None:
		print(f"... with data:\n{data}\n")
		r = requests.post(full_url,json=data)
	else:
		r = requests.post(full_url)
	print(f"Status code {r.status_code}")
	try:
		print(r.json())
	except:
		print("Response unreadable")
	print("-"*10)
	return r
	

while True:
	print("\n"+"="*30)
	print("="*30)
	print(f"Select request to send:\n")
	print(f"1) Update position")
	print(f"2) Capture flag")
	print(f"3) Start race")
	print(f"4) Get race status")
	print(f"5) Write to registers")
	print(f"6) Read registers")
	choice = int(input("\nChoice: "))
	print()

	match choice:
		case 1:
			print(f"Updating position")
			x,y = map(int,input("New position (x y): ").split(" "))
			send_request(f"/api/pos?x={x}&y={y}")
		case 2:
			print("Capturing flag")
			marker = int(input("Marker id: "))
			col,row = input("Flag position (col(1..6) row(A..G): ").split(" ")
			send_request(f"/api/marker?id={marker}&col={col}&row={row}")
		case 3:
			print("Starting race")
			send_request(f"/api/start")
		case 4:
			print("Getting status")
			send_request(f"/api/status")
		case 5:
			print("Writing to register")
			register_id = int(input("Register id (1..5): "))
			option = input("Writing to all (true|false): ")
			data = input("Data to write to register: ")
			send_request(f"/api/udta?idx={register_id}&all={option}",data=data)
		case 6:
			print("Reading a register")
			register_id = int(input("Register id (1..5): "))
			team_id = int(input("Team id who's reading (1..5): "))
			send_request(f"/api/udta?idx={register_id}&t={team_id}")





