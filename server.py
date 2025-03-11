from flask import Flask, request, jsonify

app = Flask(__name__)

# Guardar los datos de ambas manos
hand_data = {}

@app.route("/get_position", methods=["POST", "GET"])
def get_position():
    global hand_data

    if request.method == "POST":
        new_data = request.get_json()

        # 🔍 Verificamos que new_data sea un diccionario con datos de ambas manos
        if isinstance(new_data, dict) and any(key.startswith(("L", "R")) for key in new_data):
            hand_data = new_data  # Guardamos los datos correctamente
        else:
            print("⚠️ Error: Datos recibidos en formato incorrecto:", new_data)

        return jsonify({"message": "Datos recibidos", "data": hand_data})
    
    elif request.method == "GET":
        return jsonify(hand_data)

if __name__ == "__main__":
    app.run(debug=True)
