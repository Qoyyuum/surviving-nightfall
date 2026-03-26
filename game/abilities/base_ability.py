class BaseAbility:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.level = 1
        self.max_level = 3
        self.owner = None
        self.is_active = False

    def activate(self, owner):
        self.owner = owner
        self.is_active = True
        self.on_activate()

    def deactivate(self):
        self.is_active = False
        self.on_deactivate()

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.on_upgrade()

    def can_upgrade(self):
        return self.level < self.max_level

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_upgrade(self):
        pass

    def update(self):
        pass
