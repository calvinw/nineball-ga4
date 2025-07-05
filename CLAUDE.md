# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a complete ecommerce demo site for Google Analytics 4 (GA4) practice. The project contains a multi-page shopping website with comprehensive GA4 enhanced ecommerce tracking.

## Architecture
- **Static ecommerce website**: Multi-page HTML site with Tailwind CSS styling
- **Google Analytics 4 Integration**: Uses gtag.js with tracking ID G-RN4WWVXY5S
- **Enhanced Ecommerce Tracking**: Tracks all major ecommerce events
- **Client-side cart management**: Uses localStorage for cart persistence

## Key Files
- `index.html`: Homepage with featured products
- `products.html`: Product catalog page
- `product-laptop.html`, `product-phone.html`, `product-watch.html`: Individual product pages
- `cart.html`: Shopping cart page
- `checkout.html`: Checkout form page
- `script.js`: All JavaScript functionality including GA4 tracking
- `README.md`: Basic project description

## Products
The demo includes 3 fake products:
- Premium Laptop ($999.99) - SKU: laptop-001
- Smartphone Pro ($699.99) - SKU: phone-001  
- Smart Watch ($299.99) - SKU: watch-001

## Development
Since this is a static HTML site, no build process is required. Simply open any HTML file in a browser or serve with a local web server to test GA4 tracking functionality.

## GA4 Enhanced Ecommerce Implementation
The site tracks all major ecommerce events:
- `page_view`: Automatic page tracking
- `view_item`: When viewing product details
- `add_to_cart`: When adding items to cart
- `begin_checkout`: When starting checkout process
- `purchase`: When completing an order
- Custom events for user interactions

## Testing GA4 Analytics
To test the GA4 implementation:
1. Open the site in a browser
2. Navigate through pages, view products, add to cart, and complete checkout
3. Check GA4 Real-time reports to see events being tracked
4. Use GA4 DebugView for detailed event inspection