import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

TOKEN = os.environ["GITHUB_TOKEN"]
LOGIN = os.environ["GH_LOGIN"]

RAMP = ' .`:-=+*cs#%@'

def gh_graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_window():
    now = datetime.now(timezone.utc)
    to = now.replace(hour=23, minute=59, second=59, microsecond=0)
    frm = (now - timedelta(days=364)).replace(hour=0, minute=0, second=0, microsecond=0)
    return frm.isoformat(), to.isoformat()


QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
    repositories(first: 100, privacy: PUBLIC, isFork: false, ownerAffiliations: [OWNER]) {
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name }
          }
        }
      }
    }
  }
}
"""


def fetch_data():
    frm, to = get_window()
    result = gh_graphql(QUERY, {"login": LOGIN, "from": frm, "to": to})
    return result["data"]["user"]


def all_days(collection):
    days = []
    for week in collection["contributionCalendar"]["weeks"]:
        for d in week["contributionDays"]:
            days.append((d["date"], d["contributionCount"]))
    return days


def compute_streaks(days):
    counts = [c for _, c in days]
    longest = 0
    cur = 0
    for c in counts:
        if c > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0
    current_streak = 0
    for _, c in reversed(days):
        if c > 0:
            current_streak += 1
        else:
            break
    return current_streak, longest


def weekly_sums(collection):
    sums = []
    for week in collection["contributionCalendar"]["weeks"]:
        s = sum(d["contributionCount"] for d in week["contributionDays"])
        sums.append(s)
    return sums


def language_bytes(repos):
    totals = {}
    for repo in repos["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            totals[name] = totals.get(name, 0) + edge["size"]
    return sorted(totals.items(), key=lambda x: -x[1])


def svg_header(w, h):
    return (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{w}" height="{h}" fill="black"/>'
        f'<style>text{{font-family:monospace;fill:white;}}</style>'
    )


def write_stats_svg(total, sums):
    w, h = 500, 140
    parts = [svg_header(w, h)]
    parts.append(f'<text x="10" y="30" font-size="24" opacity="0">{total} contributions'
                  f'<animate attributeName="opacity" from="0" to="1" dur="0.6s" fill="freeze"/>'
                  f'</text>')
    maxv = max(sums) if sums else 1
    bar_w = (w - 20) / max(len(sums), 1)
    for i, v in enumerate(sums):
        bh = 0 if maxv == 0 else (v / maxv) * 80
        x = 10 + i * bar_w
        y = 120 - bh
        parts.append(
            f'<rect x="{x:.1f}" y="120" width="{bar_w*0.7:.1f}" height="0" fill="white">'
            f'<animate attributeName="height" from="0" to="{bh:.1f}" dur="0.5s" '
            f'begin="{i*0.02:.2f}s" fill="freeze"/>'
            f'<animate attributeName="y" from="120" to="{y:.1f}" dur="0.5s" '
            f'begin="{i*0.02:.2f}s" fill="freeze"/>'
            f'</rect>'
        )
    parts.append('</svg>')
    with open('stats.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))


def write_streak_svg(current, longest):
    w, h = 400, 100
    parts = [svg_header(w, h)]
    parts.append(f'<text x="10" y="30" font-size="18" opacity="0">current streak: {current} days'
                  f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0s" fill="freeze"/>'
                  f'</text>')
    parts.append(f'<text x="10" y="60" font-size="18" opacity="0">longest streak: {longest} days'
                  f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.2s" fill="freeze"/>'
                  f'</text>')
    parts.append('</svg>')
    with open('streak.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))


def write_langs_svg(langs):
    w, h = 400, 30 + 25 * min(len(langs), 6)
    parts = [svg_header(w, h)]
    top = langs[:6]
    total = sum(v for _, v in top) or 1
    for i, (name, size) in enumerate(top):
        pct = size / total * 100
        y = 30 + i * 25
        parts.append(f'<text x="10" y="{y}" font-size="14" opacity="0">{name}: {pct:.1f}%'
                      f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" '
                      f'begin="{i*0.1:.2f}s" fill="freeze"/>'
                      f'</text>')
    parts.append('</svg>')
    with open('langs.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))


def write_year_svg(days):
    cols = 53
    rows = 7
    cell = 10
    w, h = cols * cell + 20, rows * cell + 20
    parts = [svg_header(w, h)]
    maxv = max((c for _, c in days), default=1) or 1
    n = len(RAMP) - 1
    for idx, (date, count) in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = 10 + col * cell
        y = 10 + row * cell
        level = int((count / maxv) * n) if maxv else 0
        ch = RAMP[level]
        parts.append(
            f'<text x="{x}" y="{y+9}" font-size="10" opacity="0">{ch}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" '
            f'begin="{idx*0.003:.3f}s" fill="freeze"/>'
            f'</text>'
        )
    parts.append('</svg>')
    with open('year.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))


def main():
    user = fetch_data()
    collection = user["contributionsCollection"]
    total = collection["contributionCalendar"]["totalContributions"]
    days = all_days(collection)
    sums = weekly_sums(collection)
    current, longest = compute_streaks(days)
    langs = language_bytes(user["repositories"])

    write_stats_svg(total, sums)
    write_streak_svg(current, longest)
    write_langs_svg(langs)
    write_year_svg(days)

    print("wrote stats.svg, streak.svg, langs.svg, year.svg")


if __name__ == "__main__":
    main()
