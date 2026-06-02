<!-- import { useState, useEffect } from "react";

const products = [
  { id: 1, name: "Obsidian Ceramic Vase", price: 129, category: "Home", tag: "Bestseller", emoji: "🏺", desc: "Hand-thrown stoneware with matte obsidian glaze. Each piece is unique.", rating: 4.9, reviews: 214 },
  { id: 2, name: "Linen Cloud Throw", price: 89, category: "Home", tag: "New", emoji: "🧶", desc: "Belgian linen blend, 140×180cm. Naturally softens with every wash.", rating: 4.8, reviews: 178 },
  { id: 3, name: "Walnut Desk Organizer", price: 64, category: "Office", tag: null, emoji: "🪵", desc: "Solid black walnut with brass pin joints. Three compartments.", rating: 4.7, reviews: 99 },
  { id: 4, name: "Merino Wool Cap", price: 48, category: "Apparel", tag: "Limited", emoji: "🧢", desc: "Extra-fine 18.5 micron merino. Ribbed knit, unisex fit.", rating: 4.9, reviews: 302 },
  { id: 5, name: "Amber Glass Carafe", price: 56, category: "Home", tag: null, emoji: "🫙", desc: "Mouth-blown borosilicate glass, 1.2L. Leak-proof cork stopper.", rating: 4.6, reviews: 143 },
  { id: 6, name: "Brass Candle Snuffer", price: 32, category: "Home", tag: "New", emoji: "🕯️", desc: "Solid brass, lacquer-free patina. 28cm length.", rating: 4.8, reviews: 87 },
  { id: 7, name: "Leather Card Sleeve", price: 42, category: "Apparel", tag: null, emoji: "👛", desc: "Full-grain vegetable-tanned leather. Holds 4–6 cards.", rating: 4.9, reviews: 421 },
  { id: 8, name: "Concrete Planter Set", price: 74, category: "Home", tag: "Bestseller", emoji: "🪴", desc: "Set of 3 — small, medium, large. Drainage hole with bamboo tray.", rating: 4.7, reviews: 188 },
  { id: 9, name: "Linen Tote Bag", price: 38, category: "Apparel", tag: null, emoji: "👜", desc: "Stonewashed heavy linen. Reinforced base, natural rope handles.", rating: 4.8, reviews: 267 },
  { id: 10, name: "Cork Trivet Set", price: 28, category: "Home", tag: "Sale", emoji: "🍽️", desc: "Natural Portuguese cork. Set of 3 hexagons, 10/15/20cm.", rating: 4.5, reviews: 76 },
  { id: 11, name: "Minimalist Wall Clock", price: 95, category: "Office", tag: null, emoji: "🕐", desc: "Brushed aluminum face, silent quartz movement. 30cm diameter.", rating: 4.9, reviews: 156 },
  { id: 12, name: "Marble Rolling Pin", price: 67, category: "Home", tag: "Sale", emoji: "🍞", desc: "Solid white marble with wooden handles. Stays cool naturally.", rating: 4.7, reviews: 112 },
];

const categories = ["All", "Home", "Apparel", "Office"];

const tagColors = {
  "Bestseller": { bg: "#2D2D2D", text: "#F5F0E8" },
  "New": { bg: "#C4A882", text: "#1A1410" },
  "Limited": { bg: "#8B3A3A", text: "#FBF0EE" },
  "Sale": { bg: "#3A6B4A", text: "#EBF5EE" },
};

function StarRating({ rating }) {
  return (
    <span style={{ color: "#C4A882", fontSize: 13, letterSpacing: 1 }}>
      {"★".repeat(Math.round(rating))}{"☆".repeat(5 - Math.round(rating))}
      <span style={{ color: "#888", marginLeft: 6, fontFamily: "'EB Garamond', serif", fontSize: 13 }}>{rating}</span>
    </span>
  );
}

function Toast({ msg, onClose }) {
  useEffect(() => { const t = setTimeout(onClose, 2200); return () => clearTimeout(t); }, []);
  return (
    <div style={{
      position: "fixed", bottom: 32, left: "50%", transform: "translateX(-50%)",
      background: "#1A1410", color: "#F5F0E8", padding: "14px 28px",
      borderRadius: 2, fontSize: 14, letterSpacing: "0.04em",
      fontFamily: "'EB Garamond', serif", zIndex: 1000,
      boxShadow: "0 8px 32px rgba(0,0,0,0.28)", border: "1px solid #3A3228",
      animation: "fadeUp 0.3s ease"
    }}>
      {msg}
    </div>
  );
}

function ProductCard({ p, onAddToCart, onView }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: "#FDFAF6",
        border: "1px solid #E8E0D4",
        borderRadius: 2,
        overflow: "hidden",
        cursor: "pointer",
        transition: "box-shadow 0.25s, transform 0.2s",
        transform: hovered ? "translateY(-4px)" : "none",
        boxShadow: hovered ? "0 16px 40px rgba(60,40,20,0.12)" : "0 2px 8px rgba(60,40,20,0.04)",
      }}
    >
      <div
        onClick={() => onView(p)}
        style={{
          height: 200, background: "#F0E8DC",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 72, position: "relative", overflow: "hidden",
          transition: "background 0.3s",
          backgroundImage: hovered ? "radial-gradient(circle at 60% 40%, #E8DCCF 0%, #F0E8DC 60%)" : "none"
        }}
      >
        <span style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.15))", transition: "transform 0.3s", transform: hovered ? "scale(1.12)" : "scale(1)" }}>
          {p.emoji}
        </span>
        {p.tag && (
          <span style={{
            position: "absolute", top: 12, left: 12,
            background: tagColors[p.tag].bg, color: tagColors[p.tag].text,
            fontSize: 10, letterSpacing: "0.1em", padding: "4px 10px",
            fontFamily: "'EB Garamond', serif", textTransform: "uppercase",
            borderRadius: 1,
          }}>{p.tag}</span>
        )}
      </div>
      <div style={{ padding: "18px 20px 20px" }}>
        <div style={{ fontSize: 11, color: "#B8A898", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: 6, fontFamily: "'EB Garamond', serif" }}>
          {p.category}
        </div>
        <div onClick={() => onView(p)} style={{ fontFamily: "'EB Garamond', serif", fontSize: 18, color: "#1A1410", lineHeight: 1.3, marginBottom: 6, fontWeight: 500 }}>
          {p.name}
        </div>
        <StarRating rating={p.rating} />
        <div style={{ color: "#888", fontSize: 12, marginLeft: 2, display: "inline", fontFamily: "'EB Garamond', serif" }}> ({p.reviews})</div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 16 }}>
          <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 20, color: "#1A1410", fontWeight: 600 }}>
            ${p.price}
          </span>
          <button
            onClick={(e) => { e.stopPropagation(); onAddToCart(p); }}
            style={{
              background: hovered ? "#1A1410" : "transparent",
              color: hovered ? "#F5F0E8" : "#1A1410",
              border: "1px solid #1A1410",
              padding: "8px 18px",
              fontSize: 12, letterSpacing: "0.08em",
              fontFamily: "'EB Garamond', serif",
              cursor: "pointer", borderRadius: 1,
              transition: "all 0.2s",
              textTransform: "uppercase",
            }}
          >
            Add to cart
          </button>
        </div>
      </div>
    </div>
  );
}

function CartDrawer({ cart, onClose, onRemove, onCheckout }) {
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 500 }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(20,14,8,0.45)" }} />
      <div style={{
        position: "absolute", right: 0, top: 0, bottom: 0, width: 400,
        background: "#FDFAF6", display: "flex", flexDirection: "column",
        borderLeft: "1px solid #E8E0D4",
      }}>
        <div style={{ padding: "28px 28px 20px", borderBottom: "1px solid #E8E0D4", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ fontFamily: "'EB Garamond', serif", fontSize: 24, color: "#1A1410", fontWeight: 500 }}>Your Cart</div>
            <div style={{ color: "#B8A898", fontSize: 13, fontFamily: "'EB Garamond', serif", marginTop: 2 }}>{cart.length} {cart.length === 1 ? "item" : "items"}</div>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 24, color: "#888", lineHeight: 1 }}>×</button>
        </div>
        <div style={{ flex: 1, overflowY: "auto", padding: "20px 28px" }}>
          {cart.length === 0 && (
            <div style={{ textAlign: "center", padding: "60px 0", color: "#C0B8AE", fontFamily: "'EB Garamond', serif", fontSize: 18 }}>
              <div style={{ fontSize: 48, marginBottom: 16 }}>🛒</div>
              Your cart is empty
            </div>
          )}
          {cart.map(item => (
            <div key={item.id} style={{ display: "flex", gap: 16, marginBottom: 20, paddingBottom: 20, borderBottom: "1px solid #F0E8DC" }}>
              <div style={{ width: 64, height: 64, background: "#F0E8DC", borderRadius: 2, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 28, flexShrink: 0 }}>
                {item.emoji}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: "'EB Garamond', serif", fontSize: 16, color: "#1A1410", fontWeight: 500 }}>{item.name}</div>
                <div style={{ color: "#888", fontSize: 13, fontFamily: "'EB Garamond', serif", marginTop: 2 }}>Qty: {item.qty}</div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 6 }}>
                  <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 16, color: "#1A1410", fontWeight: 600 }}>${item.price * item.qty}</span>
                  <button onClick={() => onRemove(item.id)} style={{ background: "none", border: "none", color: "#C0A898", cursor: "pointer", fontSize: 12, letterSpacing: "0.08em", fontFamily: "'EB Garamond', serif", textDecoration: "underline" }}>Remove</button>
                </div>
              </div>
            </div>
          ))}
        </div>
        {cart.length > 0 && (
          <div style={{ padding: "20px 28px 28px", borderTop: "1px solid #E8E0D4" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span style={{ fontFamily: "'EB Garamond', serif", color: "#888", fontSize: 14 }}>Subtotal</span>
              <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 14, color: "#1A1410" }}>${total}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
              <span style={{ fontFamily: "'EB Garamond', serif", color: "#888", fontSize: 14 }}>Shipping</span>
              <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 14, color: "#3A6B4A" }}>{total > 100 ? "Free" : "$9.90"}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 24, paddingTop: 16, borderTop: "1px solid #E8E0D4" }}>
              <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 18, color: "#1A1410", fontWeight: 600 }}>Total</span>
              <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 20, color: "#1A1410", fontWeight: 600 }}>${total > 100 ? total : total + 9.9}</span>
            </div>
            {total > 100 && (
              <div style={{ background: "#EBF5EE", border: "1px solid #B8D8C0", borderRadius: 2, padding: "8px 14px", marginBottom: 18, fontSize: 13, color: "#3A6B4A", fontFamily: "'EB Garamond', serif" }}>
                🎉 You qualify for free shipping!
              </div>
            )}
            <button
              onClick={onCheckout}
              style={{
                width: "100%", background: "#1A1410", color: "#F5F0E8",
                border: "none", padding: "16px", cursor: "pointer",
                fontFamily: "'EB Garamond', serif", fontSize: 15,
                letterSpacing: "0.1em", textTransform: "uppercase",
                borderRadius: 2, transition: "background 0.2s",
              }}
            >
              Proceed to Checkout
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function ProductModal({ product, onClose, onAddToCart }) {
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 600, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(20,14,8,0.55)" }} />
      <div style={{
        position: "relative", background: "#FDFAF6", width: "min(700px, 94vw)",
        borderRadius: 2, overflow: "hidden", display: "flex", flexDirection: "row",
        maxHeight: "85vh", border: "1px solid #E0D8CC",
      }}>
        <div style={{ width: "45%", background: "#F0E8DC", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 100 }}>
          {product.emoji}
        </div>
        <div style={{ flex: 1, padding: "36px 32px 32px", overflowY: "auto" }}>
          <button onClick={onClose} style={{ position: "absolute", top: 16, right: 16, background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#888" }}>×</button>
          {product.tag && (
            <div style={{ display: "inline-block", background: tagColors[product.tag].bg, color: tagColors[product.tag].text, fontSize: 10, letterSpacing: "0.1em", padding: "4px 10px", fontFamily: "'EB Garamond', serif", textTransform: "uppercase", borderRadius: 1, marginBottom: 14 }}>
              {product.tag}
            </div>
          )}
          <div style={{ fontSize: 11, color: "#B8A898", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: 8, fontFamily: "'EB Garamond', serif" }}>{product.category}</div>
          <h2 style={{ fontFamily: "'EB Garamond', serif", fontSize: 28, color: "#1A1410", fontWeight: 500, lineHeight: 1.25, marginBottom: 12 }}>{product.name}</h2>
          <div style={{ marginBottom: 12 }}>
            <StarRating rating={product.rating} />
            <span style={{ color: "#888", fontSize: 13, marginLeft: 8, fontFamily: "'EB Garamond', serif" }}>{product.reviews} reviews</span>
          </div>
          <p style={{ color: "#5A4E44", fontFamily: "'EB Garamond', serif", fontSize: 16, lineHeight: 1.7, marginBottom: 24 }}>{product.desc}</p>
          <div style={{ borderTop: "1px solid #E8E0D4", paddingTop: 20, marginBottom: 24 }}>
            {["Materials", "Shipping", "Returns"].map((label, i) => (
              <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #F0E8DC" }}>
                <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 13, color: "#888" }}>{label}</span>
                <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 13, color: "#5A4E44" }}>
                  {["Natural & sustainable", "Free over $100", "30-day returns"][i]}
                </span>
              </div>
            ))}
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <span style={{ fontFamily: "'EB Garamond', serif", fontSize: 28, color: "#1A1410", fontWeight: 600 }}>${product.price}</span>
            <button
              onClick={() => { onAddToCart(product); onClose(); }}
              style={{
                flex: 1, background: "#1A1410", color: "#F5F0E8",
                border: "none", padding: "14px", cursor: "pointer",
                fontFamily: "'EB Garamond', serif", fontSize: 14,
                letterSpacing: "0.1em", textTransform: "uppercase",
                borderRadius: 2,
              }}
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [cart, setCart] = useState([]);
  const [cartOpen, setCartOpen] = useState(false);
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("default");
  const [toast, setToast] = useState(null);
  const [viewProduct, setViewProduct] = useState(null);
  const [wishlist, setWishlist] = useState([]);
  const [page, setPage] = useState("shop");

  const cartCount = cart.reduce((s, i) => s + i.qty, 0);

  const addToCart = (p) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === p.id);
      if (existing) return prev.map(i => i.id === p.id ? { ...i, qty: i.qty + 1 } : i);
      return [...prev, { ...p, qty: 1 }];
    });
    setToast(`${p.name} added to cart`);
  };

  const removeFromCart = (id) => setCart(prev => prev.filter(i => i.id !== id));

  const toggleWishlist = (id) => setWishlist(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);

  let filtered = products.filter(p =>
    (category === "All" || p.category === category) &&
    p.name.toLowerCase().includes(search.toLowerCase())
  );
  if (sort === "price-asc") filtered = [...filtered].sort((a, b) => a.price - b.price);
  if (sort === "price-desc") filtered = [...filtered].sort((a, b) => b.price - a.price);
  if (sort === "rating") filtered = [...filtered].sort((a, b) => b.rating - a.rating);

  return (
    <div style={{ minHeight: "100vh", background: "#FAF7F2", fontFamily: "'EB Garamond', serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap');
        @keyframes fadeUp { from { opacity:0; transform: translateX(-50%) translateY(12px); } to { opacity:1; transform: translateX(-50%) translateY(0); } }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-track { background: #F0E8DC; } ::-webkit-scrollbar-thumb { background: #C4A882; border-radius: 2px; }
        input[type=text], select { font-family: 'EB Garamond', serif; }
      `}</style>

      {/* Nav */}
      <nav style={{ background: "#1A1410", position: "sticky", top: 0, zIndex: 100, borderBottom: "1px solid #2D2520" }}>
        <div style={{ maxWidth: 1240, margin: "0 auto", padding: "0 32px", display: "flex", alignItems: "center", height: 64 }}>
          <div onClick={() => setPage("shop")} style={{ fontFamily: "'EB Garamond', serif", fontSize: 22, color: "#F5F0E8", fontWeight: 500, letterSpacing: "0.06em", cursor: "pointer", flex: 1 }}>
            ARTISANAL
          </div>
          <div style={{ display: "flex", gap: 32, marginRight: 32 }}>
            {["Shop", "About", "Journal"].map(n => (
              <span key={n} onClick={() => setPage(n.toLowerCase())} style={{ color: page === n.toLowerCase() ? "#C4A882" : "#B8A898", fontSize: 14, letterSpacing: "0.08em", cursor: "pointer", textTransform: "uppercase", transition: "color 0.2s" }}>
                {n}
              </span>
            ))}
          </div>
          <button onClick={() => setCartOpen(true)} style={{ background: "none", border: "1px solid #3A3228", color: "#F5F0E8", padding: "8px 18px", cursor: "pointer", fontFamily: "'EB Garamond', serif", fontSize: 14, letterSpacing: "0.06em", borderRadius: 1, display: "flex", alignItems: "center", gap: 8 }}>
            Cart
            {cartCount > 0 && <span style={{ background: "#C4A882", color: "#1A1410", borderRadius: "50%", width: 20, height: 20, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 600 }}>{cartCount}</span>}
          </button>
        </div>
      </nav>

      {page === "shop" && (
        <>
          {/* Hero */}
          <div style={{ background: "linear-gradient(135deg, #1A1410 0%, #2D2018 50%, #3A2A1C 100%)", padding: "80px 32px", textAlign: "center", position: "relative", overflow: "hidden" }}>
            <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%,-50%)", width: 600, height: 600, background: "radial-gradient(circle, rgba(196,168,130,0.08) 0%, transparent 70%)", borderRadius: "50%", pointerEvents: "none" }} />
            <div style={{ fontSize: 11, color: "#C4A882", letterSpacing: "0.2em", textTransform: "uppercase", marginBottom: 24 }}>Curated Objects for Thoughtful Living</div>
            <h1 style={{ fontFamily: "'EB Garamond', serif", fontSize: "clamp(42px, 6vw, 72px)", color: "#F5F0E8", fontWeight: 400, lineHeight: 1.1, marginBottom: 24, maxWidth: 700, margin: "0 auto 24px" }}>
              Craft &<br /><em style={{ color: "#C4A882" }}>Character</em>
            </h1>
            <p style={{ color: "#B8A898", fontSize: 18, maxWidth: 480, margin: "0 auto 36px", lineHeight: 1.7 }}>
              Each piece tells a story of its maker. Honest materials, enduring form.
            </p>
            <button onClick={() => document.getElementById("products-section").scrollIntoView({ behavior: "smooth" })} style={{ background: "#C4A882", color: "#1A1410", border: "none", padding: "14px 36px", cursor: "pointer", fontFamily: "'EB Garamond', serif", fontSize: 15, letterSpacing: "0.1em", textTransform: "uppercase", borderRadius: 1 }}>
              Explore Collection
            </button>
          </div>

          {/* Category Pills + Search + Sort */}
          <div id="products-section" style={{ maxWidth: 1240, margin: "0 auto", padding: "40px 32px 0" }}>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center", marginBottom: 28 }}>
              {categories.map(c => (
                <button key={c} onClick={() => setCategory(c)} style={{
                  background: category === c ? "#1A1410" : "transparent",
                  color: category === c ? "#F5F0E8" : "#888",
                  border: `1px solid ${category === c ? "#1A1410" : "#D8CEC4"}`,
                  padding: "8px 20px", cursor: "pointer",
                  fontFamily: "'EB Garamond', serif", fontSize: 14,
                  letterSpacing: "0.06em", borderRadius: 1, transition: "all 0.2s",
                }}>{c}</button>
              ))}
              <div style={{ flex: 1 }} />
              <input
                type="text"
                placeholder="Search products…"
                value={search}
                onChange={e => setSearch(e.target.value)}
                style={{ border: "1px solid #D8CEC4", background: "#FDFAF6", padding: "8px 16px", fontFamily: "'EB Garamond', serif", fontSize: 14, color: "#1A1410", outline: "none", borderRadius: 1, width: 220 }}
              />
              <select value={sort} onChange={e => setSort(e.target.value)} style={{ border: "1px solid #D8CEC4", background: "#FDFAF6", padding: "8px 14px", fontFamily: "'EB Garamond', serif", fontSize: 14, color: "#1A1410", outline: "none", borderRadius: 1, cursor: "pointer" }}>
                <option value="default">Sort: Featured</option>
                <option value="price-asc">Price: Low–High</option>
                <option value="price-desc">Price: High–Low</option>
                <option value="rating">Top Rated</option>
              </select>
            </div>
            <div style={{ color: "#B8A898", fontSize: 13, marginBottom: 24, fontFamily: "'EB Garamond', serif" }}>
              {filtered.length} {filtered.length === 1 ? "product" : "products"}
            </div>
          </div>

          {/* Products Grid */}
          <div style={{ maxWidth: 1240, margin: "0 auto", padding: "0 32px 80px" }}>
            {filtered.length === 0 ? (
              <div style={{ textAlign: "center", padding: "80px 0", color: "#C0B8AE", fontFamily: "'EB Garamond', serif", fontSize: 20 }}>
                No products found. Try a different search.
              </div>
            ) : (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 24 }}>
                {filtered.map(p => (
                  <ProductCard key={p.id} p={p} onAddToCart={addToCart} onView={setViewProduct} />
                ))}
              </div>
            )}
          </div>

          {/* Banner */}
          <div style={{ background: "#F0E8DC", borderTop: "1px solid #E0D4C4", borderBottom: "1px solid #E0D4C4", padding: "48px 32px", textAlign: "center" }}>
            <div style={{ maxWidth: 600, margin: "0 auto" }}>
              <div style={{ fontSize: 11, color: "#C4A882", letterSpacing: "0.18em", textTransform: "uppercase", marginBottom: 12 }}>Free Shipping</div>
              <h3 style={{ fontFamily: "'EB Garamond', serif", fontSize: 28, color: "#1A1410", fontWeight: 400, marginBottom: 12 }}>On all orders over $100</h3>
              <p style={{ color: "#7A6E64", fontSize: 16, lineHeight: 1.7 }}>Carefully packaged with recycled materials. Delivered in 3–5 business days.</p>
            </div>
          </div>
        </>
      )}

      {page === "about" && (
        <div style={{ maxWidth: 780, margin: "80px auto", padding: "0 32px" }}>
          <div style={{ fontSize: 11, color: "#C4A882", letterSpacing: "0.18em", textTransform: "uppercase", marginBottom: 16 }}>Our Story</div>
          <h1 style={{ fontFamily: "'EB Garamond', serif", fontSize: 48, color: "#1A1410", fontWeight: 400, lineHeight: 1.2, marginBottom: 32 }}>Made to Last,<br />Meant to Be Used</h1>
          <p style={{ color: "#5A4E44", fontSize: 18, lineHeight: 1.8, marginBottom: 24 }}>
            ARTISANAL was founded on the belief that everyday objects should bring genuine pleasure. We seek out makers who still use their hands — ceramicists, weavers, woodworkers — and work with them to bring their craft to more homes.
          </p>
          <p style={{ color: "#5A4E44", fontSize: 18, lineHeight: 1.8, marginBottom: 24 }}>
            Every piece in our collection is made to endure. We favour natural materials, honest construction, and designs that resist trend. A well-made object is a small act of resistance against disposability.
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 24, marginTop: 48 }}>
            {[["🌿", "Sustainable", "Natural materials, minimal packaging"], ["🤝", "Fair Trade", "Makers paid fairly, always"], ["♻️", "No Waste", "Zero-waste packaging policy"]].map(([emoji, title, desc]) => (
              <div key={title} style={{ background: "#F0E8DC", borderRadius: 2, padding: "28px 24px", textAlign: "center" }}>
                <div style={{ fontSize: 32, marginBottom: 12 }}>{emoji}</div>
                <div style={{ fontFamily: "'EB Garamond', serif", fontSize: 18, color: "#1A1410", fontWeight: 500, marginBottom: 8 }}>{title}</div>
                <div style={{ color: "#7A6E64", fontSize: 14, lineHeight: 1.6 }}>{desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {page === "journal" && (
        <div style={{ maxWidth: 900, margin: "80px auto", padding: "0 32px 80px" }}>
          <div style={{ fontSize: 11, color: "#C4A882", letterSpacing: "0.18em", textTransform: "uppercase", marginBottom: 16 }}>Journal</div>
          <h1 style={{ fontFamily: "'EB Garamond', serif", fontSize: 48, color: "#1A1410", fontWeight: 400, marginBottom: 48 }}>Notes on Craft</h1>
          {[
            { emoji: "🏺", title: "The Art of Imperfection", cat: "Ceramics", date: "May 2025", excerpt: "Why wabi-sabi thinking transforms the way we value handmade objects — and why every slight variation is a feature, not a flaw." },
            { emoji: "🧶", title: "A Short History of Linen", cat: "Textiles", date: "Apr 2025", excerpt: "From ancient Egypt to Belgian farmhouses — how one of the world's oldest fibres became synonymous with understated luxury." },
            { emoji: "🪵", title: "Working with Grain", cat: "Woodwork", date: "Mar 2025", excerpt: "Master woodworker Elias Brandt on reading the grain, the smell of walnut shavings, and why he refuses to use power sanders." },
          ].map(post => (
            <div key={post.title} style={{ display: "flex", gap: 32, marginBottom: 48, paddingBottom: 48, borderBottom: "1px solid #E8E0D4" }}>
              <div style={{ width: 120, height: 120, background: "#F0E8DC", borderRadius: 2, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 52, flexShrink: 0 }}>
                {post.emoji}
              </div>
              <div>
                <div style={{ fontSize: 11, color: "#C4A882", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: 8 }}>{post.cat} · {post.date}</div>
                <h2 style={{ fontFamily: "'EB Garamond', serif", fontSize: 26, color: "#1A1410", fontWeight: 500, marginBottom: 12, lineHeight: 1.25 }}>{post.title}</h2>
                <p style={{ color: "#7A6E64", fontSize: 16, lineHeight: 1.7 }}>{post.excerpt}</p>
                <button style={{ background: "none", border: "none", color: "#C4A882", cursor: "pointer", fontSize: 14, fontFamily: "'EB Garamond', serif", letterSpacing: "0.06em", marginTop: 12, textDecoration: "underline" }}>Read more →</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Footer */}
      <footer style={{ background: "#1A1410", borderTop: "1px solid #2D2520", padding: "48px 32px 32px" }}>
        <div style={{ maxWidth: 1240, margin: "0 auto" }}>
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", gap: 40, marginBottom: 40 }}>
            <div>
              <div style={{ fontFamily: "'EB Garamond', serif", fontSize: 22, color: "#F5F0E8", fontWeight: 500, letterSpacing: "0.06em", marginBottom: 16 }}>ARTISANAL</div>
              <p style={{ color: "#7A6E64", fontSize: 14, lineHeight: 1.7, maxWidth: 280 }}>Thoughtfully curated objects for homes that value craft over convention.</p>
            </div>
            {[["Shop", ["All Products", "Home & Living", "Apparel", "Office"]], ["Company", ["About Us", "Journal", "Sustainability", "Careers"]], ["Support", ["Shipping", "Returns", "FAQ", "Contact"]]].map(([title, links]) => (
              <div key={title}>
                <div style={{ color: "#F5F0E8", fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: 16, fontFamily: "'EB Garamond', serif" }}>{title}</div>
                {links.map(l => <div key={l} style={{ color: "#7A6E64", fontSize: 14, marginBottom: 8, cursor: "pointer", fontFamily: "'EB Garamond', serif" }}>{l}</div>)}
              </div>
            ))}
          </div>
          <div style={{ borderTop: "1px solid #2D2520", paddingTop: 24, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ color: "#5A5048", fontSize: 12, fontFamily: "'EB Garamond', serif" }}>© 2025 Artisanal. All rights reserved.</div>
            <div style={{ color: "#5A5048", fontSize: 12, fontFamily: "'EB Garamond', serif" }}>Made with care · No algorithms · No ads</div>
          </div>
        </div>
      </footer>

      {cartOpen && <CartDrawer cart={cart} onClose={() => setCartOpen(false)} onRemove={removeFromCart} onCheckout={() => { setToast("Checkout coming soon!"); setCartOpen(false); }} />}
      {viewProduct && <ProductModal product={viewProduct} onClose={() => setViewProduct(null)} onAddToCart={addToCart} />}
      {toast && <Toast msg={toast} onClose={() => setToast(null)} />}
    </div>
  );
} -->