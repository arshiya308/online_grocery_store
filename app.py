from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "grocery_secret_key"

# ---------------- PRODUCTS ----------------
products = [
    {"name": "Apple", "price": 120, "image": "images/apples.jpg"},
    {"name": "Banana", "price": 40, "image": "images/banana.jpg"},
    {"name": "Oil", "price": 150, "image": "images/oil.jpg"},
    {"name": "Rice", "price": 80, "image": "images/rice.jpg"},
    {"name": "Milk", "price": 60, "image": "images/milk.jpg"},
    {"name": "Eggs", "price": 70, "image": "images/eggs.jpg"},
]

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["cart"] = []
        session["orders"] = []
        return redirect(url_for("products_page"))
    return render_template("login.html")

# ---------------- PRODUCTS ----------------
@app.route("/products")
def products_page():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", products=products, username=session["username"])

# ---------------- ADD TO CART ----------------
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "username" not in session:
        return redirect(url_for("login"))

    product_name = request.form["product"]
    session["cart"].append(product_name)
    session.modified = True  # ⭐ IMPORTANT
    flash("Item added to cart")
    return redirect(url_for("products_page"))

# ---------------- CART ----------------
@app.route("/cart")
def cart():
    if "username" not in session:
        return redirect(url_for("login"))

    cart_items = session.get("cart", [])
    item_count = {}
    for item in cart_items:
        item_count[item] = item_count.get(item, 0) + 1

    cart_details = []
    total = 0
    for p in products:
        if p["name"] in item_count:
            qty = item_count[p["name"]]
            price = qty * p["price"]
            total += price
            cart_details.append({
                "name": p["name"],
                "qty": qty,
                "price": price
            })

    return render_template(
        "cart.html",
        cart=cart_details,
        total=total,
        username=session["username"]
    )

# ---------------- PLACE ORDER ----------------
@app.route("/place_order")
def place_order():
    if "username" not in session:
        return redirect(url_for("login"))

    session["orders"].extend(session["cart"])
    session["cart"] = []
    flash("Order placed successfully")
    return redirect(url_for("orders"))

# ---------------- ORDERS ----------------
@app.route("/orders")
def orders():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("orders.html", orders=session.get("orders", []))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)