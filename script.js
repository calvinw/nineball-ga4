// Shopping cart functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Product data
const products = {
    'laptop-001': { id: 'laptop-001', name: 'Premium Laptop', price: 999.99, category: 'Electronics' },
    'phone-001': { id: 'phone-001', name: 'Smartphone Pro', price: 699.99, category: 'Electronics' },
    'watch-001': { id: 'watch-001', name: 'Smart Watch', price: 299.99, category: 'Electronics' }
};

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    // Check which page we're on and initialize accordingly
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'cart.html') {
        displayCart();
    } else if (currentPage === 'checkout.html') {
        displayCheckout();
    }
    
    // Track page view
    trackPageView();
});

// Track page views
function trackPageView() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const pageTitle = document.title;
    
    gtag('event', 'page_view', {
        page_title: pageTitle,
        page_location: window.location.href,
        page_path: window.location.pathname
    });
}

// GA4 Event Tracking Functions (with fallback for when GA4 isn't loaded)
function trackEvent(eventName, parameters = {}) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, parameters);
    }
}

function trackPurchase(transactionId, items, value) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'purchase', {
            transaction_id: transactionId,
            value: value,
            currency: 'USD',
            items: items
        });
    }
}

function trackAddToCart(item) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'add_to_cart', {
            currency: 'USD',
            value: item.price,
            items: [{
                item_id: item.id,
                item_name: item.name,
                category: item.category,
                price: item.price,
                quantity: 1
            }]
        });
    }
}

function trackViewItem(item) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'view_item', {
            currency: 'USD',
            value: item.price,
            items: [{
                item_id: item.id,
                item_name: item.name,
                category: item.category,
                price: item.price
            }]
        });
    }
}

function trackBeginCheckout(items, value) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'begin_checkout', {
            currency: 'USD',
            value: value,
            items: items
        });
    }
}

// Product Functions
function viewProduct(productId, productName, price) {
    const product = products[productId];
    if (product) {
        trackViewItem(product);
    }
    
    // Navigate to product page based on product ID
    let productPage;
    switch(productId) {
        case 'laptop-001':
            productPage = 'product-laptop.html';
            break;
        case 'phone-001':
            productPage = 'product-phone.html';
            break;
        case 'watch-001':
            productPage = 'product-watch.html';
            break;
        default:
            productPage = 'products.html';
    }
    
    window.location.href = productPage;
}

function addToCart(productId, productName, price) {
    const product = products[productId];
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Track GA4 event
    trackAddToCart(product);
    
    // Show success message
    showNotification(`${productName} added to cart!`);
}

function buyNow(productId, productName, price) {
    addToCart(productId, productName, price);
    window.location.href = 'checkout.html';
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    displayCart();
}

function updateQuantity(productId, quantity) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = Math.max(1, quantity);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        displayCart();
    }
}

function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElements = document.querySelectorAll('#cart-count');
    cartCountElements.forEach(element => {
        element.textContent = totalItems;
    });
}

function calculateTotals() {
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const tax = subtotal * 0.085; // 8.5% tax
    const total = subtotal + tax;
    
    return { subtotal, tax, total };
}

function displayCart() {
    const cartEmpty = document.getElementById('cart-empty');
    const cartItems = document.getElementById('cart-items');
    const cartList = document.getElementById('cart-list');
    
    if (cart.length === 0) {
        cartEmpty.classList.remove('hidden');
        cartItems.classList.add('hidden');
        return;
    }
    
    cartEmpty.classList.add('hidden');
    cartItems.classList.remove('hidden');
    
    cartList.innerHTML = '';
    
    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.className = 'flex items-center justify-between p-6';
        const imageMap = {
            'laptop-001': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=80&h=80&fit=crop&crop=center',
            'phone-001': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=80&h=80&fit=crop&crop=center',
            'watch-001': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=80&h=80&fit=crop&crop=center'
        };
        
        cartItem.innerHTML = `
            <div class="flex items-center space-x-4">
                <img src="${imageMap[item.id] || 'https://via.placeholder.com/80x80/007bff/ffffff?text=Product'}" alt="${item.name}" class="w-16 h-16 rounded object-cover">
                <div>
                    <h4 class="font-semibold">${item.name}</h4>
                    <p class="text-gray-600">$${item.price.toFixed(2)}</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <div class="flex items-center space-x-2">
                    <button onclick="updateQuantity('${item.id}', ${item.quantity - 1})" class="bg-gray-200 text-gray-700 w-8 h-8 rounded hover:bg-gray-300">−</button>
                    <span class="w-8 text-center">${item.quantity}</span>
                    <button onclick="updateQuantity('${item.id}', ${item.quantity + 1})" class="bg-gray-200 text-gray-700 w-8 h-8 rounded hover:bg-gray-300">+</button>
                </div>
                <span class="font-semibold w-20 text-right">$${(item.price * item.quantity).toFixed(2)}</span>
                <button onclick="removeFromCart('${item.id}')" class="text-red-600 hover:text-red-800">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
            </div>
        `;
        cartList.appendChild(cartItem);
    });
    
    const { subtotal, tax, total } = calculateTotals();
    
    document.getElementById('cart-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('cart-tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('cart-total').textContent = `$${total.toFixed(2)}`;
}

function proceedToCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    // Track begin checkout event
    const { total } = calculateTotals();
    const items = cart.map(item => ({
        item_id: item.id,
        item_name: item.name,
        category: 'Electronics',
        price: item.price,
        quantity: item.quantity
    }));
    
    trackBeginCheckout(items, total);
    
    window.location.href = 'checkout.html';
}

function displayCheckout() {
    const checkoutItems = document.getElementById('checkout-items');
    
    if (cart.length === 0) {
        checkoutItems.innerHTML = '<p class="text-gray-600">No items in cart</p>';
        return;
    }
    
    checkoutItems.innerHTML = '';
    
    cart.forEach(item => {
        const checkoutItem = document.createElement('div');
        checkoutItem.className = 'flex justify-between items-center';
        const imageMap = {
            'laptop-001': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=50&h=50&fit=crop&crop=center',
            'phone-001': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=50&h=50&fit=crop&crop=center',
            'watch-001': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=50&h=50&fit=crop&crop=center'
        };
        
        checkoutItem.innerHTML = `
            <div class="flex items-center space-x-3">
                <img src="${imageMap[item.id] || 'https://via.placeholder.com/50x50/007bff/ffffff?text=Product'}" alt="${item.name}" class="w-12 h-12 rounded object-cover">
                <div>
                    <h4 class="font-medium">${item.name}</h4>
                    <p class="text-sm text-gray-600">Qty: ${item.quantity}</p>
                </div>
            </div>
            <span class="font-semibold">$${(item.price * item.quantity).toFixed(2)}</span>
        `;
        checkoutItems.appendChild(checkoutItem);
    });
    
    const { subtotal, tax, total } = calculateTotals();
    
    document.getElementById('checkout-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('checkout-tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('checkout-total').textContent = `$${total.toFixed(2)}`;
}

function completeOrder() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    // Generate transaction ID
    const transactionId = 'T' + Date.now();
    
    // Prepare items for GA4
    const items = cart.map(item => ({
        item_id: item.id,
        item_name: item.name,
        category: 'Electronics',
        price: item.price,
        quantity: item.quantity
    }));
    
    const { total } = calculateTotals();
    
    // Track purchase event
    trackPurchase(transactionId, items, total);
    
    // Prepare order data for thank you page
    const orderData = {
        transactionId: transactionId,
        items: cart.map(item => ({
            name: item.name,
            price: item.price,
            quantity: item.quantity
        })),
        total: total
    };
    
    // Clear cart
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Show success message and redirect to thank you page
    showNotification('Order completed successfully!');
    
    setTimeout(() => {
        // Redirect to thank you page with order data
        const orderParam = encodeURIComponent(JSON.stringify(orderData));
        window.location.href = `thank-you.html?order=${orderParam}`;
    }, 1500);
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}