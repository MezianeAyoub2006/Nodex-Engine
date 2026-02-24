class EventBus:
    def __init__(self):
        self.events = [] 
    
    def push(self, type, **kwargs):
        self.events.append({
            "type" : type
        } | kwargs) 