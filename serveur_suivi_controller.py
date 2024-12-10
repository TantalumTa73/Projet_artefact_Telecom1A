import requests
import time

url = "http://proj103.r2.enst.fr"
mode_test = False
test_team_id = -1

def send_request(api,data=None,method="POST"):
	print("\n"+"-"*10)
	full_url = url+api
	print(f"Sending request {full_url}",end=" ")
	if data is not None:
		print(f"with data:\n{data}\n")
		r = requests.post(full_url,json=data)
	else:
		if method=="POST":
			print(f"with method POST")
			r = requests.post(full_url)
		elif method=="GET":
			print(f"with method GET")
			r = requests.get(full_url)
		else:
			print(f"\nUnrecognized method {method}")

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
	if mode_test:
		print(f"Mode test enabled, using team {test_team_id}")
	else:
		print(f"Mode test not active")
	print(f"Choose action:\n")
	print(f"1) Update position")
	print(f"2) Capture flag")
	print(f"3) Start race")
	print(f"4) Stop race")
	print(f"5) Get race status")
	print(f"6) Get flags")
	print(f"7) Write to registers")
	print(f"8) Read registers")
	print(f"9) Toggle test mode")
	choice = int(input("\nChoice: "))
	print()

	match choice:
		case 1:
			print(f"Updating position")
			x,y = map(int,input("New position (x y): ").split(" "))
			if mode_test:
				send_request(f"/api/pos?x={x}&y={y}&t={test_team_id}")
			else:
				send_request(f"/api/pos?x={x}&y={y}")
		case 2:
			print("Capturing flag")
			marker = int(input("Marker id: "))
			col,row = input("Flag position (col(1..6) row(A..G): ").split(" ")
			if mode_test:
				send_request(f"/api/marker?id={marker}&col={col}&row={row}&t={test_team_id}")
			else:
				send_request(f"/api/marker?id={marker}&col={col}&row={row}")
		case 3:
			print("Starting race")
			send_request(f"/api/start")
		case 4:
			print("Stopping race")
			send_request(f"/api/stop")
		case 5:
			print("Getting status")
			send_request(f"/api/status",method="GET")
		case 6:
			print("Getting flags")
			send_request(f"/api/checkboard",method="GET")
		case 7:
			print("Writing to register")
			register_id = int(input("Register id (1..5): "))
			option = input("Writing to all (true|false): ")
			data = input("Data to write to register: ")
			send_request(f"/api/udta?idx={register_id}&all={option}",data=data)
		case 8:
			print("Reading a register")
			register_id = int(input("Register id (1..5): "))
			team_id = int(input("Team id who's reading (1..5): "))
			send_request(f"/api/udta?idx={register_id}&t={team_id}",method="GET")
		case 9:
			if mode_test:
				print("Disabling test mode")
				mode_test = False
			else:
				print("Activating test mode")
				test_team_id = int(input("Team id: "))
				mode_test = True





