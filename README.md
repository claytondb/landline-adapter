# Landline Adapter

**Turn any thrift-store landline phone into a kid-safe WiFi phone with parental controls.**

## The Problem

Parents want to give kids independence to talk with friends, but:
- Smartphones come with too much (internet, social media, apps)
- Kid-specific phones require subscriptions and new hardware
- No way to repurpose cheap landline phones for modern use

## The Solution

A small WiFi adapter that:
1. Plugs into any standard RJ-11 landline phone
2. Connects to home WiFi
3. Lets kids call/receive from a **whitelist of approved numbers**
4. Gives parents a simple web portal for control

## Market Research

### Competitors (None doing exactly this)

| Product | What It Is | Why It's Different |
|---------|------------|-------------------|
| [Tin Can](https://tincan.kids/) | Complete WiFi landline-style phone | Full device, not an adapter |
| [Bark Phone](https://www.bark.us/bark-phone/) | Kid-safe smartphone | Full phone, cellular plan |
| [Troomi](https://troomi.com/) | Kid-safe smartphone | Full phone, subscription |
| Generic ATAs | VoIP adapters | No kid focus, no whitelist, no parent portal |

**Our niche:** Plug-in adapter + any phone + parental controls + no cellular plan

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Landline Phone │────▶│   Adapter Box   │────▶│   Cloud SIP     │
│   (any RJ-11)   │     │ (Pi + ATA)      │     │   Server        │
└─────────────────┘     │                 │     └────────┬────────┘
                        │ • WiFi          │              │
                        │ • Whitelist     │              ▼
                        │ • Web Portal    │     ┌─────────────────┐
                        └─────────────────┘     │  Parent's Phone │
                                                │  (SIP app)      │
                                                └─────────────────┘
```

## V1 Prototype Shopping List

### Hardware (~$80-100)

| Item | Purpose | Where to Buy | Est. Cost |
|------|---------|--------------|-----------|
| Analog landline phone | The actual phone | Thrift store, eBay | $5-15 |
| Raspberry Pi 4 Model B | Brain + web portal | raspberrypi.com | $35-55 |
| 32GB microSD card | Pi storage | Amazon | $8-12 |
| 5V USB-C power supply | Pi power | Amazon | $10 |
| Grandstream HT801 ATA | FXS interface for phone | Amazon, grandstream.com | $30-40 |

### Cloud (~$5-10/month)

| Service | Purpose | Where |
|---------|---------|-------|
| VPS (1 vCPU, 1GB RAM) | SIP server (Asterisk) | DigitalOcean, Linode, Vultr |

## Build Phases

### Phase 1: Basic Calling ✅
- [ ] Set up VPS with Asterisk
- [ ] Create SIP accounts: `kid_phone`, `parent_phone`
- [ ] Configure ATA with kid_phone credentials
- [ ] Test call from landline to parent's SIP app

### Phase 2: Raspberry Pi + Web Portal
- [ ] Set up Pi with Raspberry Pi OS
- [ ] Install Flask/Node web server
- [ ] Build parent portal at `http://kidphone.local`
  - [ ] Login page
  - [ ] Whitelist management (add/remove numbers)
  - [ ] Call logs
- [ ] Pi intercepts calls and checks whitelist

### Phase 3: Polish & Features
- [ ] Quiet hours (no calls after bedtime)
- [ ] Contact nicknames (dial "1" for Mom, "2" for Dad)
- [ ] Voicemail
- [ ] Call duration limits
- [ ] Multiple kid profiles

### Phase 4: Product Hardware
- [ ] Design custom PCB (FXS + compute + WiFi on one board)
- [ ] 3D print enclosure
- [ ] Subscription/account system
- [ ] Mobile app for parents

## Technical Notes

### Asterisk Config (Phase 1)

```ini
; /etc/asterisk/sip.conf
[kid_phone]
type=friend
secret=kidpass123
host=dynamic
context=kids

[parent_phone]
type=friend
secret=parentpass123
host=dynamic
context=default
```

```ini
; /etc/asterisk/extensions.conf
[kids]
exten => _X.,1,GotoIf($[${WHITELIST(${EXTEN})}]?allowed:blocked)
exten => _X.,n(allowed),Dial(SIP/${EXTEN}@parent_phone)
exten => _X.,n(blocked),Playback(access-denied)
exten => _X.,n,Hangup()
```

### Flask Web Portal Structure

```
web/
├── app.py              # Flask app
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── whitelist.html
├── static/
│   └── style.css
└── whitelist.json      # Approved numbers
```

## Revenue Model Ideas

1. **Hardware sale** ($49-79 one-time)
2. **Optional subscription** ($3-5/month) for:
   - Cloud call routing
   - Advanced features (call recording, analytics)
   - Multiple devices

## Name Ideas

- KidLine
- SafeDial
- TalkSafe
- PhoneBuddy
- WeeCall
- RingGuard

---

## Next Steps

1. Order the hardware (Pi 4, HT801 ATA, thrift phone)
2. Set up VPS with Asterisk
3. Get basic call working
4. Build the whitelist web portal

Let's make landlines cool again! 📞
