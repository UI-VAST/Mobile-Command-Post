from SatComm import create_app

print("Creating App")
app = create_app()
print("Running App")
app.run(host="localhost", port=8080, debug=True)
