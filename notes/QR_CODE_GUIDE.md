# 🔲 QR Code Feature Guide - FarmTrack

## Overview
Each animal in FarmTrack has a unique QR code that links to a **public traceability page**. Anyone can scan the QR code to view the animal's history, events, and facility information—**no login required**.

---

## How to Use QR Codes

### 1️⃣ **View QR Code for an Animal**

1. Go to **Animals** page (`/animals`)
2. Click on any animal to view details
3. Click the **"View QR Code"** button in the header
4. A dialog will open showing:
   - ✅ QR code image
   - ✅ Public tracking URL
   - ✅ Download and print options

### 2️⃣ **Download QR Code**

In the QR Code dialog:
- Click **"Download QR Code"** to save as PNG
- Click **"Print"** to print the QR code
- Use these for:
  - Physical tags/labels
  - Product packaging
  - Farm signage
  - Marketing materials

### 3️⃣ **Copy Public URL**

- Click **"Copy"** button next to the URL
- Share the link via:
  - Email
  - SMS
  - Social media
  - Your website

### 4️⃣ **Scan QR Code (Public Access)**

When someone scans the QR code:
1. They're taken to `/public/{animal_id}`
2. They see:
   - ✅ Animal name, species, breed
   - ✅ Tag ID and registration date
   - ✅ Current facility location
   - ✅ Complete event timeline
   - ✅ Traceability verification badge

**No login or authentication required!** Perfect for:
- 🛒 Consumers checking product origin
- 🏪 Retailers verifying supply chain
- 🔍 Regulators conducting inspections
- 📱 Anyone interested in food traceability

---

## Technical Details

### Backend API
```
GET /api/v1/animals/{animal_id}/qr
```
Returns PNG image of QR code containing public URL.

### Public Page
```
/public/{animal_id}
```
Publicly accessible page showing animal traceability data.

### QR Code Contents
Each QR code encodes:
```
http://localhost:3000/public/{animal_id}
```
(In production, use your actual domain)

---

## Use Cases

### 🥩 **Farm to Table Transparency**
- Print QR codes on meat packaging
- Consumers scan to see farm origin, events, transport history

### 🏪 **Retail Verification**
- Display QR codes at point of sale
- Customers verify animal welfare certifications

### 🔍 **Regulatory Compliance**
- Inspectors scan QR codes during audits
- Instant access to complete traceability records

### 📦 **Supply Chain Tracking**
- Attach QR codes to shipments
- Track animal movement between facilities

---

## Security & Privacy

✅ **Public Information Only**
- QR codes link to read-only public pages
- No sensitive user data exposed
- No authentication required

✅ **Verified Data**
- All information backed by blockchain/database
- Immutable event timeline
- Trust badge shows verification status

✅ **No Editing**
- Public users can only **view** information
- Cannot modify or delete records
- All changes require authenticated access

---

## Production Deployment

### Update Frontend URL
In `nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      siteUrl: 'https://your-domain.com', // Update this!
      apiUrl: 'https://api.your-domain.com/api/v1'
    }
  }
})
```

### Update Backend URL
In `BackEnd/app/utils/qr_generator.py`:
```python
def generate_animal_qr_url(animal_id: int, base_url: str = "https://your-domain.com"):
    return f"{base_url}/public/{animal_id}"
```

---

## Examples

### Consumer Scanning at Grocery Store
```
Customer: *scans QR code on beef package*
Browser: Opens /public/42
Shows:  
  - "Angus #TAG-042" 
  - Born: Jan 15, 2024
  - Farm: Green Valley Ranch
  - Events: Birth → Vaccination → Weighing → Processing
  - ✓ Verified by FarmTrack
```

### Regulator Inspection
```
Inspector: *scans QR code on animal ear tag*
Browser: Opens /public/123
Shows:
  - Complete movement history
  - All health certifications
  - Facility compliance records
  - Anomaly flags (if any)
```

### Restaurant Marketing
```
Menu: "Our grass-fed beef comes from local farms"
         [QR Code] Scan to see the farm story
Customer: *scans*
Browser: Shows farm details, animal welfare info, journey to table
```

---

## Testing

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Open FarmTrack:**
   ```
   http://localhost:3000
   ```

3. **Login and view an animal:**
   ```
   Username: farmer@example.com
   Password: password123
   ```

4. **Click "View QR Code" button**

5. **Test public access:**
   - Copy the public URL
   - Open in incognito window (or logout)
   - Verify you can see animal info without login

---

## Troubleshooting

### QR Code Won't Load
- Check backend is running: `docker ps`
- Verify API URL in browser console
- Check animal exists: `/animals/{id}` in API docs

### Public Page Shows "Animal Not Found"
- Verify animal ID exists in database
- Check API response in Network tab
- Ensure no authentication errors

### QR Code Shows Wrong URL
- Update `siteUrl` in `nuxt.config.ts`
- Restart frontend: `docker-compose restart traceability_web`

---

## Next Steps

- 🖨️ **Print QR codes** on physical tags using thermal printer
- 📱 **Add NFC support** for tap-to-view functionality  
- 🎨 **Customize public page** with your farm branding
- 📊 **Track scan analytics** to see how many people view each animal
- 🌐 **Multilingual support** for international customers

---

**Ready to use!** The QR code feature is now fully implemented and working. 🎉
