# manutd-win-streak

A Python-based tool that tracks Manchester United's current winning streak and generates a dynamic JSON endpoint for Shields.io badges. 🔴⚪⚫

![option 1](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/aadilvagh/manutd-win-streak/main/badges/mu-streak.json)

## About

This project automatically fetches the latest match results for Manchester United from the [football-data.org](https://www.football-data.org/) API. It calculates the current winning streak (or lack thereof) and updates a JSON file hosted in this repository. This JSON file is then consumed by Shields.io to render a real-time status badge that you can embed anywhere.

## Inspiration

Inspired by [The United Strand](https://www.instagram.com/theunitedstrand/?hl=en), the Man Utd fan who refused to cut his hair until United won 5 games in a row. 💇‍♂️🚫

## How It Works

### The Script (`man-utd-win-streak.py`)

The core logic is contained in a single Python script that performs the following steps:

1.  **Fetch Data**: authenticated request to `api.football-data.org` to get the last 10 finished matches for Manchester United (Team ID: 66).
2.  **Process Results**:
    - Sorts matches by date (newest first).
    - Iterates through the matches to count consecutive wins.
    - Stops counting as soon as a draw or loss is encountered.
3.  **Determine Status**:
    - **Streak = 0**: 😂😂😂 (Grey) - *Rough times*
    - **Streak < 3**: 🥶🥶🥶 (Orange) - *Warming up*
    - **Streak Result**: 🔥🔥🔥 AMORIMS RED ARMYYY (Red) - *We are so back*
4.  **Generate output**: Writes the result to `badges/mu-streak.json` in a format compatible with Shields.io Endpoint.

### The Automation (`.github/workflows/main.yml`)

We use GitHub Actions to run this script automatically so you don't have to.

- **Schedule**: Runs every 6 hours (cron: `0 */6 * * *`).
- **Environment**: Sets up Python 3.11 and installs dependencies (`requests`, `python-dotenv`).
- **Secrets**: Injects the `FD_API_KEY` from repository secrets.
- **Commit**: If the streak has changed (and thus the JSON file has changed), the action commits the new file back to the repository. This keeps the badge URL stable while the content updates.

## Setup & Usage

### Prerequisites

1.  Get a free API Key from [football-data.org](https://www.football-data.org/client/register).
2.  Fork or Clone this repository.

### Running Locally

1.  Install dependencies:
    ```bash
    pip install requests python-dotenv
    ```
2.  Create a `.env` file in the root directory:
    ```bash
    FD_API_KEY=your_api_key_here
    ```
3.  Run the script:
    ```bash
    python man-utd-win-streak.py
    ```
    This will generate/update `badges/mu-streak.json`.

### Running on GitHub

To enable the automatic updates on your own fork:

1.  Go to your repository **Settings**.
2.  Navigate to **Secrets and variables** > **Actions**.
3.  Click **New repository secret**.
4.  **Name**: `FD_API_KEY`
5.  **Value**: (Paste your API Key).
6.  The workflow will now run automatically on the 6-hour schedule.

## Badge Integration

You can use the generated JSON to display a badge on your profile or website.

**Markdown:**
```markdown
![Man Utd Streak](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/<YOUR-USERNAME>/manutd-win-streak/main/badges/mu-streak.json)
```

**Styled (For-the-Badge):**
```markdown
![Man Utd Streak](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/<YOUR-USERNAME>/manutd-win-streak/main/badges/mu-streak.json)
```

**Note**: Replace `<YOUR-USERNAME>` with your actual GitHub username.
