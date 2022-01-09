from duchamp_reader.app import app
from duchamp_reader.constantes import actual_path, templates

print(actual_path)
print(templates)

if __name__ == "__main__":
    app.run(debug=True)