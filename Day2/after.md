<!-- Here's a comprehensive, production-ready e-commerce plan. I've made the following stack decisions:

**Stack confirmed:**
- Frontend: React + TypeScript (Vite) — type safety pays off immediately in e-commerce with complex cart/order state
- Backend: Node.js/Express + TypeScript, REST API, PostgreSQL (relational integrity for orders/inventory)
- Payments: Stripe in test mode
- Deployment: Vercel (frontend) + Railway (backend + Postgres) — zero-config CI/CD via GitHub
- MVP features: product catalog + search/filters, product detail page, cart, checkout with Stripe, user auth (JWT), order history

Let's start with the architecture overview, then dive into all deliverables.Now the full plan — phased deliverables, database schema, API contracts, and code snippets.

---

## Phase 1 — MVP (weeks 1–4)

### Project structure

```
shopify-clone/
├── apps/
│   ├── web/                        # React + TypeScript (Vite)
│   │   ├── src/
│   │   │   ├── components/         # Shared UI (Button, Input, Badge…)
│   │   │   ├── features/           # Collocated feature modules
│   │   │   │   ├── catalog/        # ProductGrid, ProductCard, Filters
│   │   │   │   ├── cart/           # CartDrawer, CartItem, useCart
│   │   │   │   ├── checkout/       # CheckoutForm, PaymentStep
│   │   │   │   ├── auth/           # LoginForm, RegisterForm
│   │   │   │   └── orders/         # OrderHistory, OrderDetail
│   │   │   ├── hooks/              # useDebounce, useLocalStorage…
│   │   │   ├── lib/                # api.ts (typed fetch wrapper)
│   │   │   ├── store/              # Zustand slices (cart, auth)
│   │   │   └── App.tsx
│   └── api/                        # Express + TypeScript
│       ├── src/
│       │   ├── routes/             # products, orders, users, auth, webhooks
│       │   ├── middleware/         # auth, validation, rateLimiter, errorHandler
│       │   ├── services/           # ProductService, OrderService, StripeService
│       │   ├── db/                 # Prisma schema + migrations
│       │   └── index.ts
├── packages/
│   └── shared-types/               # Shared TS types (Product, Order, User…)
└── .github/workflows/ci.yml
```

Monorepo managed with **pnpm workspaces**. `shared-types` eliminates frontend/backend drift on data shapes.

---

### Database schema

```sql
-- Users
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name        TEXT NOT NULL,
  role        TEXT NOT NULL DEFAULT 'customer',  -- 'customer' | 'admin'
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Products
CREATE TABLE products (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  slug        TEXT UNIQUE NOT NULL,
  description TEXT,
  price_cents INT NOT NULL,           -- store money as integer cents
  stock       INT NOT NULL DEFAULT 0,
  category    TEXT NOT NULL,
  images      TEXT[] NOT NULL DEFAULT '{}',
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_name_trgm ON products USING GIN(name gin_trgm_ops); -- fuzzy search

-- Orders
CREATE TABLE orders (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID NOT NULL REFERENCES users(id),
  status           TEXT NOT NULL DEFAULT 'pending', -- pending|paid|shipped|delivered|cancelled
  total_cents      INT NOT NULL,
  stripe_payment_intent_id TEXT UNIQUE,
  shipping_address JSONB NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Order line items
CREATE TABLE order_items (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id  UUID NOT NULL REFERENCES products(id),
  quantity    INT NOT NULL CHECK (quantity > 0),
  price_cents INT NOT NULL   -- snapshot price at time of order
);

-- Reviews
CREATE TABLE reviews (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id  UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES users(id),
  rating      INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  body        TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(product_id, user_id)  -- one review per user per product
);
```

Use **Prisma** as the ORM — schema is defined in `prisma/schema.prisma` and migrations are auto-generated.

---

### API contracts

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Returns JWT |
| GET | `/products` | — | List with `?search=&category=&minPrice=&maxPrice=&page=&limit=` |
| GET | `/products/:slug` | — | Product detail + avg rating |
| POST | `/products` | Admin | Create product |
| PATCH | `/products/:id` | Admin | Update product |
| GET | `/orders` | User | Order history |
| POST | `/orders` | User | Create order + Stripe PaymentIntent |
| GET | `/orders/:id` | User | Order detail |
| POST | `/webhooks/stripe` | Stripe sig | Handle `payment_intent.succeeded` |
| POST | `/reviews` | User | Submit review |
| GET | `/products/:id/reviews` | — | Paginated reviews |

All endpoints return `{ data, meta? }` on success and `{ error: { code, message } }` on failure. Pagination meta: `{ page, limit, total, totalPages }`.

---

### Core code snippets

#### 1. Typed API client (frontend)

```typescript
// apps/web/src/lib/api.ts
const BASE = import.meta.env.VITE_API_URL;

async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const token = localStorage.getItem('token');
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error?.message ?? 'Request failed');
  }
  return res.json().then((r) => r.data);
}

export const api = {
  get:    <T>(path: string) => request<T>(path),
  post:   <T>(path: string, body: unknown) =>
            request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
  patch:  <T>(path: string, body: unknown) =>
            request<T>(path, { method: 'PATCH', body: JSON.stringify(body) }),
};
```

#### 2. Product listing with search & filters

```typescript
// apps/api/src/routes/products.ts
import { Router } from 'express';
import { prisma } from '../db/client';

export const productsRouter = Router();

productsRouter.get('/', async (req, res) => {
  const { search, category, minPrice, maxPrice, page = 1, limit = 20 } = req.query;

  const where = {
    isActive: true,
    ...(search && { name: { contains: String(search), mode: 'insensitive' } }),
    ...(category && { category: String(category) }),
    priceCents: {
      ...(minPrice && { gte: Number(minPrice) * 100 }),
      ...(maxPrice && { lte: Number(maxPrice) * 100 }),
    },
  };

  const [products, total] = await Promise.all([
    prisma.product.findMany({
      where,
      skip: (Number(page) - 1) * Number(limit),
      take: Number(limit),
      orderBy: { createdAt: 'desc' },
    }),
    prisma.product.count({ where }),
  ]);

  res.json({
    data: products,
    meta: { page: Number(page), limit: Number(limit), total, totalPages: Math.ceil(total / Number(limit)) },
  });
});
```

#### 3. Cart state with Zustand

```typescript
// apps/web/src/store/cartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Product } from '@shop/shared-types';

interface CartItem { product: Product; quantity: number }
interface CartState {
  items: CartItem[];
  add: (product: Product) => void;
  remove: (productId: string) => void;
  updateQty: (productId: string, qty: number) => void;
  clear: () => void;
  totalCents: () => number;
}

export const useCart = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      add: (product) =>
        set((s) => {
          const existing = s.items.find((i) => i.product.id === product.id);
          return existing
            ? { items: s.items.map((i) => i.product.id === product.id
                ? { ...i, quantity: i.quantity + 1 } : i) }
            : { items: [...s.items, { product, quantity: 1 }] };
        }),
      remove: (id) => set((s) => ({ items: s.items.filter((i) => i.product.id !== id) })),
      updateQty: (id, qty) =>
        set((s) => ({
          items: qty <= 0
            ? s.items.filter((i) => i.product.id !== id)
            : s.items.map((i) => i.product.id === id ? { ...i, quantity: qty } : i),
        })),
      clear: () => set({ items: [] }),
      totalCents: () => get().items.reduce((sum, i) => sum + i.product.priceCents * i.quantity, 0),
    }),
    { name: 'cart' }  // persists to localStorage
  )
);
```

#### 4. Checkout — create order + Stripe PaymentIntent

```typescript
// apps/api/src/routes/orders.ts (POST /)
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

ordersRouter.post('/', requireAuth, async (req, res) => {
  const { items, shippingAddress } = req.body;
  const userId = req.user.id;

  // 1. Fetch live prices from DB (never trust client-sent prices)
  const productIds = items.map((i: any) => i.productId);
  const products = await prisma.product.findMany({ where: { id: { in: productIds } } });
  const productMap = new Map(products.map((p) => [p.id, p]));

  const totalCents = items.reduce((sum: number, item: any) => {
    const product = productMap.get(item.productId);
    if (!product) throw new Error(`Product ${item.productId} not found`);
    return sum + product.priceCents * item.quantity;
  }, 0);

  // 2. Create Stripe PaymentIntent
  const paymentIntent = await stripe.paymentIntents.create({
    amount: totalCents,
    currency: 'usd',
    metadata: { userId },
  });

  // 3. Create order record (status: 'pending' until webhook confirms)
  const order = await prisma.order.create({
    data: {
      userId,
      totalCents,
      status: 'pending',
      stripePaymentIntentId: paymentIntent.id,
      shippingAddress,
      items: {
        create: items.map((i: any) => ({
          productId: i.productId,
          quantity: i.quantity,
          priceCents: productMap.get(i.productId)!.priceCents,
        })),
      },
    },
    include: { items: true },
  });

  res.json({ data: { order, clientSecret: paymentIntent.client_secret } });
});
```

#### 5. Stripe webhook — confirm payment

```typescript
// apps/api/src/routes/webhooks.ts
webhooksRouter.post('/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature']!;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return res.status(400).send('Webhook signature verification failed');
  }

  if (event.type === 'payment_intent.succeeded') {
    const pi = event.data.object as Stripe.PaymentIntent;
    await prisma.order.updateMany({
      where: { stripePaymentIntentId: pi.id },
      data: { status: 'paid' },
    });
  }

  res.json({ received: true });
});
```

#### 6. Auth middleware (JWT)

```typescript
// apps/api/src/middleware/auth.ts
import jwt from 'jsonwebtoken';
import type { RequestHandler } from 'express';

export const requireAuth: RequestHandler = (req, res, next) => {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) return res.status(401).json({ error: { message: 'Unauthorized' } });

  try {
    const payload = jwt.verify(header.slice(7), process.env.JWT_SECRET!) as { id: string; role: string };
    req.user = payload;
    next();
  } catch {
    res.status(401).json({ error: { message: 'Invalid or expired token' } });
  }
};

export const requireAdmin: RequestHandler = (req, res, next) => {
  if (req.user?.role !== 'admin') return res.status(403).json({ error: { message: 'Forbidden' } });
  next();
};
```

#### 7. Checkout UI with Stripe Elements (frontend)

```tsx
// apps/web/src/features/checkout/PaymentStep.tsx
import { PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';

export function PaymentStep({ clientSecret, orderId }: { clientSecret: string; orderId: string }) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    setLoading(true);
    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/orders/${orderId}/confirmation`,
      },
    });
    if (error) setError(error.message ?? 'Payment failed');
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit" disabled={loading || !stripe}>
        {loading ? 'Processing…' : 'Pay now'}
      </button>
    </form>
  );
}
```

---

### End-to-end test order flow

```
1. POST /auth/register  → receive JWT
2. GET  /products?category=shoes  → pick a product ID
3. POST /orders  { items: [{productId, quantity:1}], shippingAddress }
   → receive { order.id, clientSecret }
4. Frontend: stripe.confirmPayment({ elements, confirmParams })
   → Stripe test card: 4242 4242 4242 4242, any future exp, any CVC
5. Stripe fires payment_intent.succeeded to /webhooks/stripe
   → order.status updated to 'paid'
6. GET /orders/:id  → verify status === 'paid'
```

---

## Phase 2 — Enhancements (weeks 5–8)

- **Admin panel**: React table with `@tanstack/react-table`, product CRUD, order status management, stock editing
- **Reviews**: star rating component, review submission gated to users with a delivered order for that product
- **Image uploads**: Cloudinary integration via signed upload URLs (no server-side storage)
- **Email notifications**: Resend (or Nodemailer + SendGrid) for order confirmation and shipping updates
- **Input validation**: `zod` schemas on every API route, validated before hitting the DB
- **Rate limiting**: `express-rate-limit` on `/auth/*` (10 req/15 min), `/orders` (30 req/min)
- **Search improvement**: switch product search to `pg_trgm` trigram index or add Typesense for full-text

## Phase 3 — Polish (weeks 9–12)

- **Analytics**: product view counts (Redis `INCR`) + Recharts dashboard for admins
- **Wishlists**: saved products per user, synced server-side
- **Discount codes**: `discounts` table, applied at checkout, validated server-side before PaymentIntent creation
- **Performance**: React Query for data fetching + stale-while-revalidate caching; Vite bundle analysis; image lazy loading + next/image-style srcset via Cloudinary
- **Accessibility**: focus trap in cart drawer, `aria-live` region for cart count, keyboard-navigable filters, color contrast audit with axe-core CI check
- **Security hardening**: `helmet.js`, CORS whitelist, `Content-Security-Policy`, short JWT expiry (15 min) + refresh token rotation, parameterized queries enforced by Prisma

---

## Non-functional targets

| Concern | Target | Approach |
|---------|--------|----------|
| Page load | < 2s LCP | Code-split per route; CDN for static assets |
| API latency | < 200ms p95 | DB indexes, connection pooling (PgBouncer via Railway) |
| Accessibility | WCAG 2.1 AA | axe-core in CI, semantic HTML throughout |
| Security | OWASP Top 10 | helmet, rate limiting, bcrypt, parameterized queries |
| Responsive | 320px–1440px | Tailwind CSS breakpoints, mobile-first layout |

---

## CI/CD (`.github/workflows/ci.yml` skeleton)

```yaml
name: CI
on: [push]
jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter api typecheck
      - run: pnpm --filter web typecheck
      - run: pnpm --filter api test        # Vitest
      - run: pnpm --filter web test
      - if: github.ref == 'refs/heads/main'
        run: |
          vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
          railway up --service api
```

---

The most important things to get right early are: **price validation server-side** (never trust client cart totals), **Stripe webhook idempotency** (use `stripePaymentIntentId` as a unique key so retried webhooks don't double-update), and **JWT secret rotation** handled via env vars from day one. Everything else can evolve incrementally. -->