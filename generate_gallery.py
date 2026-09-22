import os
import json
from pathlib import Path

# Get list of images
img_dir = "processed_images"
images = sorted([f for f in os.listdir(img_dir) if f.startswith("Product_") and f.endswith(".jpg")])

# Extract product data
products = []
for img in images:
    parts = img.split('_', 2)
    if len(parts) >= 2:
        product_num = parts[1]
        products.append({
            "id": int(product_num),
            "number": product_num,
            "image": f"../processed_images/{img}"
        })

# Create gallery HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dance Shoes Gallery</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        .controls {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .controls input {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        .controls button {{
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        .controls button:hover {{
            background: #45a049;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }}
        .product {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .product:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .product input[type="checkbox"] {{
            position: absolute;
            top: 10px;
            left: 10px;
            width: 20px;
            height: 20px;
            cursor: pointer;
            z-index: 10;
        }}
        .product.selected {{
            border: 3px solid #4CAF50;
        }}
        .product-img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        .product-info {{
            padding: 15px;
            text-align: center;
        }}
        .product-number {{
            font-weight: bold;
            color: #333;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dance Shoes Gallery</h1>
            <p>Total Products: {len(products)}</p>
        </div>
        
        <div class="controls">
            <input type="text" id="searchInput" placeholder="Search by product number...">
            <button onclick="selectAll()">Select All</button>
            <button onclick="deselectAll()">Deselect All</button>
            <button onclick="generateList()">Generate List</button>
            <button onclick="exportJSON()">Export JSON</button>
        </div>
        
        <div class="gallery" id="gallery"></div>
    </div>

    <script>
        const products = {json.dumps(products)};
        
        function renderGallery(productsToShow = products) {{
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = '';
            
            productsToShow.forEach(product => {{
                const div = document.createElement('div');
                div.className = 'product';
                div.innerHTML = `
                    <input type="checkbox" class="product-checkbox" value="${{product.id}}" data-number="${{product.number}}">
                    <img src="${{product.image}}" alt="Product ${{product.number}}" class="product-img">
                    <div class="product-info">
                        <div class="product-number">Product ${{product.number}}</div>
                    </div>
                `;
                
                const checkbox = div.querySelector('input[type="checkbox"]');
                checkbox.addEventListener('change', () => {{
                    if (checkbox.checked) {{
                        div.classList.add('selected');
                    }} else {{
                        div.classList.remove('selected');
                    }}
                }});
                
                gallery.appendChild(div);
            }});
        }}
        
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.trim();
            if (query === '') {{
                renderGallery(products);
            }} else {{
                const filtered = products.filter(p => p.number.includes(query));
                renderGallery(filtered);
            }}
        }});
        
        function selectAll() {{
            document.querySelectorAll('.product-checkbox').forEach(cb => {{
                cb.checked = true;
                cb.closest('.product').classList.add('selected');
            }});
        }}
        
        function deselectAll() {{
            document.querySelectorAll('.product-checkbox').forEach(cb => {{
                cb.checked = false;
                cb.closest('.product').classList.remove('selected');
            }});
        }}
        
        function generateList() {{
            const selected = document.querySelectorAll('.product-checkbox:checked');
            if (selected.length === 0) {{
                alert('Please select at least one product');
                return;
            }}
            
            const numbers = Array.from(selected).map(cb => cb.dataset.number).sort((a, b) => parseInt(a) - parseInt(b));
            const timestamp = new Date().toLocaleString();
            const list = `Generated on: ${{timestamp}}\nSelected Products (${{numbers.length}}):\n\n${{numbers.join(', ')}}`;
            
            alert(list);
        }}
        
        function exportJSON() {{
            const selected = document.querySelectorAll('.product-checkbox:checked');
            const selectedProducts = products.filter(p => 
                Array.from(selected).some(cb => cb.value == p.id)
            );
            
            const data = {{
                timestamp: new Date().toISOString(),
                totalCount: selectedProducts.length,
                products: selectedProducts
            }};
            
            const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'selected_products.json';
            a.click();
        }}
        
        renderGallery();
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Gallery generated with {len(products)} products")
