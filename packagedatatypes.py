class Package:
    def __init__(self,name,request,x,y) -> None:
        self.name = name
        self.request = request
        self.x = x
        self.y = y
    def to_json(self):
        return "{"+ f"'name':'{self.name}','request':'{self.request}','x':'{self.x}','y':'{self.y}'" +"}"
    def read_json(json):
        if len(json)<1:
            return "no opponent"
        dict_form = eval(json)
        name = dict_form["name"]
        request = dict_form["request"]
        x = dict_form["x"]
        y = dict_form["y"]
        return Package(name,request,x,y)