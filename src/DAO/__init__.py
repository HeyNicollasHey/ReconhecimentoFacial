import psycopg2
from PIL import Image
from io import BytesIO
import face_recognition as fc
import io
def conexaodb():
    conn = psycopg2.connect(
        dbname="reconhecimentoFacial",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    return conn
def insert_image(image_path, name):
    conn = conexaodb()
    cursor = conn.cursor()

    with open(image_path, 'rb') as file:
        img_data = file.read()

    cursor.execute('''
        INSERT INTO images (name, image) VALUES (%s, %s)
    ''', (name, psycopg2.Binary(img_data)))

    conn.commit()
    cursor.close()
    conn.close()

def retornar_image_id(image_id):
    conn = conexaodb()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT image FROM images WHERE id = %s
    ''', (image_id,))

    img_data = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    img = Image.open(BytesIO(img_data))

    return img

def retornar_image_name(image_name):
    conn = conexaodb()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT image FROM images WHERE name = %s
    ''', (image_name,))

    img_data = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    img = Image.open(BytesIO(img_data))

    return img
def reconhecerRosto(foto):
    conn = conexaodb()

    face_image = fc.load_image_file(foto)
    face_encodings = fc.face_encodings(face_image)

    if not face_encodings:
        print("Nenhum rosto encontrado na imagem fornecida.")
        return

    cur = conn.cursor()

    cur.execute("SELECT id, name, image FROM images")
    imagens = cur.fetchall()

    banco_encodings = {}

    for img in imagens:
        img_id, img_nome, img_bin = img

        img_io = io.BytesIO(img_bin)
        face_unknown = fc.load_image_file(img_io)
        face_unknown_encodings = fc.face_encodings(face_unknown)

        if face_unknown_encodings:
            banco_encodings[img_nome] = face_unknown_encodings[0]

    for i, face_encoding in enumerate(face_encodings):
        encontrado = False
        for nome, encoding_banco in banco_encodings.items():
            resultado = fc.compare_faces([encoding_banco], face_encoding)

            if resultado[0]:
                print(f"Rosto {i + 1}: {nome} está presente na imagem.")
                encontrado = True

        if not encontrado:
            print(f"Rosto {i + 1}: Não identificado no banco de dados.")

    cur.close()
    conn.close()
