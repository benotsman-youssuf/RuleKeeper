# RuleKeeper Discord Bot

Discord moderation bot using Mistral AI to detect and remove rule violations.

<img src="https://scontent.forn3-6.fna.fbcdn.net/v/t39.30808-6/447761280_908761131282105_2976580810188517736_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeHGeOJ7rkdTyTK_8IEA44KqTvc5wnj7jCVO9znCePuMJWwJ6FZzu7h4CdOH2WV-GsvCcrZQAr0fAUJAxn4IvwoP&_nc_ohc=XffUjiZV-dsQ7kNvgHrviNt&_nc_zt=23&_nc_ht=scontent.forn3-6.fna&_nc_gid=A8OhmrrM2UvFd3FTaqNwacW&oh=00_AYCDqHBAVoTdpRXzaQfz9pftGUUqkPh84DchELWBgj1bcw&oe=67749D42">

## Features

- Real-time message moderation
- Automatic content analysis using Mistral AI
- Violation detection for:
  - Business exploitation attempts
  - Negative behavior/toxicity
  - Community guideline violations
  - Academic integrity issues
- Automated warning system with embeds

## Setup

1. Clone:
```bash
git clone https://github.com/benotsman-youssuf/RuleKeeper.git
```

2. Add `.env`:
```
DISCORD_TOKEN=your_token
MISTRAL_API_KEY=your_key
```

3. Run with Python:
```bash
pip install -r requirements.txt
python app.py
```

4. Or with Docker:
```bash
docker build -t rulekeeper .
docker run -d \
  -e DISCORD_TOKEN=your_token \
  -e MISTRAL_API_KEY=your_key \
  rulekeeper
```

## Author

Youssuf Benotsman
