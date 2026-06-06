# tidal/cli.py
import sys
from tidal import data, pipeline

def format_report(result):
    lines = []
    lines.append(f"TIDAL — subject brand: {result['subject']} "
                 f"(confidence {result['subject_confidence']:.2f})")
    lines.append("")
    lines.append("Gap board (worst first):")
    for row in result["gap_board"][:5]:
        lines.append(f"  {row['topic']:12} you {row['you']*100:4.1f}%  "
                     f"vs {row['leader']} {row['leader_rate']*100:4.1f}%")
    lines.append("")
    lines.append("Fix first (by $/yr):")
    for o in result["opportunities"][:3]:
        lines.append(f"  {o['topic']:12} ${o['annual_value']:,.0f}/yr  — {o['why']}")
    lines.append("")
    hero = result["hero"]
    lines.append(f"Hero gap: {hero['topic']}")
    lines.append(f"  recipe: {hero['content']['dna']['format']}")
    lines.append(f"  top sources: {', '.join(s['url'].split('/')[2] for s in hero['sources'][:3])}")
    lines.append("")
    r = result["radar"]
    lines.append(f"Radar (month {r['month']}, {r['live']['basis']}): "
                 f"{len(r['forecast'])} seasonal movers")
    return "\n".join(lines)

def main(argv=None):
    argv = argv or sys.argv[1:]
    month = int(argv[0]) if argv else 6
    result = pipeline.run(data.load_primary(), month=month)
    print(format_report(result))

if __name__ == "__main__":
    main()
