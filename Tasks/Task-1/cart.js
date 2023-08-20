// Sample cart data
const cartItems = [
    { id: 1, name: "Men's Shoe 1", price: 79.99, quantity: 2 },
    { id: 2, name: "Women's Shoe 1", price: 89.99, quantity: 1 }
  ];
  
  // Calculate cart subtotal and total
  function calculateTotals() {
    let subtotal = 0;
    for (const item of cartItems) {
      subtotal += item.price * item.quantity;
    }
  
    const shipping = 5.00;
    const total = subtotal + shipping;
  
    document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById("total").textContent = `$${total.toFixed(2)}`;
  }
  
  // Populate cart items
  function populateCart() {
    const cartItemsContainer = document.getElementById("cart-items");
    cartItemsContainer.innerHTML = '';
  
    for (const item of cartItems) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>$${item.price.toFixed(2)}</td>
        <td>${item.quantity}</td>
        <td>$${(item.price * item.quantity).toFixed(2)}</td>
        <td><button class="btn btn-danger btn-sm remove-item" data-id="${item.id}">Remove</button></td>
      `;
  
      cartItemsContainer.appendChild(row);
    }
  
    calculateTotals();
  }
  
  // Handle item removal
  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-item")) {
      const itemId = parseInt(event.target.getAttribute("data-id"));
      const itemIndex = cartItems.findIndex(item => item.id === itemId);
      if (itemIndex !== -1) {
        cartItems.splice(itemIndex, 1);
        populateCart();
      }
    }
  });
  
  // Initialize the cart
  populateCart();
  