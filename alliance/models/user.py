class User:
    def __init__(self, profile: dict):
        self.profile = profile

    def update(self, updates: dict):
        self.profile.update(updates)

    def to_dict(self):
        return self.profile
