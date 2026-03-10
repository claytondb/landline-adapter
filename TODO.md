# TODO - Landline Adapter

## Phase 1: Basic Calling (MVP)

**Estimated Total: $95-130 one-time + $6/mo cloud**

### Hardware
- [ ] Order Raspberry Pi 4 Model B — **$45-55** ([raspberrypi.com](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/))
- [ ] Order 32GB microSD card — **$8-12** ([Amazon](https://www.amazon.com/s?k=32gb+microsd))
- [ ] Order 5V USB-C power supply — **$10-12** ([Amazon](https://www.amazon.com/s?k=raspberry+pi+4+power+supply))
- [ ] Order Grandstream HT801 ATA — **$30-40** ([Amazon](https://www.amazon.com/s?k=grandstream+ht801))
- [ ] Find/buy a thrift store landline phone — **$5-15** (Goodwill, eBay, Facebook Marketplace)

### Cloud Setup
- [ ] Provision VPS — **$6/month** ([DigitalOcean](https://www.digitalocean.com/pricing/droplets), [Linode](https://www.linode.com/pricing/), [Vultr](https://www.vultr.com/pricing/))
- [ ] Install Asterisk — *free*
- [ ] Configure firewall (allow SIP ports 5060, 10000-20000) — *free*
- [ ] Create `kid_phone` SIP account — *free*
- [ ] Create `parent_phone` SIP account — *free*
- [ ] Test with softphone (Zoiper/Linphone) — *free apps*

### ATA Setup
- [ ] Plug phone into HT801 FXS port
- [ ] Access HT801 web UI
- [ ] Configure SIP server = VPS IP
- [ ] Configure credentials = kid_phone
- [ ] Test dial tone
- [ ] Test calling parent_phone

## Phase 2: Raspberry Pi + Web Portal

**Estimated Cost: $0** (software only, hardware from Phase 1)

### Pi Setup
- [ ] Flash Raspberry Pi OS to microSD — *free* ([download](https://www.raspberrypi.com/software/))
- [ ] Boot Pi, connect to WiFi
- [ ] Enable SSH
- [ ] Install Python 3 + Flask — *free*
- [ ] Set up as `kidphone.local` via mDNS — *free*

### Web Portal v1
- [ ] Login page (simple password) — *included in repo*
- [ ] Dashboard showing phone status — *included in repo*
- [ ] Whitelist page (add/remove numbers) — *included in repo*
- [ ] Save whitelist to JSON file — *included in repo*
- [ ] Basic styling — *included in repo*

### Call Interception
- [ ] Install Asterisk (or PJSIP) on Pi — *free*
- [ ] Register Pi as middleman between ATA and cloud
- [ ] Read whitelist on incoming dial
- [ ] Allow/block based on whitelist
- [ ] Log all call attempts

## Phase 3: Polish

**Estimated Cost: $0** (software features)

### Features
- [ ] Quiet hours (no calls 9pm-7am) — *included in repo*
- [ ] Speed dial (1=Mom, 2=Dad, etc.)
- [ ] Incoming call whitelist
- [ ] Call duration limits
- [ ] Voicemail

### UX
- [ ] Mobile-friendly web portal — *included in repo*
- [ ] Real-time call status
- [ ] Push notifications to parent — *free with Pushover or ntfy.sh*
- [ ] Call history with timestamps — *included in repo*

## Phase 4: Product

**Estimated Cost: $200-500+** (prototyping & business setup)

### Hardware
- [ ] Research custom PCB options — *free research*
- [ ] Design single-board solution (ESP32 + FXS chip?) — **$50-100** for dev boards & prototyping
- [ ] 3D print enclosure prototype — **$20-50** (or free if you have a printer)
- [ ] Cost analysis for manufacturing — *free*

### Business
- [ ] Choose product name — *free*
- [ ] Create landing page — **$0-12/year** (GitHub Pages free, or domain ~$12/yr)
- [ ] Define pricing model — *free*
- [ ] Legal: privacy policy, terms — **$0-500** (free templates or lawyer review)
- [ ] Kickstarter or pre-orders? — **$0 upfront** (Kickstarter takes ~10% of funds raised)

## Research Links

- Asterisk docs: https://www.asterisk.org/
- Grandstream HT801: https://www.grandstream.com/products/gateways-and-atas/analog-telephone-adaptors/product/ht801
- FreePBX (easier Asterisk): https://www.freepbx.org/
- PJSIP Python bindings: https://www.pjsip.org/
- ESP32 + FXS research: TBD
