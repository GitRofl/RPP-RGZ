from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# Временное хранилище контактов
contacts = {}
next_id = 1

@app.route('/contacts', methods=['POST'])
def create_contact():
    """Создание нового контакта
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: artem
            phone:
              type: string
              example: "+79232334666"
    responses:
      201:
        description: Контакт создан
    """
    global next_id
    data = request.get_json()
    contact_id = next_id
    contacts[contact_id] = data
    next_id += 1
    return jsonify({"id": contact_id}), 201

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    """Получение информации о контакте по ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Информация о контакте
      404:
        description: Контакт не найден
    """
    contact = contacts.get(id)
    if not contact:
        return jsonify({"error": "Контакт не найден"}), 404
    return jsonify(contact)

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    """Удаление контакта по ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Контакт удалён
      404:
        description: Контакт не найден
    """
    if id not in contacts:
        return jsonify({"error": "Контакт не найден"}), 404
    del contacts[id]
    return jsonify({"message": "Контакт удалён"}), 200

if __name__ == "__main__":
    app.run(debug=False)

