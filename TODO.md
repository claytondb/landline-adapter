# TODO - Landline Adapter

## Phase 1: Basic Calling (MVP)

### Hardware
- [ ] Order Raspberry Pi 4 Model B
- [ ] Order 32GB microSD card
- [ ] Order 5V USB-C power supply
- [ ] Order Grandstream HT801 ATA
- [ ] Find/buy a thrift store landline phone

### Cloud Setup
- [ ] Provision VPS (DigitalOcean $6/mo droplet)
- [ ] Install Asterisk
- [ ] Configure firewall (allow SIP ports 5060, 10000-20000)
- [ ] Create `kid_phone` SIP account
- [ ] Create `parent_phone` SIP account
- [ ] Test with softphone (Zoiper/Linphone)

### ATA Setup
- [ ] Plug phone into HT801 FXS port
- [ ] Access HT801 web UI
- [ ] Configure SIP server = VPS IP
- [ ] Configure credentials = kid_phone
- [ ] Test dial tone
- [ ] Test calling parent_phone

## Phase 2: Raspberry Pi + Web Portal

### Pi Setup
- [ ] Flash Raspberry Pi OS to microSD
- [ ] Boot Pi, connect to WiFi
- [ ] Enable SSH
- [ ] Install Python 3 + Flask
- [ ] Set up as `kidphone.local` via mDNS

### Web Portal v1
- [ ] Login page (simple password)
- [ ] Dashboard showing phone status
- [ ] Whitelist page (add/remove numbers)
- [ ] Save whitelist to JSON file
- [ ] Basic styling

### Call Interception
- [ ] Install Asterisk (or PJSIP) on Pi
- [ ] Register Pi as middleman between ATA and cloud
- [ ] Read whitelist on incoming dial
- [ ] Allow/block based on whitelist
- [ ] Log all call attempts

## Phase 3: Polish

### Features
- [ ] Quiet hours (no calls 9pm-7am)
- [ ] Speed dial (1=Mom, 2=Dad, etc.)
- [ ] Incoming call whitelist
- [ ] Call duration limits
- [ ] Voicemail

### UX
- [ ] Mobile-friendly web portal
- [ ] Real-time call status
- [ ] Push notifications to parent
- [ ] Call history with timestamps

## Phase 4: Product

### Hardware
- [ ] Research custom PCB options
- [ ] Design single-board solution (ESP32 + FXS chip?)
- [ ] 3D print enclosure prototype
- [ ] Cost analysis for manufacturing

### Business
- [ ] Choose product name
- [ ] Create landing page
- [ ] Define pricing model
- [ ] Legal: privacy policy, terms
- [ ] Kickstarter or pre-orders?

## Research Links

- Asterisk docs: https://www.asterisk.org/
- Grandstream HT801: https://www.grandstream.com/products/gateways-and-atas/analog-telephone-adaptors/product/ht801
- FreePBX (easier Asterisk): https://www.freepbx.org/
- PJSIP Python bindings: https://www.pjsip.org/
- ESP32 + FXS research: TBD
