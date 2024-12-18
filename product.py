class Product:
    def __init__(self, title, price, rating, link):
        self.title = title
        self.price = price
        self.rating = rating
        self.link = link

    # Custom comparison based on price first, then rating if prices are equal
    def __lt__(self, other_product):
        if self.price == other_product.price:
            return self.rating > other_product.rating
        return self.price < other_product.price  # Prefer the cheaper product

    # convert to string
    def __repr__(self):
        return f"Product({self.to_dict()})"  

    # convert for easier conversion to json format
    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "link": self.link
        }
