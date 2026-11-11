"""/corte da GW: tira as pausas (silêncios) de um vídeo falado.
Uso: python3 tools/corte.py entrada.mp4 saida.mp4 [--ruido -32] [--pausa 0.45] [--folga 0.12]
- ruido: nível (dB) abaixo do qual é silêncio; pausa: duração mínima de silêncio cortado; folga: respiro mantido nas bordas.
"""
import subprocess, sys, re, argparse, json
ap = argparse.ArgumentParser(); ap.add_argument('entrada'); ap.add_argument('saida')
ap.add_argument('--ruido', type=float, default=-32); ap.add_argument('--pausa', type=float, default=0.45); ap.add_argument('--folga', type=float, default=0.12)
a = ap.parse_args()
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.entrada]).strip())
log = subprocess.run(['ffmpeg', '-i', a.entrada, '-af', f'silencedetect=noise={a.ruido}dB:d={a.pausa}', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
if len(en) < len(st): en.append(dur)
keep, cur = [], 0.0
for s, e in zip(st, en):
    s2, e2 = s + a.folga, e - a.folga
    if s2 > cur: keep.append((cur, s2))
    cur = max(cur, e2)
if cur < dur: keep.append((cur, dur))
keep = [(s, e) for s, e in keep if e - s > 0.15]
sel = '+'.join(f'between(t,{s:.3f},{e:.3f})' for s, e in keep)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.entrada, '-vf', f"select='{sel}',setpts=N/FRAME_RATE/TB", '-af', f"aselect='{sel}',asetpts=N/SR/TB",
                '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-movflags', '+faststart', a.saida], check=True)
novo = sum(e - s for s, e in keep)
print(json.dumps({'original_s': round(dur, 1), 'final_s': round(novo, 1), 'cortado_s': round(dur - novo, 1), 'trechos': len(keep)}))
