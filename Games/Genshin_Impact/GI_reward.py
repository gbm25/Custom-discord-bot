class GenshinReward:

    def __init__(self, item_name=None, quantity=None):
        self.item_name = item_name
        self.quantity = quantity

    def asdict(self):
        return {
            "item_name": self.item_name,
            "quantity": self.quantity
        }
