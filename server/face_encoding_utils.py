import face_recognition
def get_encoding(picture): # for when a client sends a picture to register with, returns the encoding of the named face in the picture
    return face_recognition.face_encodings(picture)[0]
def get_potential_hits(names, known_encodings, picture):
    face_positions = face_recognition.face_locations(picture)
    unknown_encodings = face_recognition.face_encodings(picture, face_positions=face_positions)
    found_faces = []
    for unkEn, fPos in zip(unknown_encodings, face_positions):
        foundFaces = face_recognition.compare_faces(known_encodings, unkEn)
        for isFound, name in zip(foundFaces, names):
            if isFound:
                found_faces.append((name, fPos))
    return found_faces