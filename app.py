from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# Dati di esempio
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# 1. READ con RICERCA: Visualizza transazioni filtrate e calcola il bilancio
@app.route("/")
def get_transactions():
    # Recuperiamo il termine di ricerca dall'URL (es: ?search=giugno)
    search_query = request.args.get('search')
    
    if search_query:
        # Se c'è una ricerca, filtriamo la lista controllando sia la data che l'importo
        filtered_data = [
            t for t in transactions 
            if search_query.lower() in t['date'].lower() or search_query in str(t['amount'])
        ]
    else:
        # Se non c'è ricerca, mostriamo tutto
        filtered_data = transactions

    # Calcoliamo il bilancio totale SOLO sulle transazioni attualmente visibili
    total = sum(transaction['amount'] for transaction in filtered_data)
    
    # Passiamo i dati filtrati e il totale al template
    return render_template("transactions.html", transactions=filtered_data, total_balance=total)

# 2. CREATE: Aggiungi nuova transazione
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # Creiamo un nuovo ID cercando il massimo attuale per evitare duplicati
        new_id = max([t['id'] for t in transactions], default=0) + 1
        
        transaction = {
            'id': new_id,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    
    return render_template("form.html")

# 3. UPDATE: Modifica transazione esistente
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        return redirect(url_for("get_transactions"))
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    return {"message": "Transaction not found"}, 404

# 4. DELETE: Rimuovi una transazione
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Funzione extra: Rotta testuale per il bilancio
@app.route("/balance")
def total_balance():
    balance = sum(t['amount'] for t in transactions)
    return f"Total Balance: {balance}"

if __name__ == "__main__":
    app.run(debug=True)