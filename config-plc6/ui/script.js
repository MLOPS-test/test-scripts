let balance = 0.00;

function deposit() {
    const amount = parseFloat(document.getElementById("amount").value);
    if (isNaN(amount) || amount <= 0) {
        showMessage("Please enter a valid deposit amount.");
        return;
    }
    balance += amount;
    updateBalance();
    showMessage(`Deposited ₹${amount.toFixed(2)} successfully.`);
}

function withdraw() {
    const amount = parseFloat(document.getElementById("amount").value);
    if (isNaN(amount) || amount <= 0) {
        showMessage("Please enter a valid withdrawal amount.");
        return;
    }
    if (amount > balance) {
        showMessage("Insufficient funds.");
        return;
    }
    balance -= amount;
    updateBalance();
    showMessage(`Withdrew ₹${amount.toFixed(2)} successfully.`);
}

function updateBalance() {
    document.getElementById("balance").textContent = balance.toFixed(2);
}

function showMessage(msg) {
    document.getElementById("message").textContent = msg;
}


