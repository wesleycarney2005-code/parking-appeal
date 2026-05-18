# Deploy Checklist

## 1. Stripe Setup (5 minutes)
1. Go to https://dashboard.stripe.com/products
2. Click "Add product"
   - Name: "Parking Fine Appeal Letter"
   - Price: £7.99 — One time
   - Click Save
3. Copy the **Price ID** (starts with `price_...`)
4. Go to Developers > API Keys — copy your **Secret key** (starts with `sk_live_...`)

## 2. Render Setup (5 minutes)
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repo: `wesleycarney2005-code/parking-appeal`
3. Settings:
   - Name: `parking-appeal`
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Add Environment Variables:
   - `STRIPE_SECRET_KEY` = your sk_live_... key
   - `STRIPE_PRICE_ID` = your price_... ID
   - `SECRET_KEY` = any random string (e.g. `parking2026xkz`)
   - `BASE_URL` = `https://parking-appeal.onrender.com`
5. Click Deploy

## 3. Test It
- Visit your Render URL
- Click "Generate My Letter"
- Fill the form and pay with Stripe test card: `4242 4242 4242 4242`
- Confirm PDF downloads

## 4. Get a Domain (optional but recommended)
- Buy `parkingappeal.co.uk` (~£10/yr on Namecheap)
- Point to Render via CNAME

## Marketing — Do This Day 1
Post this in these places (copy/paste ready):

**Reddit (r/LegalAdviceUK, r/CasualUK, r/DIYUK):**
> "I got a parking fine last month and found the appeal process confusing, so I built a tool that generates a professional appeal letter in 2 minutes. It's £7.99 — cheaper than paying the fine. 40% of UK council PCN appeals succeed at the first stage. Link: [your URL]"

**Facebook Groups (Brighton Business, UK Motorists, Mumsnet):**
> "Has anyone successfully appealed a parking fine? I built a tool that writes the appeal letter for you — covers missing signage, broken meters, medical emergencies and more. Takes 2 minutes, costs £7.99. [URL]"

**Twitter/X:**
> "40% of parking fine appeals in the UK succeed.
> Most people don't appeal because they don't know how to write the letter.
> I built a tool that does it for you in 2 minutes — £7.99.
> [URL]
> #ParkingFine #UKMotorists"
