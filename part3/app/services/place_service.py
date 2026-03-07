from app.models.place import Place

class PlaceService:
    def __init__(self):
        self.places = {}  # Simple in-memory storage, key=id, value=Place instance

    def create_place(self, data):
        place = Place(**data)
        self.places[place.id] = place
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None
        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        place.updated_at = datetime.now()
        return place

    def list_places(self):
        return list(self.places.values())

